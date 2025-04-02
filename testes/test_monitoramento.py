from scripts.monitoramento import MonitoramentoPipeline
from pyspark.sql import SparkSession
import unittest
from datetime import datetime
from unittest.mock import patch
import logging

class TestMonitorPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spark = SparkSession.builder \
            .master("local[1]") \
            .appName("TestesMonitoramento") \
            .getOrCreate()
        
        # Configurar logging para testes
        logging.basicConfig(level=logging.INFO)
        cls.logger = logging.getLogger('monitoramento_pipeline')

    def setUp(self):
        """Reinicia as métricas antes de cada teste"""
        self.monitor = MonitoramentoPipeline()

    def test_registrar_processados(self):
        """Testa registro de registros processados"""
        self.monitor.registrar_processados(100)
        self.assertEqual(self.monitor.metricas['registros_processados'], 100)
        
        self.monitor.registrar_processados(50)
        self.assertEqual(self.monitor.metricas['registros_processados'], 150)

    def test_registrar_sucesso(self):
        """Testa registro de execução bem sucedida"""
        before = datetime.now()
        self.monitor.registrar_sucesso()
        after = datetime.now()
        
        ultima_execucao = self.monitor.metricas['ultima_execucao_bem_sucedida']
        self.assertIsNotNone(ultima_execucao)
        self.assertTrue(before <= ultima_execucao <= after)

    def test_registrar_erro(self):
        """Testa registro de erros"""
        try:
            1/0
        except Exception as e:
            self.monitor.registrar_erro(e, "Teste de divisão por zero")
        
        self.assertEqual(len(self.monitor.metricas['erros']), 1)
        erro = self.monitor.metricas['erros'][0]
        self.assertEqual(erro['tipo'], 'ZeroDivisionError')
        self.assertIn("division by zero", erro['erro'])
        self.assertEqual(erro['contexto'], "Teste de divisão por zero")

    @patch('logging.Logger.error')
    def test_enviar_alerta_erro(self, mock_log):
        """Testa envio de alertas de erro"""
        alerta = self.monitor.enviar_alerta("Erro crítico", nivel='erro')
        
        self.assertEqual(alerta['nivel'], 'erro')
        self.assertEqual(alerta['mensagem'], "Erro crítico")
        self.assertEqual(len(self.monitor.metricas['alertas']), 1)
        mock_log.assert_called_once_with("ALERTA: Erro crítico")

    @patch('logging.Logger.warning')
    def test_enviar_alerta_aviso(self, mock_log):
        """Testa envio de alertas de aviso"""
        contexto = {'detalhes': 'Valor aproximado'}
        alerta = self.monitor.enviar_alerta("Aviso importante", nivel='aviso', contexto=contexto)
        
        self.assertEqual(alerta['nivel'], 'aviso')
        self.assertEqual(alerta['mensagem'], "Aviso importante")
        self.assertEqual(alerta['contexto'], contexto)
        mock_log.assert_called_once_with("ALERTA: Aviso importante")

    def test_obter_metricas(self):
        """Testa obtenção de métricas completas"""
        self.monitor.registrar_processados(10)
        self.monitor.registrar_sucesso()
        
        metricas = self.monitor.obter_metricas()
        self.assertEqual(metricas['registros_processados'], 10)
        self.assertIsNotNone(metricas['ultima_execucao_bem_sucedida'])
        self.assertEqual(len(metricas['erros']), 0)
        self.assertEqual(len(metricas['alertas']), 0)

if __name__ == '__main__':
    unittest.main()