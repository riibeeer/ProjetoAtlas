import pandas as pd


data = pd.read_excel('planilhaDados.xlsx')


agrupado = data.groupby(['year', 'bairro', 'residuo'])['volume'].sum().reset_index()


coordenadas = {
    "Liberdade": [-12.9750, -38.5139],
    "Sé": [-23.5505, -46.6333],
    "Mooca": [-23.5654, -46.6168],
    "Vila Mariana": [-23.5858, -46.6359],
    "Penha": [-23.5319, -46.4613],
    "Santana":[1, 1],
    "Lapa":
    "Pinheiros":
    "Butantan":
    "Capela do Socorro":
    "Campo Limpo":
    "São Mateus":
    "Cidade Tiradentes":
    "Parelheiros":
    "Jabaquara":
}


agrupado['coords'] = agrupado['bairro'].map(coordenadas)


agrupado.to_json('dados_bairros.json', orient='records')


from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/dados', methods=['GET'])
def obter_dados():
    dados_json = agrupado.to_dict(orient='records')
    return jsonify(dados_json)

if __name__ == '__main__':
    app.run(debug=True)
