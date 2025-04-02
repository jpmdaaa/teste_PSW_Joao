from scripts.consumidor_api import ConsumidorAPICervejarias
from unittest.mock import patch, MagicMock
import unittest
import requests

class TestConsumidorAPI(unittest.TestCase):
    @patch('requests.Session.get')
    def test_buscar_cervejarias_sucesso(self, mock_get):
        """Testa busca bem-sucedida com dados mockados"""
        # Configura mock
        mock_resposta = MagicMock()
        mock_resposta.json.return_value = [{
            "id": "1", 
            "name": "Cervejaria Teste",
            "country": "Brazil"
        }]
        mock_resposta.raise_for_status.return_value = None
        mock_get.return_value = mock_resposta
        
        # Testa
        consumidor = ConsumidorAPICervejarias()
        resultado = consumidor.buscar_cervejarias(por_pagina=1)
        
        # Verifica
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]["name"], "Cervejaria Teste")

    @patch('requests.Session.get')
    def test_buscar_cervejarias_erro(self, mock_get):
        """Testa tratamento de erro na API"""
        # Configura mock para simular erro
        mock_get.side_effect = requests.exceptions.RequestException("Erro simulado")
        
        # Testa
        consumidor = ConsumidorAPICervejarias()
        resultado = consumidor.buscar_cervejarias()
        
        # Verifica se retorna lista vazia
        self.assertEqual(resultado, [])

    @patch('requests.Session.get')
    def test_buscar_cervejarias_brasil(self, mock_get):
        """Testa especificamente dados brasileiros"""
        # Configura mock com dados BR e Brazil
        mock_resposta = MagicMock()
        mock_resposta.json.return_value = [
            {"id": "b1", "name": "Ambev", "country": "Brazil"},
            {"id": "b2", "name": "Bohemia", "country": "BR"}
        ]
        mock_get.return_value = mock_resposta
        
        # Testa
        consumidor = ConsumidorAPICervejarias()
        resultado = consumidor.buscar_cervejarias()
        
        # Verifica
        self.assertEqual(len(resultado), 2)
        self.assertTrue(any(c["country"] == "Brazil" for c in resultado))

    @patch('requests.Session.get')
    def test_buscar_todas_cervejarias(self, mock_get):
        """Testa paginação completa"""
        # Configura mock para simular 3 páginas
        mock_get.side_effect = [
            MagicMock(json=MagicMock(return_value=[{"id": str(i)} for i in range(20)]), 
                    raise_for_status=MagicMock(return_value=None)),
            MagicMock(json=MagicMock(return_value=[{"id": str(i)} for i in range(20,40)]), 
                    raise_for_status=MagicMock(return_value=None)),
            MagicMock(json=MagicMock(return_value=[]),  # Página vazia para encerrar
                    raise_for_status=MagicMock(return_value=None))
        ]
        
        consumidor = ConsumidorAPICervejarias()
        resultado = consumidor.buscar_todas_cervejarias(max_paginas=3)
        
        self.assertEqual(len(resultado), 40)

if __name__ == '__main__':
    unittest.main()