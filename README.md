## Score de Probabilidade de Contratação

🔍 O que é?
Modelo preditivo supervisionado que estima a probabilidade de um candidato ser contratado, com base em dados históricos de vagas e seleções anteriores.

🧠 Modelo preditivo supervisionado.
Regressão logística.

🎯 Problema que resolve:
O time de recrutamento perde muito tempo avaliando candidatos que dificilmente seriam contratados — seja por desalinhamento técnico, salarial ou outros motivos.
Este modelo ajuda a priorizar candidatos com mais chances reais de contratação, focando energia nos mais promissores.

⚙️ Como funciona:
Usa os dados dos candidatos (applicants.json), das vagas (vagas.json) e da prospecção (prospects.json).
Para cada candidato de uma vaga, o modelo aprende quais características estavam mais presentes nos que foram contratados.

🧩 Variáveis de entrada (features):
•	Idade do candidato
•	Tempo de experiência
•	Nível de senioridade (nivel_profissional)
•	Nível acadêmico
•	Nível de inglês
•	Nível de espanhol
•	Certificações

📌 Variável target (saída):
Se o candidato foi contratado ou não.

🎯 Resultado:
- Um score entre 0 e 1 para cada prospect indicando a probabilidade de ser contratado.
- Previsão: 1 (contratação) ou 0 (não contratação).

## Requisitos do Projeto - DATATHON
• Treinamento do modelo preditivo: Treinamento realizado no fonte train_model.py ou Datathon.ipynb.
• Crie uma API para deployment do modelo: API criada em app.py.
• Realize o empacotamento do modelo com Docker: Empacotamento Docker realizado.
• Deploy do modelo: Deploy realizado na AWS.
• Teste da API: Teste realizado com Postman.
• Testes unitários: Teste unitário da API incluído no fonte test_api.py.
• Monitoramento Contínuo: Logs e monitoramento com Prometheus e Grafana.

## ⚠️ Cobertura de testes unitários (test_api.py)
•	test_predict_success: fluxo principal
•	test_predict_missing_fields: campos ausentes
•	test_predict_invalid_type: tipo incorreto
•	test_predict_multiple_requests: uso contínuo

## 📘 Documentação da API
Esta API Flask serve um modelo de machine learning treinado para prever a probabilidade de contratação de candidatos com base em informações fornecidas.

•	Autenticação
Esta API não possui autenticação.

•	Endpoints
- GET /
  Verifica se a API está ativa.
  Exemplo de resposta: 
    ✅ API de Previsão de Contratação está rodando.
- POST /predict
  Recebe os dados do candidato e retorna a probabilidade de contratação e a classe (0 ou 1).
  Exemplo de requisição:
    {
      "idade": 30,
      "tempo_experiencia": 5,
      "nivel_profissional": "Pleno",
      "nivel_academico": "Graduacao",
      "nivel_ingles": "Intermediario",
      "nivel_espanhol": "Basico",
      "certificacoes": 2
    }
  Exemplo de resposta:
    {
      "probabilidade_contratacao": 0.7821,
      "previsao": 1
    }

•	Possíveis erros
- 400 Bad Request: Dados ausentes ou com tipos inválidos.
- 500 Internal Server Error: Erro inesperado no servidor.

•	 Monitoramento com Prometheus
A API expõe métricas para consumo pelo Prometheus.
Métricas:
request_processing_seconds - Tempo de resposta por requisição.
prediction_requests_total	- Número total de requisições de predição.
prediction_errors_total	-	Número total de erros nas predições.
last_prediction_value	-	Último valor de probabilidade predito.
prediction_drift_score	-	Desvio médio em relação à média do dataset de treinamento.

## 📁 Estrutura do Projeto
```bash
DATATHON01/
  ├── tests/
  │   └── test_api.py
  ├── bases/
  │   └── arquivos json
  ├── __init__.py
  ├── .gitignore
  ├── app.py
  ├── Datathon.ipynb
  ├── docker-compose.yml
  ├── Dockerfile
  ├── entrypoint.sh
  ├── modelo_contratacao.pkl
  ├── prometheus.yml  
  ├── README.md
  ├── requirements.txt
  ├── supervisord.conf
  └── train_model.py
```

- **`DATATHON01/`**: Diretório principal do aplicativo.
- **`tests/`**: Diretório com os fontes para teste unitário.
- **`test_api.py`**: Teste unitário da API.
- **`bases/`**: Diretório com as bases para treinamento.
- **`.gitignore`**: Tipos ignorados pelo GITHUB.
- **`app.py`**: Fonte para rodar a API.
- **`Datathon.ipynb`**: Execução dos testes e modelo no formato notebook.
- **`docker-compose.yml`**: Orquestra múltiplos containers (Flask + Prometheus + Grafana).
- **`Dockerfile`**: Define como construir a imagem do container da sua aplicação.
- **`entrypoint.sh`**: Script que roda assim que o container sobe.
- **`modelo_contratacao.pkl`**: Modelo Exportado.
- **`prometheus.yml `**: Configura as fontes de métricas que o Prometheus vai monitorar.
- **`README.md`**: Documentação do projeto.
- **`requirements.txt`**: Lista de dependências do projeto.
- **`supervisord.conf`**: Define como o supervisord vai gerenciar processos dentro do container.
- **`train_model.py`**: Fonte para treinamento e geração do modelo preditivo.

