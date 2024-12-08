import streamlit as st
import io
import matplotlib.pyplot as plt
from app.sistema import SistemaResiduos


sistema = SistemaResiduos("data/planilhaDados.xlsx")


try:
    df = sistema.gerenciador_dados.carregar_dados_excel()
except FileNotFoundError:
    st.error("Arquivo de dados não encontrado. Verifique o caminho.")
    st.stop()


st.set_page_config(page_title="Dashboard de Resíduos", layout="wide")
st.title("Dashboard de Resíduos")


anos_disponiveis = df["year"].unique()
bairros_disponiveis = df["bairro"].unique()


tipo_analise = st.selectbox("Escolha o tipo de análise", ["Análise por Volume", "Análise por Tipo", "Tendência ao Longo do Tempo", "Comparação entre Bairros"])


if tipo_analise != "Tendência ao Longo do Tempo":
    ano_selecionado = st.selectbox("Selecione o ano", sorted(anos_disponiveis))


def gerar_grafico_comparacao_bairros(df, bairros_selecionados, ano_selecionado):
    dados_filtrados = df[(df["bairro"].isin(bairros_selecionados)) & (df["year"] == ano_selecionado)]
    dados_agrupados = dados_filtrados.groupby('bairro')['volume'].sum()

    plt.figure(figsize=(10, 6))
    dados_agrupados.plot(kind='bar', color='skyblue')
    plt.title(f'Comparação de Resíduos por Bairro - Ano {ano_selecionado}')
    plt.xlabel('Bairro')
    plt.ylabel('Volume de Resíduos (kg)')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True)

    grafico_buffer = io.BytesIO()
    plt.savefig(grafico_buffer, format='png')
    grafico_buffer.seek(0)
    return grafico_buffer


def gerar_grafico_tendencia(df, bairro_selecionado):
    dados_filtrados = df[df["bairro"] == bairro_selecionado]
    dados_agrupados = dados_filtrados.groupby("year")["volume"].sum()

    plt.figure(figsize=(10, 6))
    plt.plot(dados_agrupados.index, dados_agrupados.values, marker='o', color='skyblue')
    plt.title(f"Tendência de Resíduos ao Longo do Tempo - Bairro {bairro_selecionado}")
    plt.xlabel("Ano")
    plt.ylabel("Volume de Resíduos (kg)")
    plt.grid(True)

    grafico_buffer = io.BytesIO()
    plt.savefig(grafico_buffer, format='png')
    grafico_buffer.seek(0)
    return grafico_buffer


if tipo_analise == "Análise por Volume":
    if st.button("Gerar Gráfico de Volume"):
        dados_agrupados = sistema.gerenciador_dados.agrupar_dados(["bairro", "year"], "volume")
        dados_agrupados = dados_agrupados[dados_agrupados["year"] == ano_selecionado]

        grafico_barras = sistema.gerador_graficos.grafico_barras(
            dados_agrupados.set_index("bairro")["volume"],
            f"Volume de Resíduos por Bairro - Ano {ano_selecionado}",
            "Bairro",
            "Volume (kg)",
        )
        st.image(grafico_barras, use_container_width=True)

elif tipo_analise == "Análise por Tipo":
    bairro_selecionado = st.selectbox("Selecione o bairro", sorted(bairros_disponiveis))

    if st.button("Gerar Gráfico de Pizza"):
        dados_filtrados = df[(df["year"] == ano_selecionado) & (df["bairro"] == bairro_selecionado)]
        dados_agrupados = dados_filtrados.groupby("type")["volume"].sum()

        grafico_pizza = sistema.gerador_graficos.grafico_pizza(
            dados_agrupados,
            f"Distribuição de Resíduos no Bairro {bairro_selecionado} - Ano {ano_selecionado}",
        )
        st.image(grafico_pizza, use_container_width=True)

elif tipo_analise == "Tendência ao Longo do Tempo":
    bairro_selecionado = st.selectbox("Selecione o bairro", sorted(bairros_disponiveis))
    
    if st.button(f"Gerar Gráfico de Tendência - {bairro_selecionado}"):
        grafico_tendencia = gerar_grafico_tendencia(df, bairro_selecionado)
        st.image(grafico_tendencia, use_container_width=True)

elif tipo_analise == "Comparação entre Bairros":
    bairros_selecionados = st.multiselect("Selecione os bairros", bairros_disponiveis)

    if len(bairros_selecionados) >= 2:
        if st.button("Gerar Gráfico de Comparação entre Bairros"):
            grafico_comparacao = gerar_grafico_comparacao_bairros(df, bairros_selecionados, ano_selecionado)
            st.image(grafico_comparacao, use_container_width=True)
    else:
        st.warning("Selecione pelo menos dois bairros para comparar.")
