from scripts.verificacao_qualidade_dados import VerificacaoQualidadeDadosCervejaria
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType
import pyspark.sql.functions as F
import unittest

class TestVerificacaoQualidade(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spark = SparkSession.builder \
            .appName("TestesQualidade") \
            .getOrCreate()
        
        cls.esquema = StructType([
            StructField("id", StringType(), nullable=False),
            StructField("name", StringType(), nullable=True),
            StructField("brewery_type", StringType(), nullable=True),
            StructField("country", StringType(), nullable=True),
            StructField("state", StringType(), nullable=True)
        ])
    
    def test_verificacao_brasil(self):
        """Testa verificacao especifica para dados brasileiros"""
        dados = [
            ("1", "Cervejaria A", "micro", "Brazil", "SP"),  
            ("2", "Cervejaria B", None, "BR", "California"),  
            ("3", "Cervejaria C", "nano", "Brasil", None)  
        ]
        df = self.spark.createDataFrame(dados, schema=self.esquema)
        
        verificador = VerificacaoQualidadeDadosCervejaria()
        resultados = verificador.executar_verificacoes(df)
        
        # Verifica resultados especificos para Brasil
        self.assertTrue(resultados['dataset_nao_vazio'])
        self.assertGreater(resultados['nulos_por_pais']['Brazil'], 0)
        self.assertIn('estados_invalidos', resultados)
        self.assertIn('California', str(resultados['estados_invalidos']))

if __name__ == '__main__':
    unittest.main()