## 🛠️ Como Executar o Projeto Localmente
Passos para execução do projeto em ambiente local.

### 1. Clone o Repositório
```bash
git clone https://github.com/biles83/Datathon01
```
### 2. Crie um Ambiente Virtual
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```
### 3. Instale as Dependências
```bash
pip install -r requirements.txt
```
### 4. Construa a Imagem Docker
```bash
docker-compose up --build
```
### 5. Testes Unitários
```bash
python -m pytest tests/
```
### 6. Sites
Métricas      =>   http://localhost:8000/metrics
API           =>   http://localhost:5000
API           =>   http://localhost:5000/predict
Prometheus    =>   http://localhost:9090/
Grafana       =>   http://localhost:3300/

## 🛠️ Deploy em nuvem AWS - EC2
Passos pararealizar o deploy em nuvem AWS.

1. Criar Instância EC2 na AWS.
Tipo: t2.micro
SO: Ubuntu 22.04 LTS
Baixe o arquivo .pem para conectar via SSH.
2. Conectar no EC2 via SSH.
```bash
ssh -i chave.pem ubuntu@SEU_IP_PUBLICO
```
3. Instalar Docker e Docker Compose.
```bash
sudo apt update
sudo apt install -y docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
```
4. Subir o código do projeto (GIT).
```bash
sudo apt install git -y
git clone https://github.com/biles83/Datathon01.git
cd Datathon01
```
5. Rodar aplicação com Docker Compose.
```bash
docker-compose up --build -d
```
6. Acessar na Web (usando IP público da EC2)
API =>             http://SEU_IP_PUBLICO:5000
API_PPREDICAO =>   http://SEU_IP_PUBLICO:5000/PREDICT
Prometheus =>	     http://SEU_IP_PUBLICO:9090
Métricas =>	       http://SEU_IP_PUBLICO:8000/metrics
Grafana	=>         http://SEU_IP_PUBLICO:3300

## ⚙️ Configurar com systemd (não obrigatório)
Configurar a API para subir automaticamente quando iniciar a VM.

1. Crie o arquivo do serviço
```bash
sudo nano /etc/systemd/system/app-contratacao.service
```
2. Cole o conteúdo abaixo:
[Unit]
Description=Serviço para subir aplicação Flask + Prometheus + Grafana com Docker Compose
After=network.target docker.service
Requires=docker.service
[Service]
Type=oneshot
WorkingDirectory=/home/ubuntu/Datathon01
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
RemainAfterExit=yes
TimeoutStartSec=0
[Install]
WantedBy=multi-user.target
3. Dê permissão para o serviço
```bash
sudo chmod 644 /etc/systemd/system/app-contratacao.service
```
4. Recarregue o systemd
```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
```
5. Inicie e habilite o serviço
```bash
sudo systemctl start app-contratacao
sudo systemctl enable app-contratacao
```
6. Comandos úteis
Iniciar serviço	               -   sudo systemctl start app-contratacao
Parar serviço	                 -   sudo systemctl stop app-contratacao
Ver status	                   -   sudo systemctl status app-contratacao
Habilitar na inicialização	   -   sudo systemctl enable app-contratacao
Desabilitar na inicialização   -   sudo systemctl disable app-contratacao
Ver logs                       -   journalctl -u app-contratacao -f

## 🚀 Deploy de atualizações contínuas
1. Acesse a instância via SSH
```bash
ssh -i chave.pem ubuntu@SEU_IP_PUBLICO
```
2. Entre na pasta do projeto
```bash
cd Datathon01
```
3. Atualize o código com Git
```bash
git pull origin main  # ou branch que estiver usando
```
4. Reconstrua e reinicie os containers
```bash
docker-compose down   # Para parar e remover os containers antigos
docker-compose up --build -d   # Reconstrói e sobe em background
```

## 📖 Documentação do Projeto
A documentação do projeto encontra-se distribuída em 2 arquivos conforme mostrado abaixo.
- **`README.md`**: Documentação do projeto.
```bash
DATATHON01/
  └── README.md
```

## 🤝 Contribuindo
1. Fork este repositório.
2. Crie sua branch (`git checkout -b feature/nova-funcionalidade`).
3. Faça commit das suas alterações (`git commit -m 'Adiciona nova funcionalidade'`).
4. Faça push para sua branch (`git push origin feature/nova-funcionalidade`).
5. Abra um Pull Request.
instalar, configurar e usar o projeto. Ele também cobre contribuições, contato, licença e agradecimentos, tornando-o completo e fácil de entender para novos desenvolvedores.