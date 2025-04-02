from scripts.consumidor_api import ConsumidorAPICervejarias
from unittest.mock import patch, MagicMock
import unittest

class TestConsumidorAPI(unittest.TestCase):
    @patch('requests.get')
    def test_buscar_cervejarias_sucesso(self, mock_get):
        # Configurar mock
        mock_resposta = MagicMock()
        mock_resposta.json.return_value = [{"id": "1", "name": "Cervejaria Teste"}]
        mock_resposta.raise_for_status.return_value = None
        mock_get.return_value = mock_resposta
        
        # Testar
        consumidor = ConsumidorAPICervejarias()
        resultado = consumidor.buscar_cervejarias()
        
        # Verificar
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]["name"], "Cervejaria Teste")
        
    @patch('requests.get')
    def test_buscar_cervejarias_erro(self, mock_get):
        # Configurar para lancar excecao
        mock_get.side_effect = Exception("Erro de API")
        
        # Testar
        consumidor = ConsumidorAPICervejarias()
        with self.assertRaises(Exception):
            consumidor.buscar_cervejarias()

if __name__ == '__main__':
    unittest.main()