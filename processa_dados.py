import pandas as pd
import json


arquivo = 'data/planilhaDados.xlsx'  
df = pd.read_excel(arquivo)


print(df.head())


df_agrupado = df.groupby(['year', 'bairro'])['volume'].sum().reset_index()


df_agrupado['volume'] = df_agrupado['volume'].round(1)


dados_json = df_agrupado.to_dict(orient='records')


with open('dados.json', 'w') as f:
    json.dump(dados_json, f, indent=2)

print("Arquivo JSON gerado com sucesso!")


