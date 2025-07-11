from flask import Flask, request, jsonify
import joblib
import pandas as pd

# Inicializa o app
app = Flask(__name__)

# Carrega o modelo treinado
modelo = joblib.load('modelo_contratacao.pkl')


@app.route('/')
def home():
    return 'API de Previsão de Contratação - OK'

# Endpoint de predição


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Recebe os dados em JSON
        dados = request.get_json()

        # Transforma em DataFrame
        entrada = pd.DataFrame([dados])

        # Realiza a predição
        probabilidade = modelo.predict_proba(entrada)[0][1]
        classe = int(probabilidade >= 0.5)

        return jsonify({
            'probabilidade_contratacao': round(probabilidade, 4),
            'previsao': classe
        })

    except Exception as e:
        return jsonify({'erro': str(e)}), 400


# Executa localmente
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
