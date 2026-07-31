# Usa uma versão leve do Python
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências primeiro (otimiza o build)
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o resto do código da sua pasta para o container
COPY . .

# Define a porta que o Flask usa
EXPOSE 5000

# Comando para iniciar o seu app
CMD ["python", "app.py"]