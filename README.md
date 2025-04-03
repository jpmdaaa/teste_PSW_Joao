

# Pipeline de Dados para Cervejarias 🍺

Este projeto implementa um pipeline completo de dados que coleta informações de cervejarias da Open Brewery DB API, processa e armazena em um data lake seguindo a arquitetura bronze, prata, ouro, com interface gráfica para controle.

## 📋 Pré-requisitos

* Docker Desktop instalado
* Python 3.8+ (para execução local)
* 4GB+ de memória RAM disponível
* Conexão com internet para acessar a API
* Git (para clonar o repositório)

## 🏗️ Estrutura do Projeto

teste_PSW_jpm/
├── dados/
│ ├── bronze/ # Dados brutos da API
│ ├── prata/ # Dados processados
│ ├── ouro/ # Dados agregados
│ ├── resumo_prata.csv # Resumo estatístico
│ └── resumo_ouro.csv # Resumo analítico
├── docker/
│ ├── Dockerfile # Configuração do container
│ └── requirements.txt # Dependências do projeto
├── scripts/
│ ├── consumidor_api.py # Coleta de dados da API
│ ├── transformacao.py # Transformações de dados
│ ├── verificacao_qualidade_dados.py # Validação de dados
│ └── monitoramento.py # Monitoramento do pipeline
├── testes/
│ ├── test_consumidor_api.py # Testes da API
│ ├── test_transformacao.py # Testes de transformação
│ ├── test_verificacao_qualidade.py # Testes de qualidade
│ └── test_monitoramento.py # Testes de monitoramento
├── dags/
│ └── cervejarias_pipeline.py # Pipeline Airflow
├── executar_pipeline.py # Script principal
├── interface_pipeline.py # Interface gráfica
├── visualizar_dados.py # Visualização de resultados
└── README.md

## 🚀 Como Executar

### Opção 1: Via Docker (Recomendado para produção)

1. **Construir a imagem Docker**:
```powershell
docker build -t pipeline-cervejarias -f docker/Dockerfile .

2. **Executar o pipeline completo** :

powershell

docker run -it --rm -v ${PWD}/dados:/dados pipeline-cervejarias python3 executar_pipeline.py

3. **Abrir a interface gráfica** :

powershell

python interface_pipeline.py

### Opção 2: Execução com Airflow (Para orquestração)

1. **Iniciar os containers** :

powershell

docker-compose up -d

2. **Acessar a interface do Airflow** :
   Acesse `http://localhost:8080` no navegador (usuário: admin, senha: admin)
3. **Ativar o DAG** :
   Na interface do Airflow, ative o DAG `cervejarias_pipeline` que será executado diariamente

### Opção 3: Execução Local (Para desenvolvimento)

1. **Configurar ambiente virtual** :

powershell

python -m venv venv
.\venv\Scripts\activate
pip install -r docker/requirements.txt

2. **Executar o pipeline** :

powershell

python executar_pipeline.py

3. **Abrir a interface gráfica** :

powershell

python interface_pipeline.py


## 🖥️ Interface Gráfica

A interface Tkinter fornece controle completo sobre o pipeline

Funcionalidades:

* Execução individual de cada etapa do pipeline
* Visualização em tempo real dos logs
* Controle de processos
* Exibição de resultados

## 📊 Visualização de Dados

Após executar o pipeline, você pode:

1. Ver os arquivos CSV gerados:
   * `dados/resumo_prata.csv` (dados processados)
   * `dados/resumo_ouro.csv` (dados agregados)
2. Visualizar os gráficos gerados:
   * `dados/grafico_paises_prata.png`
   * `dados/grafico_paises_ouro.png`
3. Usar o visualizador integrado:

powershell

python visualizar_dados.py

## 🧪 Testes

Execute todos os testes com:

powershell

python -m pytest testes/

Ou testes individuais:

powershell

python -m pytest testes/test_consumidor_api.py -v

## 📝 Personalização

Principais pontos de configuração:

| Arquivo                            | Propósito                            |
| ---------------------------------- | ------------------------------------- |
| `executar_pipeline.py`           | Configuração geral do pipeline      |
| `verificacao_qualidade_dados.py` | Regras de validação de dados        |
| `transformacao.py`               | Lógica de transformação dos dados  |
| `monitoramento.py`               | Configuração de alertas e métricas |

## 📈 Fluxo de Dados

1. **Bronze** : Coleta bruta da API → JSON
2. **Prata** : Limpeza e validação → Parquet
3. **Ouro** : Agregação e análise → CSV/Parquet
