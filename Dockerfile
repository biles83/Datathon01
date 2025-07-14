# Dockerfile
FROM python:3.10-slim

# Instalar dependências de sistema
RUN apt-get update && apt-get install -y \
    wget curl gnupg2 software-properties-common \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Instalar Prometheus
RUN mkdir /prometheus && \
    wget https://github.com/prometheus/prometheus/releases/download/v2.51.2/prometheus-2.51.2.linux-amd64.tar.gz && \
    tar xvfz prometheus-2.51.2.linux-amd64.tar.gz && \
    mv prometheus-2.51.2.linux-amd64/prometheus /bin/ && \
    rm -rf prometheus-2.51.2.linux-amd64*

# Instalar Grafana
#RUN wget https://dl.grafana.com/oss/release/grafana_10.4.2_amd64.deb && \
#    apt install -y ./grafana_10.4.2_amd64.deb && \
#    rm grafana_10.4.2_amd64.deb

# Diretório de trabalho e instalação de dependências Python
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia arquivos da aplicação e supervisord
COPY . /app
COPY supervisord.conf /etc/supervisord.conf
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 5000 8000 9090 3000
CMD ["/entrypoint.sh"]