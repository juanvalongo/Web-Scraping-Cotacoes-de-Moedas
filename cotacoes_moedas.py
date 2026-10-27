
import os
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import pandas as pd
import requests
import seaborn as sns


# Configuração visual dos gráficos
plt.style.use("ggplot")
sns.set(style="whitegrid")


# Diretório para armazenar os dados e gráficos
DIRETORIO_DADOS = "dados_cotacoes"
os.makedirs(DIRETORIO_DADOS, exist_ok=True)


# Definição do período: últimos 30 dias
data_fim = datetime.now().strftime("%m-%d-%Y")
data_inicio = (
    datetime.now() - timedelta(days=30)
).strftime("%m-%d-%Y")


# Moedas que serão consultadas
moedas = {
    "USD": "Dólar Americano",
    "EUR": "Euro",
    "GBP": "Libra Esterlina",
    "JPY": "Iene Japonês",
    "AUD": "Dólar Australiano",
}


# Dicionário que armazenará os dados coletados
dados_cotacoes = {}


# URL-base da API PTAX do Banco Central
URL_BASE = (
    "https://olinda.bcb.gov.br/olinda/servico/PTAX/"
    "versao/v1/odata/CotacaoMoedaPeriodo"
)


print("Iniciando coleta de cotações...")
print(f"Período: {data_inicio} até {data_fim}\n")


# Consulta de cada moeda
for codigo, nome in moedas.items():
    print(f"Consultando {nome} ({codigo})...")

    parametros = {
        "@moeda": f"'{codigo}'",
        "@dataInicial": f"'{data_inicio}'",
        "@dataFinalCotacao": f"'{data_fim}'",
        "$top": 100,
        "$skip": 0,
        "$format": "json",
    }

    url = (
        f"{URL_BASE}"
        "(moeda=@moeda,dataInicial=@dataInicial,"
        "dataFinalCotacao=@dataFinalCotacao)"
    )

    cotacoes = []

    try:
        while True:
            response = requests.get(
                url,
                params=parametros,
                timeout=30,
            )

            response.raise_for_status()
            dados = response.json()

            registros = dados.get("value", [])

            for item in registros:
                cotacoes.append({
                    "data": item["dataHoraCotacao"],
                    "cotacao_compra": item["cotacaoCompra"],
                    "cotacao_venda": item["cotacaoVenda"],
                })

            # Encerrar quando não houver mais registros
            if len(registros) < parametros["$top"]:
                break

            # Avançar para o próximo conjunto de registros
            parametros["$skip"] += parametros["$top"]

        dados_cotacoes[codigo] = {
            "nome": nome,
            "cotacoes": cotacoes,
        }

        if cotacoes:
            print(f"Obtidas {len(cotacoes)} cotações.")
        else:
            print("Nenhuma cotação encontrada para o período.")

    except requests.RequestException as erro:
        dados_cotacoes[codigo] = {
            "nome": nome,
            "cotacoes": [],
        }

        print(f"Erro na consulta HTTP: {erro}")

    except (ValueError, KeyError) as erro:
        dados_cotacoes[codigo] = {
            "nome": nome,
            "cotacoes": [],
        }

        print(f"Erro ao interpretar a resposta da API: {erro}")

    print()

# Resumo da coleta
print("Resumo da coleta:")

for codigo, dados in dados_cotacoes.items():
    quantidade = len(dados["cotacoes"])
    print(f"- {dados['nome']} ({codigo}): {quantidade} registros")

# Parte 3: Processamento e armazenamento dos dados
for codigo, dados in dados_cotacoes.items():
    if dados["cotacoes"]:
        df = pd.DataFrame(dados["cotacoes"])

        # Converter a coluna de data
        df["data"] = pd.to_datetime(df["data"])

        # Ordenar por data
        df = df.sort_values("data")

        # Salvar em CSV
        arquivo_csv = os.path.join(
            DIRETORIO_DADOS,
            f"cotacao_{codigo}.csv",
        )

        df.to_csv(
            arquivo_csv,
            index=False,
            encoding="utf-8-sig",
        )

        print(f"Arquivo '{arquivo_csv}' criado com sucesso!")    

