import streamlit as st
import pandas as pd

# Definindo a classe Notificacao
class Notificacao:
    def __init__(self, id, text, read=False):
        self.id = id
        self.text = text
        self.read = read
    
    def marcar_como_lida(self):
        self.read = True
    
    def __str__(self):
        return f"ID: {self.id}, Texto: {self.text}, Lida: {self.read}"

# Classe que gerencia o histórico de notificações
class HistoricoDeNotificacoes:
    def __init__(self):
        # Se não existir o histórico de notificações, criamos um estado inicial
        if 'notificacoes' not in st.session_state:
            st.session_state.notificacoes = []
    
    def exibir_notificacoes(self):
        for notificacao in st.session_state.notificacoes:
            if not notificacao.read:
                st.markdown(f"<div style='background-color: rgba(0, 0, 0, 0.5); color: #fff; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>{notificacao.text}</div>", unsafe_allow_html=True)
                
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button(f"Marcar como Lida ({notificacao.id})"):
                        notificacao.marcar_como_lida()
                        st.session_state.notificacoes = st.session_state.notificacoes  # Força a atualização do estado
                with col2:
                    if st.button(f"Arquivar ({notificacao.id})"):
                        st.session_state.notificacoes = [n for n in st.session_state.notificacoes if n.id != notificacao.id]

    def adicionar_notificacao(self, text):
        id_nova_notificacao = len(st.session_state.notificacoes) + 1
        nova_notificacao = Notificacao(id_nova_notificacao, text)
        st.session_state.notificacoes.append(nova_notificacao)
        
    def limpar_notificacoes(self):
        st.session_state.notificacoes = []

# Função para carregar os dados
def carregar_dados():
    caminho_arquivo = "data/planilhaDados.xlsx"
    try:
        df = pd.read_excel(caminho_arquivo)
        return df
    except FileNotFoundError:
        st.error("Arquivo não encontrado. Verifique o caminho do arquivo.")
        return None

# Função para gerar alertas de volume anômalo
def alerta_volume_ano(df):
    resumo_bairro = df.groupby("bairro")["volume"].agg(["mean", "std"]).reset_index()
    limite_superior = resumo_bairro["mean"] + 2 * resumo_bairro["std"]
    alertas_volume = []
    for _, row in resumo_bairro.iterrows():
        bairro = row["bairro"]
        volume_bairro = df[df["bairro"] == bairro]["volume"].sum()
        if volume_bairro > limite_superior.loc[resumo_bairro["bairro"] == bairro].values[0]:
            alertas_volume.append(f"ALERTA: Volume anômalo de resíduos no bairro {bairro}!")
    return alertas_volume

# Função para gerar alertas de tipo de resíduo inesperado
def alerta_tipo_residuo(df):
    resumo_tipo = df.groupby("type")["volume"].agg(["mean", "std"]).reset_index()
    limite_superior_tipo = resumo_tipo["mean"] + 2 * resumo_tipo["std"]
    alertas_tipo = []
    for _, row in resumo_tipo.iterrows():
        tipo_residuo = row["type"]
        volume_tipo = df[df["type"] == tipo_residuo]["volume"].sum()
        if volume_tipo > limite_superior_tipo.loc[resumo_tipo["type"] == tipo_residuo].values[0]:
            alertas_tipo.append(f"ALERTA: Tipo de resíduo {tipo_residuo} com volume anômalo!")
    return alertas_tipo

# Função principal que exibe os alertas e as notificações
def exibir_alertas_e_notificacoes():
    df = carregar_dados()
    historico = HistoricoDeNotificacoes()

    if df is not None:
        # Gerar alertas de volume anômalo e tipo de resíduo
        alertas_volume = alerta_volume_ano(df)
        alertas_tipo = alerta_tipo_residuo(df)
        
        # Adicionar os alertas como notificações reais
        for alerta in alertas_volume + alertas_tipo:
            historico.adicionar_notificacao(alerta)
    
    # Exibir as notificações com estilo verde
    st.title("Histórico de Notificações")
    # Usando a cor verde similar ao HTML
    st.markdown("<style>body{background-color: #A8E6CF;}</style>", unsafe_allow_html=True)
    historico.exibir_notificacoes()

# Chamar a função para exibir alertas e notificações
exibir_alertas_e_notificacoes()
