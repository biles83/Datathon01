# Imagem base com Python
FROM python:3.10-slim

# Diretório de trabalho dentro do container
WORKDIR /app

# Copiar arquivos necessários
COPY requirements.txt .
COPY app.py .
COPY modelo_contratacao.pkl .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta da API
EXPOSE 5000

# Comando para iniciar a API
CMD ["python", "app.py"]