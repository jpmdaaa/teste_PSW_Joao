from scripts.verificacao_qualidade_dados import VerificacaoQualidadeDadosCervejaria
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType
import unittest

class TestVerificacaoQualidade(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spark = SparkSession.builder \
            .appName("TestesQualidade") \
            .getOrCreate()
        
        cls.esquema = StructType([
            StructField("id", StringType(), nullable=False),
            StructField("nome", StringType(), nullable=True),
            StructField("brewery_type", StringType(), nullable=True),
            StructField("country", StringType(), nullable=True),
            StructField("state", StringType(), nullable=True)
        ])
    
    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()
    
    def criar_df_teste(self, dados):
        return self.spark.createDataFrame(dados, schema=self.esquema)
    
    def test_dataset_nao_vazio(self):
        verificador = VerificacaoQualidadeDadosCervejaria()
        
        # Testar dataset vazio
        df_vazio = self.criar_df_teste([])
        self.assertFalse(verificador.verificar_dataset_nao_vazio(df_vazio))
        
        # Testar dataset não vazio
        dados_teste = [("1", "Cervejaria A", "micro", "BR", "SP")]
        df_teste = self.criar_df_teste(dados_teste)
        self.assertTrue(verificador.verificar_dataset_nao_vazio(df_teste))

if __name__ == '__main__':
    unittest.main()