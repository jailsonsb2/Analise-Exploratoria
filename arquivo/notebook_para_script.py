import nbformat
import sys

def converter_notebook_para_script(caminho_notebook: str, caminho_script_saida: str | None = None):
    """
    Converte um arquivo Jupyter Notebook (.ipynb) para um script Python (.py) limpo.

    - Células de código são mantidas como estão.
    - Células de Markdown são convertidas em blocos de comentários Python.
    - Comandos "mágicos" do Jupyter (ex: %matplotlib) são comentados.
    
    Args:
        caminho_notebook (str): O caminho para o arquivo .ipynb de entrada.
        caminho_script_saida (str, optional): O caminho para o arquivo .py de saída.
                                            Se não for fornecido, será criado com o
                                            mesmo nome do notebook, mas com extensão .py.
    """
    if not caminho_notebook.endswith('.ipynb'):
        print("❌ ERRO: O arquivo de entrada deve ser um Jupyter Notebook (.ipynb)")
        return

    # Define o nome do arquivo de saída se não for especificado
    if caminho_script_saida is None:
        caminho_script_saida = caminho_notebook.replace('.ipynb', '.py')

    print(f"--- 🔄 Convertendo '{caminho_notebook}' para '{caminho_script_saida}' ---")

    try:
        # Lê o notebook usando nbformat
        with open(caminho_notebook, 'r', encoding='utf-8') as f:
            notebook = nbformat.read(f, as_version=4)

        script_python = []
        script_python.append("# -*- coding: utf-8 -*-")
        script_python.append('"""')
        script_python.append(f"Script gerado automaticamente a partir de {caminho_notebook.split('/')[-1]}")
        script_python.append('"""')
        script_python.append("") # Linha em branco

        # Itera sobre cada célula do notebook
        for cell in notebook.cells:
            # Se for uma célula de código
            if cell.cell_type == 'code':
                codigo_limpo = []
                linhas_codigo = cell.source.split('\n')
                
                for linha in linhas_codigo:
                    # Comenta comandos mágicos do Jupyter que não funcionam em scripts .py
                    if linha.strip().startswith('%') or linha.strip().startswith('!'):
                        codigo_limpo.append(f"# {linha}")
                    else:
                        codigo_limpo.append(linha)

                script_python.append("\n# --- Célula de Código ---")
                script_python.extend(codigo_limpo)
                script_python.append("\n")

            # Se for uma célula de markdown
            elif cell.cell_type == 'markdown':
                script_python.append("#" + "="*78)
                script_python.append("# CÉLULA DE MARKDOWN (TEXTO)")
                
                # Transforma cada linha do markdown em um comentário
                linhas_markdown = cell.source.split('\n')
                for linha in linhas_markdown:
                    script_python.append(f"# {linha}")
                
                script_python.append("#" + "="*78)
                script_python.append("\n")

        # Junta todo o conteúdo em uma única string
        script_final = "\n".join(script_python)

        # Escreve o script final no arquivo de saída
        with open(caminho_script_saida, 'w', encoding='utf-8') as f:
            f.write(script_final)

        print(f"--- ✅ Conversão concluída com sucesso! ---")
        print(f"Arquivo gerado: {caminho_script_saida}")

    except FileNotFoundError:
        print(f"❌ ERRO: O arquivo notebook '{caminho_notebook}' não foi encontrado.")
    except Exception as e:
        print(f"❌ ERRO: Ocorreu um problema inesperado durante a conversão.")
        print(f"Detalhes: {e}")

# --- Exemplo de Uso pela Linha de Comando ---
if __name__ == '__main__':
    # Permite chamar o script assim: python notebook_para_script.py meu_notebook.ipynb
    if len(sys.argv) > 1:
        caminho_do_notebook = sys.argv[1]
        converter_notebook_para_script(caminho_do_notebook)
    else:
        print("Uso: python notebook_para_script.py <caminho_para_seu_notebook.ipynb>")
        
        # Para demonstração, vamos criar um notebook de exemplo e convertê-lo
        print("\n--- Criando um notebook de exemplo para demonstração ---")
        
        notebook_exemplo_json = r"""
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Análise Exploratória de Vendas\n",
    "\n",
    "Este notebook tem como objetivo analisar os dados de vendas de 2024 para identificar tendências."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "%matplotlib inline"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. Carregando os Dados\n",
    "\n",
    "Vamos carregar o arquivo `vendas.csv`."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "df = pd.read_csv('vendas.csv')\n",
    "print('Dados carregados com sucesso!')"
   ]
  }
 ],
 "metadata": {},
 "nbformat": 4,
 "nbformat_minor": 2
}
"""
        with open("exemplo.ipynb", "w") as f:
            f.write(notebook_exemplo_json)
        
        # Converte o notebook criado
        converter_notebook_para_script("exemplo.ipynb")