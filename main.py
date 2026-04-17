from agent import run_agent

BANNER = """
╔══════════════════════════════════════════════════════╗
║        🛒 Agente de Análise de E-Commerce            ║
║        Powered by Gemini 2.5 Flash + SQLite          ║
║  Digite 'sair' para encerrar | 'limpar' para limpar  ║
╚══════════════════════════════════════════════════════╝
"""

EXEMPLOS = """
💡 Exemplos de perguntas:
  - Quais são os 10 produtos mais vendidos?
  - Qual a receita total por categoria de produto?
  - Quantos pedidos existem por status?
  - Qual a média de avaliação geral dos pedidos?
  - Quais estados têm maior volume de pedidos?
  - Quais são os top 10 vendedores por avaliação?
"""


def main():
    print(BANNER)
    print(EXEMPLOS)

    while True:
        try:
            user_input = input("\n🔍 Sua pergunta: ").strip()

            if not user_input:
                continue

            if user_input.lower() == "sair":
                print("\nAté logo! 👋")
                break

            if user_input.lower() == "limpar":
                print("\033[H\033[J", end="")
                print(BANNER)
                print(EXEMPLOS)
                continue

            print("\n⏳ Consultando o banco de dados...\n")
            resposta = run_agent(user_input)
            print(f"🤖 Resposta:\n{resposta}")

        except KeyboardInterrupt:
            print("\n\nAté logo! 👋")
            break
        except Exception as e:
            print(f"\n❌ Erro inesperado: {e}")


if __name__ == "__main__":
    main()