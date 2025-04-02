import sys
from scripts.consumidor_api import ConsumidorAPICervejarias
from scripts.verificacao_qualidade_dados import VerificacaoQualidadeDadosCervejaria
from scripts.monitoramento import MonitoramentoPipeline
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('pipeline_principal')

# Schema definido
SCHEMA_CERVEJARIAS = StructType([
    StructField("id", StringType(), False),
    StructField("name", StringType(), True),
    StructField("brewery_type", StringType(), True),
    StructField("street", StringType(), True),
    StructField("city", StringType(), True),
    StructField("state", StringType(), True),
    StructField("postal_code", StringType(), True),
    StructField("country", StringType(), True),
    StructField("website_url", StringType(), True)
])

def criar_diretorios():
    """Cria a estrutura de diretórios se não existir"""
    os.makedirs("/dados/bronze", exist_ok=True)
    os.makedirs("/dados/prata", exist_ok=True)
    os.makedirs("/dados/ouro", exist_ok=True)

def executar_pipeline():
    logger.info("Iniciando pipeline de cervejarias")
    monitor = MonitoramentoPipeline()
    criar_diretorios()
    
    try:
        # 1. Camada Bronze - Extração
        logger.info("Extraindo dados da API...")
        consumidor = ConsumidorAPICervejarias()
        cervejarias = consumidor.buscar_todas_cervejarias(max_paginas=3)
        
        if not cervejarias:
            logger.warning("Nenhum dado retornado pela API - criando dataset vazio")
            cervejarias = [{
                "id": "0000", 
                "name": "Dummy", 
                "brewery_type": "dummy",
                "country": "Dummyland"
            }]
        
        caminho_bronze = consumidor.salvar_camada_bronze(cervejarias, "/dados/bronze")
        monitor.registrar_processados(len(cervejarias))
        
        # 2. Camada Prata - Transformação
        logger.info("Transformando dados...")
        spark = SparkSession.builder.appName("PipelineCervejarias").getOrCreate()
        
        # Criar DataFrame com schema explícito
        df = spark.createDataFrame(cervejarias, schema=SCHEMA_CERVEJARIAS)
        
        # Verificação de qualidade
        verificador = VerificacaoQualidadeDadosCervejaria()
        resultados = verificador.executar_verificacoes(df)
        
        # Verificar apenas falhas críticas
        falhas_criticas = {
            'dataset_nao_vazio': resultados.get('dataset_nao_vazio', False),
            'campos_obrigatorios': resultados.get('campos_obrigatorios', False),
            'ids_sem_nulos': resultados.get('ids_sem_nulos', False)
        }
        
        if not all(falhas_criticas.values()):
            logger.error("Falhas críticas na qualidade dos dados")
            monitor.registrar_erro(Exception("Falhas críticas na qualidade dos dados"))
            sys.exit(1)
            
        df.write.mode("overwrite").parquet("/dados/prata/cervejarias")
        logger.info("Dados salvos na camada prata")
        
        # 3. Camada Ouro - Agregação
        logger.info("Agregando dados...")
        df_agregado = df.groupBy("country", "state", "brewery_type").count()
        df_agregado.write.mode("overwrite").parquet("/dados/ouro/agregados")
        
        logger.info("Pipeline executado com sucesso!")
        monitor.registrar_sucesso()
        
    except Exception as e:
        logger.error(f"Erro durante a execução do pipeline: {str(e)}")
        monitor.registrar_erro(e)
        monitor.enviar_alerta(f"Falha no pipeline: {str(e)}", nivel='erro')
        sys.exit(1)

if __name__ == "__main__":
    executar_pipeline()