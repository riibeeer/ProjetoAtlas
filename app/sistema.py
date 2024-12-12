from app.gerenciador_dados import GerenciadorDeDados
from app.gerador_graficos import GeradorDeGraficos


class SistemaResiduos:
    def __init__(self, caminho_arquivo):
        self.gerenciador_dados = GerenciadorDeDados(caminho_arquivo)
        self.gerador_graficos = GeradorDeGraficos()

    def executar(self):
        
        
        df = self.gerenciador_dados.carregar_dados_excel()

        
        agrupado = self.gerenciador_dados.agrupar_dados(["year", "bairro"], "volume")

        
        grafico_barras = self.gerador_graficos.grafico_barras(
            agrupado.set_index("bairro")["volume"],
            "Volume de Resíduos por Bairro",
            "Bairro",
            "Volume (kg)",
        )

        grafico_pizza = self.gerador_graficos.grafico_pizza(
            agrupado.set_index("bairro")["volume"],
            
        )

        
        self.gerenciador_dados.salvar_json("dados.json")

        return grafico_barras, grafico_pizza
