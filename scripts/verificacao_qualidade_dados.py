from pyspark.sql import DataFrame
from pyspark.sql.functions import col, count, when, length
from typing import Dict, Callable
import logging

class VerificacaoQualidadeDadosCervejaria:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def obter_verificacoes(self) -> Dict[str, Callable[[DataFrame], bool]]:
        """Retorna um dicionario com a qualidade dos dados"""
        return {
            'dataset_nao_vazio': self.verificar_dataset_nao_vazio,
            'campos_obrigatorios': self.verificar_campos_obrigatorios,
            'ids_sem_nulos': self.verificar_ids_sem_nulos,
            'tipos_cervejaria_validos': self.verificar_tipos_cervejaria_validos,
            'consistencia_pais_estado': self.verificar_consistencia_pais_estado
        }
    
    def verificar_dataset_nao_vazio(self, df: DataFrame) -> bool:
        """Verifica se o dataset n esta vazio"""
        count = df.count()
        self.logger.info(f"Contagem de linhas do dataset: {count}")
        return count > 0
    
    def verificar_campos_obrigatorios(self, df: DataFrame) -> bool:
        """Verifica se todos os campos estao presentes"""
        campos_obrigatorios = {'id', 'name', 'brewery_type', 'country'}
        campos_existentes = set(df.columns)
        campos_faltantes = campos_obrigatorios - campos_existentes
        
        if campos_faltantes:
            self.logger.warning(f"Campos obrigatórios faltando: {campos_faltantes}")
            return False
        return True
    
    def verificar_ids_sem_nulos(self, df: DataFrame) -> bool:
        """Verifica que n há IDs nulos"""
        ids_nulos = df.filter(col("id").isNull()).count()
        if ids_nulos > 0:
            self.logger.warning(f"Encontrados {ids_nulos} registros com IDs nulos")
            return False
        return True
    
    def verificar_tipos_cervejaria_validos(self, df: DataFrame) -> bool:
        """Verifica se os tipos de cervejaria sao valores permitidos"""
        valid_types = {
            'micro', 'nano', 'regional', 'brewpub', 
            'large', 'planning', 'bar', 'contract', 
            'proprietor', 'closed', 'unknown'
        }
        
        invalid_types_df = df.filter(
            ~col("brewery_type").isin(valid_types) & 
            col("brewery_type").isNotNull()
        )
        
        invalid_count = invalid_types_df.count()
        if invalid_count > 0:
            self.logger.warning(f"Encontrados {invalid_count} registros com tipos de cervejaria inválidos")
            return False
        return True
    
    def verificar_consistencia_pais_estado(self, df: DataFrame) -> bool:
        """Verifica se os codigos de estado dso validos para o país"""
        # Apenas para registros com país preenchido
        issues = df.filter(
            (col("country").isNotNull()) & 
            (
                (col("state").isNull()) | 
                (length(col("state")) != 2)
            )
        ).count()
        
        if issues > 0:
            self.logger.warning(f"Encontrados {issues} registros com problemas de estado/país")
            return False
        return True
    
    def executar_verificacoes(self, df: DataFrame) -> Dict[str, bool]:
        """Executa todas as verificacoes de qualidade e retorna resultados"""
        checks = self.obter_verificacoes()
        results = {}
        
        for check_name, check_func in checks.items():
            try:
                results[check_name] = check_func(df)
            except Exception as e:
                self.logger.error(f"Erro executando verificação {check_name}: {str(e)}")
                results[check_name] = False
                
        return results