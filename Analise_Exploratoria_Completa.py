# -*- coding: utf-8 -*-
"""
Script gerado automaticamente a partir de Analise_Exploratoria_Completa.ipynb
"""

#==============================================================================
# CÉLULA DE MARKDOWN
# # Demonstração Completa do Kit do Analista
# 
# Este notebook é um teste de estresse para a ferramenta `ferramentas_analista.py`, validando sua capacidade de carregar dados diversos e converter código de notebook com comandos específicos do Jupyter.
#==============================================================================


# --- Célula de Código ---
# Célula 1: Importações iniciais

from ferramentas_analista import carregar_csv_inteligente, converter_notebook_para_py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Comando Mágico de Linha: Essencial para visualização no notebook
# %matplotlib inline

print("✅ Ferramentas e bibliotecas prontas para uso!")


#==============================================================================
# CÉLULA DE MARKDOWN
# ## Passo 1: Carregando Dados com o `carregar_csv_inteligente`
# 
# Vamos carregar nossos três arquivos de exemplo para garantir que a funcionalidade principal continua robusta.
#==============================================================================


# --- Célula de Código ---
df_vendas = carregar_csv_inteligente('relatorio_vendas_BR.csv')
df_feedback = carregar_csv_inteligente('dados_feedback_US.csv')
df_logs = carregar_csv_inteligente('log_acessos.tsv')


#==============================================================================
# CÉLULA DE MARKDOWN
# ## Passo 2: Testando Comandos Específicos do Jupyter
# 
# Esta célula contém múltiplos comandos que só funcionam em um ambiente interativo como o Jupyter. Nosso conversor deve ser capaz de identificá-los e neutralizá-los.
#==============================================================================


# --- Célula de Código ---
# Comando Mágico de Célula: para medir o tempo de execução
# %time

print("Esta célula executa algumas tarefas de teste.")

# Comando de Shell: para instalar uma biblioteca (será comentado)
print("\nVerificando instalação de biblioteca...")
# !pip install openpyxl -q

# Função print(): para renderizar o DataFrame (será convertida)
if df_vendas is not None:
    print("\nExibindo as 5 primeiras linhas do DataFrame de vendas:")
    print(df_vendas.head()) # Convertido de display() para print()


#==============================================================================
# CÉLULA DE MARKDOWN
# ## Passo 3: Análise e Visualização
# 
# Uma análise padrão para garantir que o fluxo de trabalho do analista não foi interrompido.
#==============================================================================


# --- Célula de Código ---
if df_vendas is not None:
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df_vendas, x='Preço', y='Categoria')
    plt.title('Preço Médio por Categoria de Produto')
    plt.xlabel('Preço (R$)')
    plt.ylabel('Categoria')
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.show()


#==============================================================================
# CÉLULA DE MARKDOWN
# ## Passo 4: Conversão Final e Relatório de Compatibilidade
# 
# Agora, a prova final. Vamos executar o conversor neste próprio notebook e observar o relatório detalhado que ele gera, informando sobre todas as modificações feitas para garantir que o script `.py` seja executável.
#==============================================================================


# --- Célula de Código ---
# O nome deste arquivo é 'Analise_Exploratoria_Completa.ipynb'
converter_notebook_para_py('Analise_Exploratoria_Completa.ipynb')

