# Web Scraper de Cotações de Moedas

Projeto acadêmico desenvolvido na disciplina de **Big Data**, no curso
de Análise e Desenvolvimento de Sistemas do Senac Pernambuco. A
atividade utiliza Python para coletar, organizar, analisar e visualizar
cotações de moedas estrangeiras em relação ao real (R\$), por meio da
API PTAX do Banco Central do Brasil.

## Objetivos

-   Consultar cotações de moedas estrangeiras em uma API pública.
-   Tratar e organizar os dados com Pandas.
-   Exportar os dados coletados para arquivos CSV.
-   Criar gráficos para comparar cotações e observar suas variações.
-   Calcular estatísticas descritivas e analisar a correlação entre as
    moedas.

## Tecnologias e bibliotecas

-   **Python**
-   **Requests** --- requisições HTTP à API.
-   **Pandas** --- tratamento, organização e exportação dos dados.
-   **Matplotlib** e **Seaborn** --- criação das visualizações.
-   **datetime** --- cálculo do período consultado.
-   **API PTAX do Banco Central do Brasil** --- fonte das cotações.

## Moedas analisadas

  Código   Moeda
  -------- -------------------
  USD      Dólar americano
  EUR      Euro
  GBP      Libra esterlina
  JPY      Iene japonês
  AUD      Dólar australiano

**Nota sobre a escolha das moedas:** o enunciado original mencionava o
peso argentino (ARS), mas essa moeda não está disponível no catálogo da
série PTAX consultada com cotações de compra e venda. Por esse motivo,
foi substituída pelo dólar australiano (AUD), mantendo a coleta na mesma
fonte de dados.

## Funcionalidades

1.  Consulta as cotações referentes aos últimos 30 dias.
2.  Faz a coleta paginada para recuperar todos os registros
    disponibilizados pela API.
3.  Salva os dados de cada moeda em um arquivo CSV dentro de
    `dados_cotacoes/`.
4.  Gera um gráfico comparativo das cotações de venda das moedas.
5.  Gera um gráfico individual para cada moeda, com cotações de compra e
    venda.
6.  Calcula a variação percentual entre a primeira e a última cotação
    disponível.
7.  Exibe estatísticas de mínimo, máximo e média das cotações de venda.
8.  Calcula e salva uma matriz de correlação entre as cotações médias
    diárias.

## Estrutura do projeto

``` text
.
├── cotacoes_moedas.py
├── dados_cotacoes/
│   ├── cotacao_USD.csv
│   ├── cotacao_EUR.csv
│   ├── cotacao_GBP.csv
│   ├── cotacao_JPY.csv
│   ├── cotacao_AUD.csv
│   ├── grafico_todas_moedas.png
│   ├── grafico_variacao_percentual.png
│   ├── grafico_correlacao_moedas.png
│   └── grafico_<CODIGO>.png
├── README.md
└── .gitignore
```

Os arquivos CSV e os gráficos são resultados gerados pelo programa. A
pasta pode estar vazia antes da primeira execução.

## Como executar

### 1. Pré-requisitos

Instale o Python 3.10 ou superior e tenha acesso à internet para
consultar a API do Banco Central.

### 2. Clone o repositório

``` bash
git clone https://github.com/juanvalongo/Web-Scraper-G1.git
cd Web-Scraper-G1
```

### 3. Crie e ative um ambiente virtual (recomendado)

No Windows, usando PowerShell:

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

No macOS ou Linux:

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Instale as dependências

``` bash
python -m pip install requests pandas matplotlib seaborn
```

### 5. Execute o programa

``` bash
python cotacoes_moedas.py
```

Ao finalizar, o programa apresenta o resumo estatístico no terminal e
grava os CSVs e gráficos no diretório `dados_cotacoes/`.

## Fonte dos dados

Os dados são obtidos da API OData PTAX do Banco Central do Brasil:

-   [Serviço PTAX --- Banco Central do
    Brasil](https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/)

A disponibilidade de registros depende da API e do calendário de
divulgação. O período é calculado dinamicamente a partir da data de
execução.

## Análise de correlação

O projeto calcula a correlação entre as cotações médias diárias das
moedas nas datas comuns disponíveis. Uma correlação positiva indica que
duas séries tenderam a variar na mesma direção durante o período
analisado; isso, por si só, **não demonstra relação de causa e efeito**.
Como a janela é curta, os resultados devem ser interpretados como
exploratórios.

## Observações

-   É necessária conexão com a internet durante a coleta.
-   A API pode retornar dados em páginas; o programa percorre essas
    páginas para não limitar a coleta aos primeiros registros.
-   Os valores e gráficos mudam conforme a data em que o programa é
    executado.
-   Este projeto tem finalidade educacional e não constitui recomendação
    de investimento.

## Autor

Projeto acadêmico desenvolvido por **Juan Valongo** para a disciplina de
Big Data --- Senac Pernambuco.
