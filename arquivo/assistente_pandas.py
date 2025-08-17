import pandas as pd
import chardet
import csv
import io

def analisar_e_carregar_csv(caminho_arquivo: str, amostra_bytes: int = 10000) -> pd.DataFrame | None:
    """
    Analisa um arquivo CSV/texto para detectar automaticamente sua codificação e 
    delimitador, exibe um resumo e o carrega em um DataFrame do Pandas.

    Args:
        caminho_arquivo (str): O caminho completo para o arquivo CSV ou de texto.
        amostra_bytes (int): O número de bytes a serem lidos do início do arquivo
                             para a detecção. Aumentar pode melhorar a precisão em
                             arquivos complexos, mas diminui a velocidade.

    Returns:
        pd.DataFrame | None: Um DataFrame do Pandas com os dados carregados ou None
                             se ocorrer um erro.
    """
    print(f"--- 🚀 Iniciando Análise Automática de '{caminho_arquivo}' ---")

    try:
        # --- Passo 1: Detectar a Codificação (Encoding) ---
        with open(caminho_arquivo, 'rb') as f:
            raw_data = f.read(amostra_bytes)
            resultado_chardet = chardet.detect(raw_data)
            codificacao_detectada = resultado_chardet['encoding']
            confianca = resultado_chardet['confidence'] * 100
            
            if codificacao_detectada is None:
                print("⚠️  Aviso: Não foi possível detectar a codificação. Usando 'utf-8' como padrão.")
                codificacao_detectada = 'utf-8'
            
            print(f"✅ Codificação Detectada: '{codificacao_detectada}' (Confiança: {confianca:.2f}%)")

        # --- Passo 2: Detectar o Delimitador ---
        # Usamos uma amostra do texto já decodificado para o Sniffer
        amostra_texto = raw_data.decode(codificacao_detectada, errors='ignore')
        
        delimitador_detectado = ',' # Valor padrão
        try:
            # O Sniffer do CSV analisa a amostra para encontrar o delimitador mais provável
            dialect = csv.Sniffer().sniff(amostra_texto, delimiters=',;|\t')
            delimitador_detectado = dialect.delimiter
            print(f"✅ Delimitador Detectado: '{delimitador_detectado}'")
        except csv.Error:
            print("⚠️  Aviso: Não foi possível detectar o delimitador. Usando ',' (vírgula) como padrão.")

        # --- Passo 3: Carregar os Dados com o Pandas ---
        print("\n--- 🔄 Carregando o arquivo completo com os parâmetros detectados ---")
        df = pd.read_csv(
            caminho_arquivo,
            sep=delimitador_detectado,
            encoding=codificacao_detectada,
            engine='python' # Usar a engine 'python' é mais flexível com delimitadores
        )

        # --- Passo 4: Exibir o Resumo e Retornar o DataFrame ---
        print("\n--- 📊 Resumo do DataFrame Carregado ---")
        print(f"Total de Linhas: {len(df)}")
        print(f"Total de Colunas: {len(df.columns)}")
        
        print("\n--- 📋 Pré-visualização dos Dados (5 primeiras linhas) ---")
        print(df.head())
        
        print("\n--- ℹ️ Informações sobre os Tipos de Dados ---")
        # Usar um buffer de string para capturar a saída de df.info()
        buffer = io.StringIO()
        df.info(buf=buffer)
        info_str = buffer.getvalue()
        print(info_str)
        
        print("--- ✅ Análise concluída! DataFrame pronto para uso. ---")
        
        return df

    except FileNotFoundError:
        print(f"❌ ERRO: O arquivo não foi encontrado no caminho: '{caminho_arquivo}'")
        return None
    except Exception as e:
        print(f"❌ ERRO: Ocorreu um problema inesperado durante o processamento do arquivo.")
        print(f"Detalhes: {e}")
        return None

# --- Exemplo de Uso ---
if __name__ == '__main__':
    # Para testar, vamos criar alguns arquivos CSV de exemplo na mesma pasta do script.
    
    # Exemplo 1: CSV padrão com vírgulas e codificação UTF-8
    dados_csv_virgula = "Nome,Idade,Cidade\nAna,28,São Paulo\nBruno,35,Rio de Janeiro\nCarla,22,Belo Horizonte"
    with open("dados_virgula.csv", "w", encoding="utf-8") as f:
        f.write(dados_csv_virgula)

    # Exemplo 2: CSV com ponto e vírgula (comum no Brasil/Europa) e codificação Latin-1
    dados_csv_ponto_virgula = "Produto;Preço;Estoque\nLaptop;4500.50;30\nMouse;89.90;150\nTeclado;120.00;80"
    with open("dados_ponto_virgula.csv", "w", encoding="latin-1") as f:
        f.write(dados_csv_ponto_virgula)
        
    # Exemplo 3: Arquivo separado por tabulação (TSV)
    dados_tsv = "ID\tUsuário\tStatus\n101\tmaria_s\tAtivo\n102\tjoao_p\tInativo"
    with open("dados_tab.tsv", "w", encoding="utf-8") as f:
        f.write(dados_tsv)

    print("=========================================================")
    print("                 TESTANDO O PRIMEIRO ARQUIVO")
    print("=========================================================")
    df1 = analisar_e_carregar_csv("dados_virgula.csv")
    if df1 is not None:
        print("\n>>> O DataFrame 'df1' está pronto para ser usado!")
        # Ex: print(df1['Idade'].mean())

    print("\n\n=========================================================")
    print("                 TESTANDO O SEGUNDO ARQUIVO")
    print("=========================================================")
    df2 = analisar_e_carregar_csv("dados_ponto_virgula.csv")
    if df2 is not None:
        print("\n>>> O DataFrame 'df2' está pronto para ser usado!")
        # Ex: print(df2.sort_values(by='Preço', ascending=False))
        
    print("\n\n=========================================================")
    print("                 TESTANDO O TERCEIRO ARQUIVO")
    print("=========================================================")
    df3 = analisar_e_carregar_csv("dados_tab.tsv")