# scripts/transformacao.py
from pyspark.sql import DataFrame
import pyspark.sql.functions as F

class TransformadorCervejarias:
    def __init__(self):
        """Inicializa o transformador com configuracoes padrao"""
        self.paises_brasileiros = ["br", "brasil", "brazil"]
        self.tipos_validos = ["micro", "nano", "regional", "brewpub"]
    
    def padronizar_paises(self, df):
        """
        Padroniza os nomes de paises, especialmente variantes do Brasil
        """
        return df.withColumn(
            "country",
            F.when(
                F.lower(F.col("country")).isin(self.paises_brasileiros),
                F.lit("Brazil")
            ).otherwise(F.col("country"))
        )
    
    def tratar_tipos_cervejaria(self, df):
        """
        Padroniza os tipos de cervejaria
        """
        return df.withColumn(
            "brewery_type",
            F.when(
                F.col("brewery_type").isin(self.tipos_validos),
                F.col("brewery_type")
            ).otherwise(F.lit("desconhecido"))
        )
    
    def transformar(self, df):
        """
        Executa todas as transformacoes em sequencia
        """
        df = self.padronizar_paises(df)
        df = self.tratar_tipos_cervejaria(df)
        return df