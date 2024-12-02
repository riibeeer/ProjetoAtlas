import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
import zipfile

# Função para carregar os dados da planilha local
def carregar_dados():
    caminho_arquivo = "data/planilhaDados.xlsx"  # Altere o caminho do seu arquivo
    try:
        df = pd.read_excel(caminho_arquivo)
        return df
    except FileNotFoundError:
        st.error("Arquivo não encontrado. Verifique o caminho do arquivo.")
        return None

# Função para gerar gráfico de barras (comparando volumes entre dois anos)
def gerar_grafico_volume(df, bairro, ano1, ano2):
    # Filtrando os dados para os dois anos selecionados e para o bairro
    df_filtrado_ano1 = df[(df['bairro'] == bairro) & (df['year'] == ano1)]
    df_filtrado_ano2 = df[(df['bairro'] == bairro) & (df['year'] == ano2)]

    if df_filtrado_ano1.empty or df_filtrado_ano2.empty:
        st.warning(f"Não há dados para o bairro {bairro} nos anos {ano1} e {ano2}.")
        return None

    # Agrupando os dados por tipo de resíduo e somando o volume
    df_resumo_ano1 = df_filtrado_ano1.groupby('type')['volume'].sum()
    df_resumo_ano2 = df_filtrado_ano2.groupby('type')['volume'].sum()

    # Gerando o gráfico de barras comparando os dois anos
    df_comparativo = pd.DataFrame({
        f'{ano1}': df_resumo_ano1,
        f'{ano2}': df_resumo_ano2
    })

    plt.figure(figsize=(10, 6))
    df_comparativo.plot(kind='bar', color=['lightblue', 'lightgreen'], ax=plt.gca())
    plt.title(f'Comparação de Volume de Resíduos por Tipo - Bairro {bairro}')
    plt.xlabel('Tipo de Resíduo')
    plt.ylabel('Volume de Resíduos (kg)')
    plt.xticks(rotation=45, ha='right')

    # Salvar gráfico em um buffer de imagem
    imagem_buffer = io.BytesIO()
    plt.savefig(imagem_buffer, format='png')
    imagem_buffer.seek(0)  # Resetar o ponteiro do buffer
    return imagem_buffer

# Função para gerar gráfico de pizza (tipos de resíduos)
def gerar_grafico_pizza(df, ano, bairro):
    # Filtrando os dados para o ano e bairro selecionados
    df_filtrado = df[(df['year'] == ano) & (df['bairro'] == bairro)]

    if df_filtrado.empty:
        st.warning(f"Não há dados para o ano {ano} e o bairro {bairro}.")
        return None

    # Agrupando os dados por tipo de resíduo e somando os volumes
    df_resumo = df_filtrado.groupby('type')['volume'].sum()

    # Gerando o gráfico de pizza
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(df_resumo, labels=df_resumo.index, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    ax.set_title(f'Distribuição de Resíduos no Bairro {bairro} - Ano {ano}')
    ax.axis('equal')  # Para deixar o gráfico de pizza em formato circular

    # Salvar gráfico em um buffer de imagem
    imagem_buffer = io.BytesIO()
    plt.savefig(imagem_buffer, format='png')
    imagem_buffer.seek(0)  # Resetar o ponteiro do buffer
    return imagem_buffer

# Função para criar um arquivo zip com as imagens para download
def criar_arquivo_zip(imagem_buffer1, imagem_buffer2, nome_arquivo1, nome_arquivo2):
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Adicionar as imagens no zip
        zip_file.writestr(nome_arquivo1, imagem_buffer1.read())
        zip_file.writestr(nome_arquivo2, imagem_buffer2.read())
    
    zip_buffer.seek(0)
    return zip_buffer

# Função para baixar o arquivo zip com os gráficos
def baixar_arquivos_zip(zip_buffer):
    st.download_button(
        label="Baixar Gráficos",
        data=zip_buffer,
        file_name="graficos_residuos.zip",
        mime="application/zip"
    )

# Configuração inicial do Streamlit
st.set_page_config(page_title="Tela de Relatórios - Resíduos", layout="wide")

# Cabeçalho
st.title("Relatórios de Resíduos")

# Carregar os dados da planilha local
df = carregar_dados()

if df is not None:
    # Obter lista de bairros e anos únicos
    bairros = df['bairro'].unique()
    anos = df['year'].unique()

    # Opção para escolher o tipo de gráfico (tipos de resíduos ou volume)
    tipo_grafico = st.selectbox("Escolha o tipo de gráfico", ["Comparativo de Volume", "Distribuição de Tipos de Resíduos"])

    # Seleção do bairro
    bairro_selecionado = st.selectbox("Selecione o bairro", bairros)

    if tipo_grafico == "Comparativo de Volume":
        # Seleção dos dois anos
        ano1 = st.selectbox(f"Selecione o primeiro ano", sorted(anos))
        ano2 = st.selectbox(f"Selecione o segundo ano", sorted(anos))

        # Gerar gráfico de volume comparativo
        if st.button(f"Gerar Gráfico de Volume - {bairro_selecionado}"):
            imagem_buffer = gerar_grafico_volume(df, bairro_selecionado, ano1, ano2)
            
            # Exibir o gráfico
            if imagem_buffer:
                st.image(imagem_buffer, use_container_width=True)
                # Criar botão de download (sem duplicar o botão)
                st.download_button(
                    label="Baixar Gráfico",
                    data=imagem_buffer,
                    file_name=f"grafico_volume_{bairro_selecionado}_{ano1}_{ano2}.png",
                    mime="image/png"
                )

    elif tipo_grafico == "Distribuição de Tipos de Resíduos":
        # Seleção dos dois anos para gerar os gráficos de pizza
        ano1 = st.selectbox(f"Selecione o primeiro ano", sorted(anos))
        ano2 = st.selectbox(f"Selecione o segundo ano", sorted(anos))

        # Gerar gráficos de pizza para os dois anos selecionados
        if st.button(f"Gerar Gráficos de Tipos de Resíduos - {bairro_selecionado}"):
            # Gerar gráfico de pizza para o primeiro ano
            imagem_buffer1 = gerar_grafico_pizza(df, ano1, bairro_selecionado)
            imagem_buffer2 = gerar_grafico_pizza(df, ano2, bairro_selecionado)

            # Exibir os gráficos lado a lado
            if imagem_buffer1 and imagem_buffer2:
                col1, col2 = st.columns(2)
                with col1:
                    st.image(imagem_buffer1, use_container_width=True)
                with col2:
                    st.image(imagem_buffer2, use_container_width=True)

                # Criar um arquivo zip com as duas imagens e exibir o botão de download único
                zip_buffer = criar_arquivo_zip(imagem_buffer1, imagem_buffer2, f"grafico_pizza_{bairro_selecionado}_{ano1}.png", f"grafico_pizza_{bairro_selecionado}_{ano2}.png")
                baixar_arquivos_zip(zip_buffer)