# Parte 4: Visualização dos dados

# Gráfico comparativo de todas as moedas
plt.figure(figsize=(14, 8))

for codigo, dados in dados_cotacoes.items():
    if dados["cotacoes"]:
        df = pd.DataFrame(dados["cotacoes"])
        df["data"] = pd.to_datetime(df["data"])
        df = df.sort_values("data")

        plt.plot(
            df["data"],
            df["cotacao_venda"],
            label=f"{dados['nome']} ({codigo})",
        )

plt.title(
    "Cotação de Moedas em Relação ao Real (R$) - Últimos 30 dias",
    fontsize=16,
)
plt.xlabel("Data", fontsize=12)
plt.ylabel("Valor em R$", fontsize=12)
plt.legend(fontsize=10)
plt.grid(True)
plt.tight_layout()

arquivo_grafico = os.path.join(
    DIRETORIO_DADOS,
    "grafico_todas_moedas.png",
)

plt.savefig(arquivo_grafico, dpi=300)
plt.close()

print(f"Gráfico '{arquivo_grafico}' criado com sucesso!")

# Gráficos individuais de cada moeda
for codigo, dados in dados_cotacoes.items():
    if dados["cotacoes"]:
        df = pd.DataFrame(dados["cotacoes"])
        df["data"] = pd.to_datetime(df["data"])
        df = df.sort_values("data")

        plt.figure(figsize=(12, 6))

        # Cotação de compra em verde
        plt.plot(
            df["data"],
            df["cotacao_compra"],
            label="Cotação de Compra",
            color="green",
        )

        # Cotação de venda em vermelho
        plt.plot(
            df["data"],
            df["cotacao_venda"],
            label="Cotação de Venda",
            color="red",
        )

        plt.title(
            f"Cotações de Compra e Venda - {dados['nome']} ({codigo})",
            fontsize=14,
        )
        plt.xlabel("Data", fontsize=12)
        plt.ylabel("Valor em R$", fontsize=12)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        # Salvar o gráfico individual
        arquivo_grafico = os.path.join(
            DIRETORIO_DADOS,
            f"grafico_{codigo}.png",
        )

        plt.savefig(arquivo_grafico, dpi=300)
        plt.close()

        print(
            f"Gráfico individual '{arquivo_grafico}' "
            "criado com sucesso!"
        )


# Gráfico de variação percentual das moedas
moedas_variacao = []
variacoes_percentuais = []

for codigo, dados in dados_cotacoes.items():
    if dados["cotacoes"]:
        df = pd.DataFrame(dados["cotacoes"])
        df["data"] = pd.to_datetime(df["data"])
        df = df.sort_values("data")

        # Obter as cotações de venda inicial e final
        cotacao_inicial = df["cotacao_venda"].iloc[0]
        cotacao_final = df["cotacao_venda"].iloc[-1]

        # Calcular a variação percentual
        if cotacao_inicial != 0:
            variacao = (
                (cotacao_final - cotacao_inicial)
                / cotacao_inicial
            ) * 100

            moedas_variacao.append(codigo)
            variacoes_percentuais.append(variacao)

# Definir verde para variações positivas e vermelho para negativas
cores = [
    "green" if variacao >= 0 else "red"
    for variacao in variacoes_percentuais
]

plt.figure(figsize=(10, 6))

plt.bar(
    moedas_variacao,
    variacoes_percentuais,
    color=cores,
)

plt.axhline(y=0, color="black", linewidth=0.8)
plt.title(
    "Variação Percentual das Cotações de Venda - Últimos 30 dias",
    fontsize=14,
)
plt.xlabel("Moeda", fontsize=12)
plt.ylabel("Variação (%)", fontsize=12)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()

# Salvar o gráfico
arquivo_grafico = os.path.join(
    DIRETORIO_DADOS,
    "grafico_variacao_percentual.png",
)

plt.savefig(arquivo_grafico, dpi=300)
plt.close()

