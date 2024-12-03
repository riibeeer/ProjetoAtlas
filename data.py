import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def carregar_dados():
    caminho_arquivo = "data/planilhaDados.xlsx"
    try:
        df = pd.read_excel(caminho_arquivo)
        return df
    except FileNotFoundError:
        st.error("Arquivo não encontrado. Verifique o caminho do arquivo.")
        return None


def gerar_grafico_barras(df, ano):
    df_filtrado = df[df['year'] == ano]
    if df_filtrado.empty:
        st.warning(f"Não há dados para o ano {ano}.")
        return

    df_resumo = df_filtrado.groupby('bairro')['volume'].sum()
    plt.figure(figsize=(10, 6))
    df_resumo.plot(kind='bar', color='skyblue')
    plt.title(f'Volume de Resíduos por Bairro - Ano {ano}')
    plt.xlabel('Bairro')
    plt.ylabel('Volume de Resíduos')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(plt)


def gerar_grafico_pizza(df, ano, bairro):
    df_filtrado = df[(df['year'] == ano) & (df['bairro'] == bairro)]
    if df_filtrado.empty:
        st.warning(f"Não há dados para o ano {ano} e o bairro {bairro}.")
        return

    df_resumo = df_filtrado.groupby('type')['volume'].sum()
    plt.figure(figsize=(8, 8))
    plt.pie(df_resumo, labels=df_resumo.index, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    plt.title(f'Distribuição de Resíduos no Bairro {bairro} - Ano {ano}')
    plt.axis('equal')
    st.pyplot(plt)


st.set_page_config(page_title="Dashboard de Resíduos", layout="wide")

st.title("Análise de Resíduos")

df = carregar_dados()

if df is not None:
    bairros = df['bairro'].unique()
    anos = df['year'].unique()

    tipo_grafico = st.selectbox("Escolha o tipo de análise", ["Análise por Volume", "Análise por Tipo"])
    ano_selecionado = st.selectbox("Selecione o ano", sorted(anos))

    if tipo_grafico == "Análise por Volume":
        if st.button("Gerar Gráfico de Barras"):
            gerar_grafico_barras(df, ano_selecionado)

    elif tipo_grafico == "Análise por Tipo":
        bairro_selecionado = st.selectbox("Selecione o bairro", sorted(bairros))
        if st.button("Gerar Gráfico de Pizza"):
            gerar_grafico_pizza(df, ano_selecionado, bairro_selecionado)
