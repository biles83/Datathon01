from collections import deque
from flask import Flask, request, jsonify
from prometheus_client import start_http_server, Summary, Counter, Gauge
import time
# import pickle
import joblib
import pandas as pd
import logging

# Inicialização do app Flask
app = Flask(__name__)

# Inicie um servidor Prometheus em uma porta diferente (por exemplo, 8000)
start_http_server(8000)

# Configuração básica de logging
# Configurações de log
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("api.log"),
        logging.StreamHandler()
    ]
)

DRIFT_GAUGE = Gauge('prediction_drift_score',
                    'Métrica de drift baseada na média móvel das previsões')

# Janela deslizante para as probabilidades
predicoes = deque(maxlen=100)

MEDIA_TREINAMENTO = 0.62  # Exemplo: média da probabilidade no dataset de treino

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
        dados = request.get_json()
        entrada = pd.DataFrame([dados])

        # Validação de tipos esperados
        tipos_esperados = {
            "idade": int,
            "tempo_experiencia": int,
            "nivel_profissional": str,
            "nivel_academico": str,
            "nivel_ingles": str,
            "nivel_espanhol": str,
            "certificacoes": int
        }

        for campo, tipo in tipos_esperados.items():
            if campo not in dados:
                raise ValueError(f"Campo ausente: {campo}")
            if not isinstance(dados[campo], tipo):
                raise ValueError(
                    f"Tipo inválido para '{campo}'. Esperado {tipo.__name__}, recebido {type(dados[campo]).__name__}")

        probabilidade = modelo.predict_proba(entrada)[0][1]
        classe = int(probabilidade >= 0.35)

        # Atualiza drift
        predicoes.append(probabilidade)
        media_atual = sum(predicoes) / len(predicoes)
        drift_score = abs(media_atual - MEDIA_TREINAMENTO)
        DRIFT_GAUGE.set(drift_score)

        LAST_PREDICTION.set(probabilidade)
        logging.info(f"Recebida nova requisição: {dados}")
        logging.info(
            f"Probabilidade predita: {probabilidade}, Classe: {classe}")
        return jsonify({
            'probabilidade_contratacao': round(probabilidade, 4),
            'previsao': classe  # 0 ou 1
        })

    except Exception as e:
        ERROR_COUNT.inc()
        logging.exception("Erro durante a predição")
        return jsonify({'erro': str(e)}), 400


# Rodar a API localmente
# if __name__ == '__main__':
#    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
