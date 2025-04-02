import os
import sys
os.environ['PYSPARK_PYTHON'] = 'python'
os.environ['PYSPARK_DRIVER_PYTHON'] = 'python'

# Adiciona o diretório raiz ao PATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.transformacao import TransformadorCervejarias
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import unittest

class TestTransformadorCervejarias(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spark = SparkSession.builder \
            .master("local[1]") \
            .appName("TestesTransformacao") \
            .config("spark.executor.memory", "1g") \
            .config("spark.driver.memory", "1g") \
            .getOrCreate()

    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()

    def test_padronizar_paises(self):
        """Testa a padronizacao de nomes de paises"""
        dados = [
            ("b1", "Brazil"),
            ("b2", "BR"),
            ("b3", "Brasil"),
            ("b4", "United States")
        ]
        df = self.criar_dataframe(dados, ["id", "country"])
        
        transformador = TransformadorCervejarias()
        df_transformado = transformador.padronizar_paises(df)
        
        # Coleta os resultados para evitar operações distribuídas nos testes
        resultados = df_transformado.collect()
        brasil_count = sum(1 for row in resultados if row["country"] == "Brazil")
        self.assertEqual(brasil_count, 3)

    def test_tratar_tipos_cervejaria(self):
        """Testa o tratamento de tipos de cervejaria"""
        dados = [
            ("b1", "micro"),
            ("b2", None),
            ("b3", "nano"),
            ("b4", "invalid_type")
        ]
        df = self.criar_dataframe(dados, ["id", "brewery_type"])
        
        transformador = TransformadorCervejarias()
        df_transformado = transformador.tratar_tipos_cervejaria(df)
        
        # Coleta os resultados para evitar operações distribuídas nos testes
        resultados = df_transformado.collect()
        desconhecidos = sum(1 for row in resultados if row["brewery_type"] == "desconhecido")
        self.assertEqual(desconhecidos, 2)

    def criar_dataframe(self, dados, colunas):
        """Helper para criar DataFrames de teste"""
        return self.spark.createDataFrame(dados, colunas)

if __name__ == '__main__':
    unittest.main()