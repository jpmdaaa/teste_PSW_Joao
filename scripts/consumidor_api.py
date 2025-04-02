import requests
from typing import List, Dict
import json
from datetime import datetime
import logging

class ConsumidorAPICervejarias:
    URL_BASE = "https://api.openbrewerydb.org/v1/breweries"
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'PipelineCervejarias/1.0',
            'Accept': 'application/json'
        })
        
    def buscar_cervejarias(self, pagina: int = 1, por_pagina: int = 1) -> List[Dict]:
        """Busca cervejarias com controle de paginação"""
        try:
            params = {'page': pagina, 'per_page': por_pagina}
            response = self.session.get(self.URL_BASE, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Erro na requisição: {str(e)}")
            return []
    
    def buscar_todas_cervejarias(self, max_paginas: int = 20) -> List[Dict]:
        """Busca paginada de todas as cervejarias"""
        todas_cervejarias = []
        pagina = 1
        
        while pagina <= max_paginas:
            cervejarias = self.buscar_cervejarias(pagina=pagina)
            if not cervejarias:
                break
            todas_cervejarias.extend(cervejarias)
            pagina += 1
                
        return todas_cervejarias
    
    def salvar_camada_bronze(self, dados: List[Dict], caminho_saida: str) -> str:
        """Salva dados brutos na camada bronze"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"{caminho_saida}/cervejarias_{timestamp}.json"
            
            with open(nome_arquivo, 'w') as arquivo:
                json.dump(dados, arquivo)
                
            self.logger.info(f"Dados salvos em {nome_arquivo}")
            return nome_arquivo
        except Exception as e:
            self.logger.error(f"Erro ao salvar: {str(e)}")
            raise