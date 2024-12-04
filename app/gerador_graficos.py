import matplotlib.pyplot as plt
import io


class GeradorDeGraficos:
    @staticmethod
    def grafico_barras(dados, titulo, xlabel, ylabel):
        """Gera um gráfico de barras e retorna como buffer de imagem."""
        plt.figure(figsize=(10, 6))
        dados.plot(kind="bar", color="skyblue")
        plt.title(titulo)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        
        # Salvar imagem em buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        plt.close()  # Fecha a figura para liberar memória
        return buffer

    @staticmethod
    def grafico_pizza(dados, titulo):
        """Gera um gráfico de pizza e retorna como buffer de imagem."""
        plt.figure(figsize=(8, 8))
        plt.pie(
            dados,
            labels=dados.index,
            autopct="%1.1f%%",
            startangle=140,
            colors=plt.cm.Paired.colors,
        )
        plt.title(titulo)
        plt.axis("equal")
        
        # Salvar imagem em buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        plt.close()  # Fecha a figura para liberar memória
        return buffer
