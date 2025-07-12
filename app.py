from flask import Flask, request, jsonify
# import pickle
import joblib
import pandas as pd

# Inicialização do app Flask
app = Flask(__name__)

# Carregamento do modelo
# with open("modelo_contratacao.pkl", "rb") as arquivo:
#    modelo = pickle.load(arquivo)
modelo = joblib.load('modelo_contratacao.pkl')


@app.route('/')
def home():
    return '✅ API de Previsão de Contratação está rodando.'


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Pega os dados enviados em JSON
        dados = request.get_json()

        # Converte para DataFrame
        entrada = pd.DataFrame([dados])

        # Faz a predição
        probabilidade = modelo.predict_proba(entrada)[0][1]
        classe = int(probabilidade >= 0.5)

        return jsonify({
            'probabilidade_contratacao': round(probabilidade, 4),
            'previsao': classe  # 0 ou 1
        })

    except Exception as e:
        return jsonify({'erro': str(e)}), 400


# Rodar a API localmente
# if __name__ == '__main__':
#    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