print(
    f"Gráfico de variação percentual '{arquivo_grafico}' "
    "criado com sucesso!"
)


# Parte 5: Resumo estatístico das cotações
print("\n" + "=" * 60)
print("RESUMO ESTATÍSTICO DAS COTAÇÕES DE VENDA")
print("=" * 60)

for codigo, dados in dados_cotacoes.items():
    if dados["cotacoes"]:
        df = pd.DataFrame(dados["cotacoes"])
        df["data"] = pd.to_datetime(df["data"])
        df = df.sort_values("data")

        # Identificar as cotações mínima e máxima
        indice_minimo = df["cotacao_venda"].idxmin()
        indice_maximo = df["cotacao_venda"].idxmax()

        cotacao_minima = df.loc[indice_minimo]
        cotacao_maxima = df.loc[indice_maximo]

        # Calcular a média das cotações de venda
        cotacao_media = df["cotacao_venda"].mean()

        print(f"\nMoeda: {dados['nome']} ({codigo})")
        print("-" * 45)

        print(
            f"Cotação mínima: R$ "
            f"{cotacao_minima['cotacao_venda']:.4f}"
        )
        print(
            "Data da cotação mínima: "
            f"{cotacao_minima['data'].strftime('%d/%m/%Y')}"
        )

        print(
            f"Cotação máxima: R$ "
            f"{cotacao_maxima['cotacao_venda']:.4f}"
        )
        print(
            "Data da cotação máxima: "
            f"{cotacao_maxima['data'].strftime('%d/%m/%Y')}"
        )

        print(f"Cotação média: R$ {cotacao_media:.4f}")


# Parte 6: Análise de correlação entre as moedas

print("\n" + "=" * 60)
print("ANÁLISE DE CORRELAÇÃO ENTRE AS MOEDAS")
print("=" * 60)

# Dicionário para armazenar as cotações médias diárias
cotacoes_diarias = {}

# Ler os dados salvos nos arquivos CSV
for arquivo in sorted(os.listdir(DIRETORIO_DADOS)):
    if arquivo.startswith("cotacao_") and arquivo.endswith(".csv"):
        codigo = arquivo.replace("cotacao_", "").replace(".csv", "")

        caminho_csv = os.path.join(DIRETORIO_DADOS, arquivo)
        df = pd.read_csv(caminho_csv)

        # Converter a data e manter somente o dia
        df["data"] = pd.to_datetime(df["data"]).dt.date

        # Calcular a média da cotação de venda para cada dia
        media_diaria = df.groupby("data")["cotacao_venda"].mean()

        cotacoes_diarias[codigo] = media_diaria

# Reunir as cotações em uma única tabela
tabela_cotacoes = pd.DataFrame(cotacoes_diarias)

# Utilizar apenas as datas presentes em todas as moedas
tabela_cotacoes = tabela_cotacoes.dropna()

if len(tabela_cotacoes) < 2:
    print("Não há datas suficientes para calcular a correlação.")

else:
    # Calcular a matriz de correlação de Pearson
    matriz_correlacao = tabela_cotacoes.corr()

    print("\nMatriz de correlação:")
    print(matriz_correlacao.round(3))

    # Criar o mapa de calor
    plt.figure(figsize=(10, 8))

    sns.heatmap(
        matriz_correlacao,
        annot=True,
        cmap="coolwarm",
        vmin=-1,
        vmax=1,
        center=0,
        fmt=".2f",
        linewidths=0.5,
    )

    plt.title(
        "Correlação entre as Cotações de Venda das Moedas",
        fontsize=14,
    )
    plt.tight_layout()

    # Salvar o gráfico na pasta de dados
    arquivo_grafico = os.path.join(
        DIRETORIO_DADOS,
        "grafico_correlacao_moedas.png",
    )

    plt.savefig(arquivo_grafico, dpi=300)
    plt.close()

    print(f"\nMapa de calor salvo em: {arquivo_grafico}")
    print(f"Datas utilizadas na análise: {len(tabela_cotacoes)}")
