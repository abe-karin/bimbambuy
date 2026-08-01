# Usa uma versão leve do Python
FROM python:3.9-slim

# Define o diretório de trabalho
WORKDIR /app

# 1. Instala dependências de sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    libheif-dev \
    build-essential \
    pkg-config \
    libffi-dev \
    poppler-utils \
    tesseract-ocr \
    tesseract-ocr-por \
    && rm -rf /var/lib/apt/lists/*

# 2. Instala o Torch separado (isso evita o erro de memória OOM)
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# 3. Copia o arquivo de requirements
COPY requirements.txt .

# 4. Instala TODO o restante de uma só vez
# Como o torch já está instalado, o pip vai pular ele e instalar o resto rapidamente
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copia o restante do código
COPY . .

# Define a porta
EXPOSE 5000

# Comando para iniciar
CMD ["python", "app.py"]