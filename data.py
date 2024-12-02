import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Função para carregar os dados da planilha local
def carregar_dados():
    caminho_arquivo = "data/planilhaDados.xlsx"  # Altere o caminho do seu arquivo
    try:
        df = pd.read_excel(caminho_arquivo)
        return df
    except FileNotFoundError:
        st.error("Arquivo não encontrado. Verifique o caminho do arquivo.")
        return None

# Função para gerar gráfico de barras (volume de resíduos)
def gerar_grafico_barras(df, ano):
    # Filtrando os dados para o ano selecionado
    df_filtrado = df[df['year'] == ano]
    
    if df_filtrado.empty:
        st.warning(f"Não há dados para o ano {ano}.")
        return
    
    # Agrupando os dados por bairro e somando o volume
    df_resumo = df_filtrado.groupby('bairro')['volume'].sum()

    # Gerando o gráfico de barras
    plt.figure(figsize=(10, 6))
    df_resumo.plot(kind='bar', color='skyblue')
    plt.title(f'Volume de Resíduos por Bairro - Ano {ano}')
    plt.xlabel('Bairro')
    plt.ylabel('Volume de Resíduos')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(plt)

# Função para gerar gráfico de pizza (tipos de resíduos)
def gerar_grafico_pizza(df, ano, bairro):
    # Filtrando os dados para o ano e bairro selecionados
    df_filtrado = df[(df['year'] == ano) & (df['bairro'] == bairro)]
    
    if df_filtrado.empty:
        st.warning(f"Não há dados para o ano {ano} e o bairro {bairro}.")
        return
    
    # Agrupando os dados por tipo de resíduo e somando os volumes
    df_resumo = df_filtrado.groupby('type')['volume'].sum()

    # Gerando o gráfico de pizza
    plt.figure(figsize=(8, 8))
    plt.pie(df_resumo, labels=df_resumo.index, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    plt.title(f'Distribuição de Resíduos no Bairro {bairro} - Ano {ano}')
    plt.axis('equal')  # Para deixar o gráfico de pizza em formato circular
    st.pyplot(plt)

# Configuração inicial do Streamlit
st.set_page_config(page_title="Dashboard de Resíduos", layout="wide")

# Cabeçalho
st.title("Análise de Resíduos")

# Carregar os dados da planilha local
df = carregar_dados()

if df is not None:
    # Obter lista de bairros e anos únicos
    bairros = df['bairro'].unique()
    anos = df['year'].unique()

    # Opção para escolher o tipo de gráfico
    tipo_grafico = st.selectbox("Escolha o tipo de análise", ["Análise por Volume", "Análise por Tipo"])

    # Seleção do ano
    ano_selecionado = st.selectbox("Selecione o ano", sorted(anos))

    # Condicional para exibir gráficos diferentes
    if tipo_grafico == "Análise por Volume":
        # Para o gráfico de barras, o bairro não é necessário
        if st.button("Gerar Gráfico de Barras"):
            gerar_grafico_barras(df, ano_selecionado)

    elif tipo_grafico == "Análise por Tipo":
        # Para o gráfico de pizza, o usuário precisa selecionar o bairro
        bairro_selecionado = st.selectbox("Selecione o bairro", bairros)
        
        if st.button("Gerar Gráfico de Pizza"):
            gerar_grafico_pizza(df, ano_selecionado, bairro_selecionado)
