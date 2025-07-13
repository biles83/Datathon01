import json
import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Teste de sucesso com dados válidos


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

# Teste com dados faltando


def test_predict_missing_fields(client):
    dados_incompletos = {
        "idade": 28,
        "nivel_profissional": "Pleno"
        # faltando campos obrigatórios
    }

    resposta = client.post(
        '/predict',
        data=json.dumps(dados_incompletos),
        content_type='application/json'
    )

    assert resposta.status_code == 400
    resposta_json = resposta.get_json()
    assert 'erro' in resposta_json

# Teste com tipo inválido


def test_predict_invalid_type(client):
    dados_invalidos = {
        "idade": "trinta",  # string ao invés de int
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
        content_type='application/json'
    )

    assert resposta.status_code == 400
    resposta_json = resposta.get_json()
    assert 'erro' in resposta_json

# Teste de múltiplas requisições (simulando uso contínuo)


def test_predict_multiple_requests(client):
    dados = {
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
            content_type='application/json'
        )
        assert resposta.status_code == 200
        assert 'probabilidade_contratacao' in resposta.get_json()
