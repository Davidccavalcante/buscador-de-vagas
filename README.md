# Buscador de Vagas

Automatiza a busca de vagas no Indeed Brasil e exporta os resultados para um arquivo CSV para visualização no Excel ou Google Sheets.

## O que faz

- Busca vagas por múltiplos termos (web designer, front end, UI designer, etc.)
- Filtra por localidade (Vitória, Vila Velha, Serra ou todo o Brasil)
- Remove vagas duplicadas automaticamente
- Exporta tudo para `vagas.csv` pronto para abrir no Excel

## Como usar

1. Clone o repositório
2. Instale as dependências:
```bash
   pip install pandas requests
```
3. Configure os termos e locais de busca no início do arquivo `buscar_vagas.py`
4. Execute:
```bash
   python buscar_vagas.py
```
5. Abra o arquivo `vagas.csv` gerado no Excel ou Google Sheets

## Configuração

No arquivo `buscar_vagas.py`, edite as listas:
```python
TERMOS = ["web designer", "junior front end", ...]
LOCAIS = ["Vitoria,+ES", "Vila+Velha,+ES", ""]
```

## Tecnologias

- Python 3
- Requests — requisições HTTP
- Pandas — manipulação e exportação de dados
- XML ElementTree — parsing do feed RSS do Indeed
