from agent import run_agent

EXEMPLOS = [
    # Análise de Vendas e Receita
    ("Vendas e Receita", "Quais são os 10 produtos mais vendidos?"),
    ("Vendas e Receita", "Qual a receita total por categoria de produto?"),

    # Análise de Entrega e Logística
    ("Entrega e Logística", "Quantos pedidos existem por status?"),
    ("Entrega e Logística", "Qual o percentual de pedidos entregues no prazo por estado?"),

    # Análise de Satisfação e Avaliações
    ("Satisfação e Avaliações", "Qual a média de avaliação geral dos pedidos?"),
    ("Satisfação e Avaliações", "Quais são os top 10 vendedores com melhor média de avaliação?"),

    # Análise de Consumidores
    ("Consumidores", "Quais estados têm maior volume de pedidos e maior ticket médio?"),
    ("Consumidores", "Quais estados têm maior atraso médio nas entregas?"),

    # Análise de Vendedores e Produtos
    ("Vendedores e Produtos", "Quais são os produtos mais vendidos por estado?"),
    ("Vendedores e Produtos", "Quais categorias têm maior taxa de avaliação negativa?"),
]


def run_examples(categorias: list[str] = None):
    """
    Executa os exemplos de análise. 
    Filtra por categoria se fornecida.
    """
    exemplos = EXEMPLOS
    if categorias:
        exemplos = [(cat, q) for cat, q in EXEMPLOS if cat in categorias]

    categoria_atual = None

    for categoria, pergunta in exemplos:
        if categoria != categoria_atual:
            categoria_atual = categoria
            print(f"\n{'='*60}")
            print(f"  📊 {categoria}")
            print(f"{'='*60}")

        print(f"\n🔍 Pergunta: {pergunta}")
        print("⏳ Consultando...")

        resposta = run_agent(pergunta)
        print(f"🤖 Resposta:\n{resposta}")
        print("-" * 60)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        categorias = sys.argv[1:]
        print(f"\nExecutando exemplos das categorias: {', '.join(categorias)}")
        run_examples(categorias)
    else:
        print("\nExecutando todos os exemplos de análise...\n")
        run_examples()