# 🛒 E-Commerce Agent — Text-to-SQL com Gemini

Agente de IA capaz de responder perguntas em linguagem natural sobre um banco de dados de e-commerce, utilizando **Gemini 2.5 Flash** e **SQLite**. O agente converte perguntas em português para queries SQL automaticamente (Text-to-SQL), executa no banco e retorna respostas interpretadas.

## 🗂️ Estrutura do Projeto

```
ecommerce-agent/
├── banco.db               # Banco de dados SQLite (7 tabelas, ~100k registros)
├── database.py            # Conexão e utilitários do banco
├── tools.py               # Ferramentas SQL disponíveis para o agente
├── agent.py               # Configuração do agente Gemini com tool calling
├── main.py                # Script principal com loop de perguntas
├── examples.py            # Exemplos de análises prontas por categoria
├── .env                   # Variáveis de ambiente (não versionado)
├── .env.example           # Exemplo de variáveis de ambiente
├── requirements.txt       # Dependências do projeto
└── README.md
```

## 🗃️ Tabelas Disponíveis

| Tabela | Descrição | Registros |
|---|---|---|
| `dim_consumidores` | Dados dos clientes | 99.441 |
| `dim_produtos` | Catálogo de produtos | 32.951 |
| `dim_vendedores` | Dados dos vendedores | 3.095 |
| `fat_pedidos` | Pedidos com status e datas de entrega | 99.441 |
| `fat_pedido_total` | Valor total dos pedidos em BRL e USD | 99.441 |
| `fat_itens_pedidos` | Itens de cada pedido com preço e frete | 112.650 |
| `fat_avaliacoes_pedidos` | Avaliações e comentários dos pedidos | 95.307 |

## ⚙️ Pré-requisitos

- Python 3.10+
- Chave de API do Google Gemini (gratuita via [Google AI Studio](https://aistudio.google.com/apikey))

## 🚀 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/ecommerce-agent.git
cd ecommerce-agent
```

2. Crie e ative o ambiente virtual:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure a chave de API:
```bash
cp .env.example .env
# Edite o .env e adicione sua GEMINI_API_KEY
```

5. Certifique-se de que o arquivo `banco.db` está na raiz do projeto.

## ▶️ Execução

### Chat interativo
```bash
python3 main.py
```

### Exemplos de análises prontas
```bash
# Todos os exemplos
python3 examples.py

# Filtrar por categoria
python3 examples.py "Vendas e Receita"
python3 examples.py "Entrega e Logística"
python3 examples.py "Satisfação e Avaliações"
python3 examples.py "Consumidores"
python3 examples.py "Vendedores e Produtos"
```

## 💡 Exemplos de Perguntas

**Vendas e Receita**
- Quais são os 10 produtos mais vendidos?
- Qual a receita total por categoria de produto?

**Entrega e Logística**
- Quantos pedidos existem por status?
- Qual o percentual de pedidos entregues no prazo por estado?

**Satisfação e Avaliações**
- Qual a média de avaliação geral dos pedidos?
- Quais são os top 10 vendedores com melhor média de avaliação?

**Consumidores**
- Quais estados têm maior volume de pedidos e maior ticket médio?
- Quais estados têm maior atraso médio nas entregas?

**Vendedores e Produtos**
- Quais são os produtos mais vendidos por estado?
- Quais categorias têm maior taxa de avaliação negativa?

## 🏗️ Arquitetura

```
Usuário (linguagem natural)
        ↓
    main.py (loop de perguntas)
        ↓
    agent.py (Gemini 2.0 Flash)
        ↓ tool calling
    tools.py
        ↓
    database.py (SQLite)
        ↓
    banco.db
```

### Estratégias implementadas (boas práticas Text-to-SQL)
- **Tool Calling**: o agente decide quando e como consultar o banco
- **Schema como ferramenta**: o schema é consultado via tool, não jogado direto no prompt
- **Auto-correção iterativa**: em caso de erro na query, o agente tenta corrigir automaticamente
- **Retry automático**: lida com erros 503 (sobrecarga) e 429 (rate limit) da API

## 📦 Dependências

| Pacote | Uso |
|---|---|
| `google-genai` | SDK oficial do Gemini |
| `python-dotenv` | Carregamento de variáveis de ambiente |
| `tabulate` | Formatação de tabelas no terminal |