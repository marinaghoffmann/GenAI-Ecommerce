import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from tools import TOOLS_DEFINITION, TOOLS_MAP
from database import get_schema

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-2.5-flash"


def build_system_prompt() -> str:
    schema = get_schema()
    return f"""Você é um agente especialista em análise de dados de um sistema de e-commerce brasileiro.
Você tem acesso a um banco de dados SQLite com as seguintes tabelas:

{schema}

Regras importantes:
- Sempre use a ferramenta `obter_schema` se tiver dúvida sobre a estrutura do banco.
- Sempre use a ferramenta `executar_query` para buscar dados reais antes de responder.
- Gere apenas queries SELECT. Nunca use INSERT, UPDATE, DELETE ou DROP.
- Responda sempre em português brasileiro de forma clara e objetiva.
- Ao apresentar resultados numéricos, formate valores monetários em BRL (R$).
- Se a pergunta não puder ser respondida com os dados disponíveis, explique o motivo.
"""


def run_agent(user_question: str, max_iterations: int = 10) -> str:
    """
    Executa o agente com uma pergunta do usuário e retorna a resposta final.
    Suporta auto-correção iterativa e retry em caso de sobrecarga da API.
    """
    client = genai.Client(api_key=GEMINI_API_KEY)
    tools = [types.Tool(function_declarations=TOOLS_DEFINITION)]
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_question)])
    ]
    system_prompt = build_system_prompt()

    for iteration in range(max_iterations):
        for attempt in range(5):
            try:
                response = client.models.generate_content(
                    model=MODEL,
                    contents=messages,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt,
                        tools=tools,
                    )
                )
                break
            except Exception as e:
                error_str = str(e)
                if "503" in error_str and attempt < 4:
                    print(f"  [retry] API sobrecarregada, aguardando 5s...")
                    time.sleep(5)
                elif "429" in error_str and attempt < 4:
                    print(f"  [retry] Rate limit atingido, aguardando 15s...")
                    time.sleep(15)
                else:
                    raise

        candidate = response.candidates[0]
        messages.append(types.Content(role="model", parts=candidate.content.parts))

        tool_calls = [p for p in candidate.content.parts if p.function_call]

        if not tool_calls:
            text_parts = [p.text for p in candidate.content.parts if p.text]
            return "\n".join(text_parts)

        tool_results = []
        for part in tool_calls:
            fn_name = part.function_call.name
            fn_args = dict(part.function_call.args)
            print(f"  [tool call] {fn_name}({fn_args})")

            if fn_name in TOOLS_MAP:
                result = TOOLS_MAP[fn_name](**fn_args)
            else:
                result = f"Ferramenta '{fn_name}' não encontrada."

            if result.startswith("Erro"):
                print(f"  [auto-correção] Erro detectado, agente irá tentar corrigir...")

            tool_results.append(
                types.Part(
                    function_response=types.FunctionResponse(
                        name=fn_name,
                        response={"result": result}
                    )
                )
            )

        messages.append(types.Content(role="user", parts=tool_results))

    return "Não foi possível gerar uma resposta após múltiplas tentativas."


if __name__ == "__main__":
    question = "Quais são os 10 produtos mais vendidos?"
    print(f"Pergunta: {question}\n")
    answer = run_agent(question)
    print(f"\nResposta:\n{answer}")