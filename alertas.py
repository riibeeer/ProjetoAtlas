import streamlit as st
import pandas as pd


st.set_page_config(page_title="Alertas de Resíduos", layout="wide")


st.markdown(
    """
    <style>
    .main {
        background-color: #FF0000;  /* Cor de fundo vermelha */
        color: white;  /* Texto branco */
    }
    .block-container {
        background-color: #FF4D4D; /* Cor de fundo das seções */
    }
    .stAlert {
        background-color: #D32F2F;  /* Cor de fundo das alertas */
        color: yellow;  /* Texto em amarelo para melhorar a visibilidade */
        border: 2px solid #FFEB3B;  /* Borda amarela */
        padding: 10px;
        font-size: 16px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True
)


class Dados:
    def __init__(self, caminho_arquivo="data/planilhaDados.xlsx"):
        self.caminho_arquivo = caminho_arquivo
        self.df = self.carregar_dados()

    def carregar_dados(self):
        try:
            df = pd.read_excel(self.caminho_arquivo)
            return df
        except FileNotFoundError:
            st.error("Arquivo não encontrado. Verifique o caminho do arquivo.")
            return None


class AlertaVolume:
    def __init__(self, df):
        self.df = df
    
    def gerar_alertas(self):
        
        resumo_bairro = self.df.groupby("bairro")["volume"].agg(["mean", "std"]).reset_index()

        
        limite_superior = resumo_bairro["mean"] + 2 * resumo_bairro["std"]

        
        alertas_volume = []
        for _, row in resumo_bairro.iterrows():
            bairro = row["bairro"]
            volume_bairro = self.df[self.df["bairro"] == bairro]["volume"].sum()
            if volume_bairro > limite_superior.loc[resumo_bairro["bairro"] == bairro].values[0]:
                alertas_volume.append(f"ALERTA: Volume anômalo de resíduos no bairro {bairro}!")

        return alertas_volume


class AlertaTipoResiduo:
    def __init__(self, df):
        self.df = df
    
    def gerar_alertas(self):
        
        resumo_tipo = self.df.groupby("type")["volume"].agg(["mean", "std"]).reset_index()

        
        limite_superior_tipo = resumo_tipo["mean"] + 2 * resumo_tipo["std"]

        
        alertas_tipo = []
        for _, row in resumo_tipo.iterrows():
            tipo_residuo = row["type"]
            volume_tipo = self.df[self.df["type"] == tipo_residuo]["volume"].sum()
            if volume_tipo > limite_superior_tipo.loc[resumo_tipo["type"] == tipo_residuo].values[0]:
                alertas_tipo.append(f"ALERTA: Tipo de resíduo {tipo_residuo} com volume anômalo!")

        return alertas_tipo


class GeradorCSV:
    def __init__(self, alertas):
        self.alertas = alertas
    
    def gerar_csv(self):
        df_alertas = pd.DataFrame(self.alertas, columns=["Alerta"])
        csv = df_alertas.to_csv(index=False)
        return csv


class GerenciadorAlertas:
    def __init__(self):
        
        self.dados = Dados()
        self.alerta_volume = AlertaVolume(self.dados.df) if self.dados.df is not None else None
        self.alerta_tipo = AlertaTipoResiduo(self.dados.df) if self.dados.df is not None else None
    
    def exibir_alertas(self):
        if self.dados.df is not None:
            
            alertas_volume = self.alerta_volume.gerar_alertas()
            if alertas_volume:
                for alerta in alertas_volume:
                    st.markdown(f"<div class='stAlert'>{alerta}</div>", unsafe_allow_html=True)

            
            alertas_tipo = self.alerta_tipo.gerar_alertas()
            if alertas_tipo:
                for alerta in alertas_tipo:
                    st.markdown(f"<div class='stAlert'>{alerta}</div>", unsafe_allow_html=True)
            
            
            todos_alertas = alertas_volume + alertas_tipo

            
            if todos_alertas:
                csv = GeradorCSV(todos_alertas).gerar_csv()

                
                st.download_button(
                    label="Baixar Alertas",
                    data=csv,
                    file_name="alertas_residuos.csv",
                    mime="text/csv"
                )


def exibir_tela_alertas():
    st.title("Alertas de Resíduos")
    gerenciador_alertas = GerenciadorAlertas()
    gerenciador_alertas.exibir_alertas()


exibir_tela_alertas()
