import html
import pandas as pd

def ler_excel(caminho,nome_aba):
    excel = pd.ExcelFile(caminho)
    planilha = excel.parse(nome_aba)
    return planilha

planilha = ler_excel('planilhas/planilha.xlsx','Página1')

dados = dict()

for _, linha in planilha.iterrows():
    dados = linha.to_dict()
    html.gerar(dados)

