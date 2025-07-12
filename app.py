from flask import Flask, request, jsonify
from prometheus_client import start_http_server, Summary, Counter, Gauge
import time
# import pickle
import joblib
import pandas as pd

# Inicialização do app Flask
app = Flask(__name__)

# Inicie um servidor Prometheus em uma porta diferente (por exemplo, 8000)
start_http_server(8000)

# Métricas
REQUEST_TIME = Summary('request_processing_seconds',
                       'Tempo de processamento de requisição')
PREDICTION_COUNT = Counter('prediction_requests_total',
                           'Número de requisições de predição')
ERROR_COUNT = Counter('prediction_errors_total',
                      'Número de erros nas predições')
LAST_PREDICTION = Gauge('last_prediction_value', 'Último valor predito')

# Carregamento do modelo
# with open("modelo_contratacao.pkl", "rb") as arquivo:
#    modelo = pickle.load(arquivo)
modelo = joblib.load('modelo_contratacao.pkl')


@app.route('/')
def home():
    return '✅ API de Previsão de Contratação está rodando.'


@app.route('/predict', methods=['POST'])
@REQUEST_TIME.time()
def predict():
    try:
        PREDICTION_COUNT.inc()
        # Pega os dados enviados em JSON
        dados = request.get_json()
        # Converte para DataFrame
        entrada = pd.DataFrame([dados])
        # Faz a predição
        probabilidade = modelo.predict_proba(entrada)[0][1]
        classe = int(probabilidade >= 0.5)
        LAST_PREDICTION.set(probabilidade)
        return jsonify({
            'probabilidade_contratacao': round(probabilidade, 4),
            'previsao': classe  # 0 ou 1
        })

    except Exception as e:
        ERROR_COUNT.inc()
        return jsonify({'erro': str(e)}), 400


# Rodar a API localmente
# if __name__ == '__main__':
#    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
