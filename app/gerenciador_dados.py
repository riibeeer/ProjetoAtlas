import pandas as pd
import json


class GerenciadorDeDados:
    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = caminho_arquivo
        self.df = None

    def carregar_dados_excel(self):
        """Carrega dados de um arquivo Excel."""
        try:
            self.df = pd.read_excel(self.caminho_arquivo)
            return self.df
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo '{self.caminho_arquivo}' não encontrado.")

    def agrupar_dados(self, colunas_agrupamento, coluna_valor):
        """Agrupa os dados com base nas colunas e calcula o total da coluna de valor."""
        if self.df is None:
            raise ValueError("Nenhum dado foi carregado para agrupar.")
        return self.df.groupby(colunas_agrupamento)[coluna_valor].sum().reset_index()

    def salvar_json(self, caminho_saida):
        """Salva os dados carregados em um arquivo JSON."""
        if self.df is None:
            raise ValueError("Nenhum dado foi carregado para salvar em JSON.")
        dados_json = self.df.to_dict(orient="records")
        with open(caminho_saida, "w") as f:
            json.dump(dados_json, f, indent=2)
        return True
