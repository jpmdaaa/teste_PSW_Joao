import logging
from typing import Dict, Any, Callable, Optional
from datetime import datetime
from pyspark.sql import DataFrame

class MonitoramentoPipeline:
    def __init__(self):
        """Inicializa o sistema de monitoramento"""
        self.logger = logging.getLogger('monitoramento_pipeline')
        self.metricas: Dict[str, Any] = {
            'registros_processados': 0,
            'ultima_execucao_bem_sucedida': None,
            'erros': [],
            'alertas': []
        }
        
    def registrar_processados(self, quantidade: int) -> None:
        """Registra a quantidade de registros processados"""
        self.metricas['registros_processados'] += quantidade
        self.logger.info(f"Registrados {quantidade} registros processados")
        
    def registrar_sucesso(self) -> None:
        """Registra uma execucao bem sucedida"""
        self.metricas['ultima_execucao_bem_sucedida'] = datetime.now()
        self.logger.info("Pipeline executado com sucesso")
        
    def registrar_erro(self, erro: Exception, contexto: Optional[str] = None) -> None:
        """Registra um erro ocorrido"""
        entrada_erro = {
            'timestamp': datetime.now(),
            'erro': str(erro),
            'contexto': contexto,
            'tipo': type(erro).__name__
        }
        self.metricas['erros'].append(entrada_erro)
        self.logger.error(f"Erro registrado: {str(erro)} | Contexto: {contexto}")
        
    def enviar_alerta(
        self, 
        mensagem: str, 
        nivel: str = 'erro',
        contexto: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
      
        if nivel not in ['erro', 'aviso']:
            nivel = 'erro'
            
        alerta = {
            'timestamp': datetime.now(),
            'nivel': nivel,
            'mensagem': mensagem,
            'contexto': contexto or {}
        }
        
        self.metricas['alertas'].append(alerta)
        
        if nivel == 'erro':
            self.logger.error(f"ALERTA: {mensagem}")
        else:
            self.logger.warning(f"ALERTA: {mensagem}")
            
        return alerta
    
    def obter_metricas(self) -> Dict[str, Any]:
        """Retorna todas as métricas coletadas"""
        return self.metricas