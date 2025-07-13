import json
import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_predict_success(client):
    dados_validos = {
        "idade": 35,
        "tempo_experiencia": 10,
        "nivel_profissional": "Sênior",
        "nivel_academico": "Ensino Superior Completo",
        "nivel_ingles": "Avançado",
        "nivel_espanhol": "Básico",
        "certificacoes": 3
    }

    resposta = client.post(
        '/predict',
        data=json.dumps(dados_validos),
        content_type='application/json'
    )

    assert resposta.status_code == 200
    resposta_json = resposta.get_json()
    assert 'probabilidade_contratacao' in resposta_json
    assert 'previsao' in resposta_json
    assert isinstance(resposta_json['previsao'], int)
