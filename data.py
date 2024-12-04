import streamlit as st
import io
import matplotlib.pyplot as plt
from app.sistema import SistemaResiduos

# Instanciar o sistema com o caminho da planilha
sistema = SistemaResiduos("data/planilhaDados.xlsx")

# Carregar os dados
try:
    df = sistema.gerenciador_dados.carregar_dados_excel()
except FileNotFoundError:
    st.error("Arquivo de dados não encontrado. Verifique o caminho.")
    st.stop()

# Título do Dashboard
st.set_page_config(page_title="Dashboard de Resíduos", layout="wide")
st.title("Dashboard de Resíduos")

# Listar anos e bairros disponíveis na planilha
anos_disponiveis = df["year"].unique()
bairros_disponiveis = df["bairro"].unique()

# Seletor para escolher o tipo de análise
tipo_analise = st.selectbox("Escolha o tipo de análise", ["Análise por Volume", "Análise por Tipo", "Tendência ao Longo do Tempo", "Comparação entre Bairros"])

# Seletor de ano (somente para as análises de volume, tipo e comparação entre bairros)
if tipo_analise != "Tendência ao Longo do Tempo":
    ano_selecionado = st.selectbox("Selecione o ano", sorted(anos_disponiveis))

def gerar_grafico_comparacao_bairros(df, bairros_selecionados, ano_selecionado):
    # Filtrar os dados para os bairros selecionados e o ano selecionado
    dados_filtrados = df[(df["bairro"].isin(bairros_selecionados)) & (df["year"] == ano_selecionado)]
    
    # Agrupar os dados por bairro e somar o volume
    dados_agrupados = dados_filtrados.groupby('bairro')['volume'].sum()

    # Gerar o gráfico de barras
    plt.figure(figsize=(10, 6))
    dados_agrupados.plot(kind='bar', color='skyblue')
    plt.title(f'Comparação de Resíduos por Bairro - Ano {ano_selecionado}')
    plt.xlabel('Bairro')
    plt.ylabel('Volume de Resíduos (kg)')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True)

    # Salvar o gráfico em um buffer para ser exibido no Streamlit
    grafico_buffer = io.BytesIO()
    plt.savefig(grafico_buffer, format='png')
    grafico_buffer.seek(0)

    return grafico_buffer

if tipo_analise == "Análise por Volume":
    # Análise por Volume: Gráfico de barras mostrando o volume total por bairro no ano selecionado
    if st.button("Gerar Gráfico de Volume"):
        # Agrupar os dados por bairro e ano
        dados_agrupados = sistema.gerenciador_dados.agrupar_dados(["bairro", "year"], "volume")
        
        # Agora que a coluna 'year' está presente, podemos filtrá-la para o ano selecionado
        dados_agrupados = dados_agrupados[dados_agrupados["year"] == ano_selecionado]

        # Gerar o gráfico de barras
        grafico_barras = sistema.gerador_graficos.grafico_barras(
            dados_agrupados.set_index("bairro")["volume"],
            f"Volume de Resíduos por Bairro - Ano {ano_selecionado}",
            "Bairro",
            "Volume (kg)",
        )

        # Mostrar o gráfico no Streamlit
        st.image(grafico_barras, use_container_width=True)

elif tipo_analise == "Análise por Tipo":
    # Análise por Tipo: Gráfico de pizza mostrando a distribuição dos tipos de resíduos para o bairro no ano selecionado
    bairro_selecionado = st.selectbox("Selecione o bairro", sorted(bairros_disponiveis))

    if st.button("Gerar Gráfico de Pizza"):
        # Filtrar os dados por ano e bairro
        dados_filtrados = df[(df["year"] == ano_selecionado) & (df["bairro"] == bairro_selecionado)]

        # Agrupar por tipo e somar o volume
        dados_agrupados = dados_filtrados.groupby("type")["volume"].sum()

        # Gerar o gráfico de pizza
        grafico_pizza = sistema.gerador_graficos.grafico_pizza(
            dados_agrupados,
            f"Distribuição de Resíduos no Bairro {bairro_selecionado} - Ano {ano_selecionado}",
        )

        # Mostrar o gráfico no Streamlit
        st.image(grafico_pizza, use_container_width=True)

elif tipo_analise == "Tendência ao Longo do Tempo":
    # Análise de tendência ao longo do tempo
    bairro_selecionado = st.selectbox("Selecione o bairro", sorted(bairros_disponiveis))
    
    if st.button(f"Gerar Gráfico de Tendência - {bairro_selecionado}"):
        # Gerar o gráfico de tendência com a função criada
        grafico_tendencia = gerar_grafico_tendencia(df, bairro_selecionado)
        
        # Mostrar o gráfico no Streamlit
        st.image(grafico_tendencia, use_container_width=True)

elif tipo_analise == "Comparação entre Bairros":
    # Análise comparativa entre bairros
    bairros_selecionados = st.multiselect("Selecione os bairros", bairros_disponiveis)

    if len(bairros_selecionados) >= 2:  # Certificar-se de que pelo menos 2 bairros foram selecionados
        if st.button("Gerar Gráfico de Comparação entre Bairros"):
            # Gerar o gráfico de comparação com a função criada
            grafico_comparacao = gerar_grafico_comparacao_bairros(df, bairros_selecionados, ano_selecionado)

            # Mostrar o gráfico no Streamlit
            st.image(grafico_comparacao, use_container_width=True)
    else:
        st.warning("Selecione pelo menos dois bairros para comparar.")
