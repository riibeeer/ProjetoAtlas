import pandas as pd
import json

# Carregar a planilha .xlsx
arquivo = 'data/planilhaDados.xlsx'  # Substitua pelo caminho da sua planilha
df = pd.read_excel(arquivo)

# Exibir as primeiras linhas para garantir que os dados estão corretos
print(df.head())

# Agrupar os dados por 'year' e 'bairro', somando o 'volume'
df_agrupado = df.groupby(['year', 'bairro'])['volume'].sum().reset_index()

# Arredondar o volume para 1 casa decimal
df_agrupado['volume'] = df_agrupado['volume'].round(1)

# Converter o DataFrame agrupado para um formato de lista de dicionários
dados_json = df_agrupado.to_dict(orient='records')

# Salvar os dados no formato JSON
with open('dados.json', 'w') as f:
    json.dump(dados_json, f, indent=2)

print("Arquivo JSON gerado com sucesso!")
