# Pipeline de Dados para Cervejarias

Este projeto implementa um pipeline de dados que coleta informações de cervejarias da Open Brewery DB API, processa e armazena em um data lake seguindo a arquitetura bronze, prata, ouro.

## Pré-requisitos

* Docker Desktop instalado
* 4GB+ de memória RAM disponível
* Conexão com internet para acessar a API

## Estrutura do Projeto

teste_PSW_jpm/
├── docker/
│   ├── Dockerfile
│   └── requirements.txt
├── scripts/
│   ├── consumidor_api.py
│   ├── verificacao_qualidade_dados.py
│   └── monitoramento.py
├── dados/
└── executar_pipeline.py

## Como Executar

1. **Construir a imagem Docker** :

Abra um terminal Powershell:

Copydocker build -t pipeline-cervejarias -f docker/Dockerfile .

2. **Executar o pipeline completo** :

docker run -it --rm -v ${PWD}/dados:/dados pipeline-cervejarias python3 executar_pipeline.py

3. **Verificar os resultados** :

ls .\dados\

# bronze/    - Dados brutos da API

# prata/     - Dados processados

# ouro/      - Dados agregados



## Como Acessar e Visualizar os Dados

Abra um terminal Powershell:

execute: python visualizar_dados.py 


## Monitoramento

O pipeline gera logs em tempo real com informações sobre:

* Coleta de dados
* Problemas de qualidade
* Estatísticas de processamento

## Personalização

Você pode modificar:

* Número de páginas da API (em `executar_pipeline.py`)
* Regras de qualidade (em `verificacao_qualidade_dados.py`)
* Estrutura de saída (em `executar_pipeline.py`)
