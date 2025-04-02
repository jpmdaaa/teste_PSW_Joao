FROM databricksruntime/standard:latest

# Instalar pip e dependencias 
RUN apt-get update && \
    apt-get install -y python3-pip && \
    pip3 install --upgrade pip

WORKDIR /app

COPY docker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY scripts/ ./scripts/
COPY notebooks/ ./notebooks/
COPY testes/ ./testes/
COPY executar_pipeline.py .

CMD ["python3", "-m", "unittest", "discover", "-s", "testes"]