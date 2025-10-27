import gerarHtml
import pandas as pd
from prettytable import PrettyTable

def ler_excel(caminho,nome_aba):
    excel = pd.ExcelFile(caminho)
    planilha = excel.parse(nome_aba)
    return planilha

planilha = ler_excel('planilhas/planilha_gerada.xlsx','Sheet1')

dados = dict()

for _, linha in planilha.iterrows():
    dados = linha.to_dict()
    keys = list(dados.keys())[:]
    values = ["NOTA NÃO INFORMADA" if pd.isna(dados[key]) else dados[key] for key in keys]
    table = PrettyTable()
    table.field_names = keys
    table.add_row(values)
    print(f"Aluno {values[1].upper()} está na linha {_ + 2}")
    print(f"{table}\n")
    gerarHtml.run(keys,values)


