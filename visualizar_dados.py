import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

# Configurações dos caminhos (Windows/Docker compatible)
BASE_DIR = Path(__file__).parent / "dados"
CAMADAS = {
    "bronze": BASE_DIR / "bronze",
    "prata": BASE_DIR / "prata" / "cervejarias",
    "ouro": BASE_DIR / "ouro" / "agregados"
}

def carregar_dados(caminho):
    """Carrega dados Parquet, suportando particionamento"""
    try:
        return pd.read_parquet(caminho, engine='pyarrow')
    except Exception as e:
        print(f"Erro ao carregar {caminho}: {str(e)}")
        return None

def visualizar_camada(df, nome_camada):
    """Exibe resumo dos dados"""
    if df is not None:
        print(f"\n=== {nome_camada.upper()} ===")
        print(f"Total de registros: {len(df)}")
        print("\nAmostra (5 primeiros):")
        print(df.head())
        
        # Salva CSV e gráficos
        salvar_analises(df, nome_camada)
    else:
        print(f"\n⚠️ Camada {nome_camada} vazia ou não encontrada")

def salvar_analises(df, camada):
    """Gera arquivos de análise"""
    # CSV resumido
    csv_path = BASE_DIR / f"resumo_{camada}.csv"
    df.sample(min(20, len(df))).to_csv(csv_path, index=False)
    print(f"📊 CSV resumido salvo em: {csv_path}")
    
    # Gráficos (se houver colunas relevantes)
    if 'country' in df.columns:
        plt.figure(figsize=(10,5))
        df['country'].value_counts().plot(kind='bar', title=f'Cervejarias por País ({camada})')
        plt.tight_layout()
        plt.savefig(BASE_DIR / f"grafico_paises_{camada}.png")
        print(f"📈 Gráfico salvo em: {BASE_DIR}/grafico_paises_{camada}.png")

def main():
    print("\n🔍 Visualizador do Pipeline de Cervejarias")
    
    # Carrega e exibe ambas as camadas
    df_prata = carregar_dados(CAMADAS["prata"])
    df_ouro = carregar_dados(CAMADAS["ouro"])
    
    visualizar_camada(df_prata, "prata")
    visualizar_camada(df_ouro, "ouro")
    
    # Comparação entre camadas
    if df_prata is not None and df_ouro is not None:
        print("\n=== COMPARAÇÃO ===")
        print(f"Prata → Ouro: {len(df_prata)} → {len(df_ouro)} registros")
        print("Diferença esperada pois a camada ouro contém agregados!")

if __name__ == "__main__":
    main()