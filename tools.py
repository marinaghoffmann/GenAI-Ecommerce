from database import get_schema, run_query


def tool_executar_query(sql: str) -> str:
    """
    Executa uma query SQL de leitura no banco de dados e retorna o resultado.

    Args:
        sql: Query SQL do tipo SELECT a ser executada.

    Returns:
        Resultado da query formatado em tabela.
    """
    return run_query(sql)


def tool_obter_schema() -> str:
    """
    Retorna o schema completo do banco de dados com todas as tabelas e colunas.
    Use esta ferramenta antes de escrever qualquer query para entender a estrutura do banco.

    Returns:
        Schema completo do banco de dados.
    """
    return get_schema()


# Definição das tools no formato do Google GenAI SDK
TOOLS_DEFINITION = [
    {
        "name": "executar_query",
        "description": (
            "Executa uma query SQL SELECT no banco de dados de e-commerce e retorna os resultados. "
            "Use esta ferramenta para responder perguntas sobre vendas, produtos, consumidores, "
            "entregas, avaliações e vendedores. Apenas queries SELECT são permitidas."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "sql": {
                    "type": "string",
                    "description": "Query SQL do tipo SELECT a ser executada no banco SQLite."
                }
            },
            "required": ["sql"]
        }
    },
    {
        "name": "obter_schema",
        "description": (
            "Retorna o schema completo do banco de dados com todas as tabelas, colunas e tipos. "
            "Use esta ferramenta quando precisar entender a estrutura do banco antes de escrever uma query."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]


# Mapeamento nome -> função
TOOLS_MAP = {
    "executar_query": tool_executar_query,
    "obter_schema": tool_obter_schema,
}