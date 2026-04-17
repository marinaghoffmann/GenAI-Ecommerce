import sqlite3
from tabulate import tabulate

DB_PATH = "banco.db"


def get_connection():
    """Retorna uma conexão com o banco de dados SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_schema() -> str:
    """Retorna o schema completo do banco em formato texto para o agente."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [row[0] for row in cur.fetchall()]

    schema_parts = []
    for table in tables:
        cur.execute(f"PRAGMA table_info({table})")
        columns = cur.fetchall()

        cur.execute(f"SELECT COUNT(*) FROM {table}")
        total = cur.fetchone()[0]

        cols_desc = ", ".join(f"{col[1]} ({col[2]})" for col in columns)
        schema_parts.append(
            f"Tabela: {table} ({total} registros)\nColunas: {cols_desc}"
        )

    conn.close()
    return "\n\n".join(schema_parts)


def run_query(sql: str) -> str:
    """
    Executa uma query SQL de leitura e retorna o resultado formatado.
    Apenas SELECT é permitido.
    """
    sql_clean = sql.strip().upper()
    if not sql_clean.startswith("SELECT"):
        return "Erro: apenas consultas SELECT são permitidas."

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        conn.close()

        if not rows:
            return "Nenhum resultado encontrado."

        headers = [description[0] for description in cur.description]
        return tabulate(rows, headers=headers, tablefmt="rounded_outline")

    except Exception as e:
        return f"Erro ao executar query: {str(e)}"


if __name__ == "__main__":
    print("=== SCHEMA DO BANCO ===\n")
    print(get_schema())

    print("\n=== TESTE DE QUERY ===\n")
    result = run_query("SELECT status, COUNT(*) as total FROM fat_pedidos GROUP BY status")
    print(result)