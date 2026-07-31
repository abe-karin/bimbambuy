# Usa uma versão leve do Python
FROM python:3.9-slim

# Define o diretório de trabalho
WORKDIR /app

# 1. Atualiza e instala as bibliotecas de sistema necessárias (libheif e compiladores)
# O --no-install-recommends ajuda a manter a imagem menor
RUN apt-get update && apt-get install -y --no-install-recommends \
    libheif-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de dependências
COPY requirements.txt .

# Instala as dependências (agora que as bibliotecas de sistema existem, vai funcionar!)
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o resto do código
COPY . .

# Define a porta
EXPOSE 5000

# Comando para iniciar
CMD ["python", "app.py"]