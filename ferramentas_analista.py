"""
Caixa de Ferramentas do Analista de Dados (Pandas Mágico)
---------------------------------------------------------

Este módulo fornece um conjunto de funções para agilizar o fluxo de
trabalho de análise de dados, desde a importação inteligente de dados
até a conversão de notebooks para scripts de produção.

Funções disponíveis:
- carregar_csv_inteligente: Analisa e carrega arquivos CSV/texto com 
  detecção automática de separador e codificação.
- converter_notebook_para_py: Transforma um notebook Jupyter (.ipynb) em 
  um script Python (.py) limpo, compatível e gera um relatório de 
  modificações.
"""

import pandas as pd
import chardet
import csv
import io
import nbformat
import sys

# ==============================================================================
# FUNÇÃO 1: CARREGADOR INTELIGENTE DE DADOS (Sem alterações)
# ==============================================================================
def carregar_csv_inteligente(caminho_arquivo: str, amostra_bytes: int = 20000) -> pd.DataFrame | None:
    # (O código desta função permanece o mesmo da versão anterior)
    print(f"--- 🚀 Iniciando Análise Automática de '{caminho_arquivo}' ---")
    try:
        with open(caminho_arquivo, 'rb') as f:
            raw_data = f.read(amostra_bytes)
            resultado_chardet = chardet.detect(raw_data)
            codificacao_detectada = resultado_chardet['encoding']
            
            if codificacao_detectada is None:
                print("⚠️  Aviso: Não foi possível detectar a codificação. Usando 'utf-8'.")
                codificacao_detectada = 'utf-8'
            else:
                confianca = resultado_chardet['confidence'] * 100
                print(f"✅ Codificação Detectada: '{codificacao_detectada}' (Confiança: {confianca:.2f}%)")

        amostra_texto = raw_data.decode(codificacao_detectada, errors='ignore')
        delimitador_detectado = ','
        try:
            dialect = csv.Sniffer().sniff(amostra_texto, delimiters=',;|\t')
            delimitador_detectado = dialect.delimiter
            print(f"✅ Delimitador Detectado: '{delimitador_detectado}'")
        except csv.Error:
            print("⚠️  Aviso: Não foi possível detectar o delimitador. Usando ',' (vírgula).")

        print("\n--- 🔄 Carregando o arquivo com os parâmetros detectados ---")
        df = pd.read_csv(caminho_arquivo, sep=delimitador_detectado, encoding=codificacao_detectada, engine='python')
        print("--- ✅ DataFrame carregado com sucesso! ---")
        return df

    except FileNotFoundError:
        print(f"❌ ERRO: O arquivo não foi encontrado em: '{caminho_arquivo}'")
        return None
    except Exception as e:
        print(f"❌ ERRO: Ocorreu um problema inesperado: {e}")
        return None

# ==============================================================================
# FUNÇÃO 2: CONVERSOR DE NOTEBOOK (Com detecção completa e relatório)
# ==============================================================================
def converter_notebook_para_py(caminho_notebook: str, caminho_script_saida: str | None = None):
    """
    Converte um notebook Jupyter (.ipynb) para um script Python (.py) limpo e compatível.

    Identifica e neutraliza comandos específicos do Jupyter (mágicos, shell, display)
    e gera um relatório final sobre as modificações realizadas.
    """
    if not caminho_notebook.endswith('.ipynb'):
        print("❌ ERRO: O arquivo de entrada deve ser um Jupyter Notebook (.ipynb)")
        return
    if caminho_script_saida is None:
        caminho_script_saida = caminho_notebook.replace('.ipynb', '.py')
    print(f"\n--- 🔄 Convertendo '{caminho_notebook}' para '{caminho_script_saida}' ---")

    try:
        with open(caminho_notebook, 'r', encoding='utf-8') as f:
            notebook = nbformat.read(f, as_version=4)

        script_python = [
            "# -*- coding: utf-8 -*-",
            '"""',
            f"Script gerado automaticamente a partir de {caminho_notebook.split('/')[-1]}",
            '"""',
            ""
        ]
        
        # Usamos um set para armazenar os comandos únicos encontrados
        comandos_jupyter_encontrados = set()

        for cell in notebook.cells:
            if cell.cell_type == 'code':
                codigo_limpo = []
                linhas_codigo = cell.source.split('\n')
                
                for i, linha in enumerate(linhas_codigo):
                    linha_strip = linha.strip()
                    linha_processada = linha

                    # Identifica todos os comandos, mas só processa uma vez por linha
                    if 'display(' in linha:
                        linha_processada = linha.replace('display(', 'print(', 1)
                        if '#' not in linha_processada:
                            linha_processada += " # Convertido de display() para print()"
                        comandos_jupyter_encontrados.add('display()')
                    
                    elif linha_strip.startswith('%'):
                        # Pega o comando específico (ex: %matplotlib, %%time)
                        comando_magico = linha_strip.split(' ')[0]
                        comandos_jupyter_encontrados.add(comando_magico)
                        linha_processada = f"# {linha}"
                    
                    elif linha_strip.startswith('!'):
                        # Pega o comando shell (ex: !pip)
                        comando_shell = "!" + linha_strip[1:].split(' ')[0]
                        comandos_jupyter_encontrados.add(comando_shell)
                        linha_processada = f"# {linha}"
                    
                    codigo_limpo.append(linha_processada)
                
                script_python.extend(["\n# --- Célula de Código ---", *codigo_limpo, "\n"])

            elif cell.cell_type == 'markdown':
                script_python.append("#" + "="*78)
                linhas_markdown = [f"# {linha}" for linha in cell.source.split('\n')]
                script_python.extend(["# CÉLULA DE MARKDOWN", *linhas_markdown])
                script_python.append("#" + "="*78 + "\n")

        with open(caminho_script_saida, 'w', encoding='utf-8') as f:
            f.write("\n".join(script_python))

        print(f"--- ✅ Conversão concluída! Arquivo salvo em: '{caminho_script_saida}' ---")

        # Gera o relatório final se algum comando foi encontrado
        if comandos_jupyter_encontrados:
            print("\n" + "="*50)
            print("⚠️  RELATÓRIO DE COMPATIBILIDADE")
            print("="*50)
            print("Seu notebook continha comandos específicos do Jupyter que não")
            print("funcionam em scripts .py. Eles foram tratados da seguinte forma:")
            
            # Ordena para uma exibição consistente
            for cmd in sorted(list(comandos_jupyter_encontrados)):
                if cmd == 'display()':
                    print(f"   - [CONVERTIDO] '{cmd}': Substituído pela função 'print()'.")
                else:
                    print(f"   - [COMENTADO]  '{cmd}': A linha de comando foi mantida, mas desativada com '#'.")
            print("="*50)

    except FileNotFoundError:
        print(f"❌ ERRO: Notebook '{caminho_notebook}' não encontrado.")
    except Exception as e:
        print(f"❌ ERRO: Problema inesperado durante a conversão: {e}")