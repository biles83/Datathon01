import json
import pytest
import base64
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def get_auth_headers(username='admin', password='admin@123'):
    credentials = f"{username}:{password}"
    token = base64.b64encode(credentials.encode()).decode()
    return {'Authorization': f'Basic {token}'}


def test_predict_success(client):
    dados_validos = {
        "area_atuacao": "TI",
        "idade": 30,
        "tempo_experiencia": 10,
        "nivel_profissional": "Sênior",
        "nivel_academico": "Pós Graduação Completo",
        "nivel_ingles": "Avançado",
        "nivel_espanhol": "Básico",
        "certificacoes": 3
    }

    resposta = client.post(
        '/predict',
        data=json.dumps(dados_validos),
        headers={
            'Content-Type': 'application/json',
            **get_auth_headers()
        }
    )

    assert resposta.status_code == 200
    resposta_json = resposta.get_json()
    assert 'probabilidade_contratacao' in resposta_json
    assert 'previsao' in resposta_json
    assert isinstance(resposta_json['previsao'], int)


def test_predict_missing_fields(client):
    dados_incompletos = {
        "idade": 28,
        "nivel_profissional": "Pleno"
    }

    resposta = client.post(
        '/predict',
        data=json.dumps(dados_incompletos),
        headers={
            'Content-Type': 'application/json',
            **get_auth_headers()
        }
    )

    assert resposta.status_code == 400
    resposta_json = resposta.get_json()
    assert 'erro' in resposta_json


def test_predict_invalid_type(client):
    dados_invalidos = {
        "area_atuacao": "TI",
        "idade": "trinta",
        "tempo_experiencia": 5,
        "nivel_profissional": "Júnior",
        "nivel_academico": "Médio",
        "nivel_ingles": "Intermediário",
        "nivel_espanhol": "Básico",
        "certificacoes": 1
    }

    resposta = client.post(
        '/predict',
        data=json.dumps(dados_invalidos),
        headers={
            'Content-Type': 'application/json',
            **get_auth_headers()
        }
    )

    assert resposta.status_code == 400
    resposta_json = resposta.get_json()
    assert 'erro' in resposta_json


def test_predict_multiple_requests(client):
    dados = {
        "area_atuacao": "TI",
        "idade": 30,
        "tempo_experiencia": 7,
        "nivel_profissional": "Pleno",
        "nivel_academico": "Ensino Superior Completo",
        "nivel_ingles": "Avançado",
        "nivel_espanhol": "Básico",
        "certificacoes": 2
    }

    for _ in range(5):
        resposta = client.post(
            '/predict',
            data=json.dumps(dados),
            headers={
                'Content-Type': 'application/json',
                **get_auth_headers()
            }
        )
        assert resposta.status_code == 200
        assert 'probabilidade_contratacao' in resposta.get_json()
