import pandas as pd
from reportlab.pdfgen import canvas
from prettytable import PrettyTable


#TRANSFORMAÇÃO DO EXCEL EM DF = LINHA 15
#GERAÇÃO DO HTML = LINHA 25
#GERAÇÃO DOS PDFs = LINHA 295
#GERAÇÃO DOS ARQUIVOS (main) = LINHA 435




caminho_planilha = 'planilhas/planilha.xlsx'

nome_pagina_planilha = 'Planilha1'

caminho_notasAT = 'notasAT'


#COLOQUE AQUI NOMES DE EVENTOS QUE CONTAM COMO NOTA EXTRA E NÃO NOTA ESSENCIAL
eventos_notas_extras = ["feira"]



#TRANSFORMAÇÃO DO EXCEL EM DF
def ler_excel():
    excel = pd.ExcelFile(caminho_planilha)
    planilha = excel.parse(nome_pagina_planilha)
    return planilha




#GERAÇÃO DO HTML
def gerarHtml(keys, values):
    
    materias = [materia for materia in keys[3:]]
    notas = [nota for nota in values[3:]]
    media = notas.pop(len(notas)-1)
    html = f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/png" href="../logo.png">
    <title>NOTAS DE PROJETOS</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: 'Arial', sans-serif;
            background-color: #e9e9e9;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        
        h1 {{
            text-align: center;
            color: #2e58a5;
            margin-bottom: 30px;
            font-size: 24px;
        }}

        .logo-container {{
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: -4%;
            margin-bottom: -4%;
        }}

        .logo-escola {{
            width: 310px;
        }}   

        .container {{
            background: white;
            margin-top: 2%;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            padding: 30px;
            max-width: 1100px;
            max-height: 600px;
            width: 90%;
        }}

        .info-aluno {{
            text-align: center;
            display: flex;
            gap: 80px;
            justify-content: center;
            margin-bottom: 20px;
            color: #000000;
            font-size: 21px;
            font-weight: 500;
            border-bottom: 1px solid #2e58a5;
            padding-bottom: 30px;
        }}

        .info {{
            text-align: center;
            justify-content: center;
            color: #2e58a5;
        }}

        

        .tabela-notas {{
            width: 100%;
            border-collapse: collapse;
            margin: 0 auto;
            font-size: 16px;
            border: 1px solid #2e58a5
        }}

        .tabela-notas th {{
            background-color: #2e58a5;
            color: white;
            padding: 15px 10px;
            text-align: center;
            font-weight: bold;
            border: none;
        }}

        .tabela-notas td {{
            padding: 15px 10px;
            text-align: center;
            border: none;
            font-weight: 600;
            font-size: 18px;
        }}

        .tabela-notas tr td:nth-child(odd) {{
            background-color: #ffffff;
        }}

        .tabela-notas tr td:nth-child(even) {{
            background-color: #eeeeee;
        }}

        .nota-azul {{
            color: #2563eb;
            font-weight: bold;
            font-size: 18px;
        }}

        .nota-vermelha {{
            color: #dc2626;
            font-weight: bold;
            font-size: 18px;
        }}

        .nota-nao-informada{{
            color: #000000;
            font-weight: 500;
            font-size: 16px;
        }}

        .media-azul {{
            background-color: #dbeafe !important;
            color: #1e40af;
            font-weight: bold;
            font-size: 18px;
        }}

        .media-vermelha {{
            background-color: #fee2e2 !important;
            color: #dc2626;
            font-weight: bold;
            font-size: 18px
        }}

        .btn-pdf {{
            background-color: #ac1f1f;
            color: white;
            padding: 15px 30px;
            border-radius: 10px;
            margin: 35px auto;
            display: block;
            cursor: pointer;
            font-size: 14px;
            font-weight: bold;
            transition: background-color 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            border: none;
            outline: none;
        }}

        .btn-pdf:hover {{
            background-color: #861616;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        }}

        .btn-pdf:active {{
            background-color: #861616;
            transform: translateY(1px);
        }}

        .caixa-de-atenção {{
            text-align: left;
            margin-top: 40px;
            padding: 5px;
            font-size: 18px;
            display: flex;
            flex-direction: column;
            gap: 0px;
            border: 3px solid #ffdf2b;
            border-radius: 10px;
            background-color: #fceea1bb;
            font-weight: 349;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }}

        .final {{
            margin-top: 2%;
            text-align: center;
            font-weight: 600;
        }}

        .creditos{{
            display: flex;
            position: fixed;
            bottom: 0;
            padding-left: 2%;
            color: #e9e9e9;
            background-color: #2e58a5;
            width: 100%;
            font-size: 14px;
            font-weight: 549;
            height: auto;
            left: 0%;
            letter-spacing: 0.5px;
        }}
    </style>
</head>
<body>
<div class="logo-container">
        <img src="https://www.reforco.net/imgempresas/colegio-univap-villa-branca-ja-491-OJ0a.jpg" alt="Logo da Escola" class="logo-escola">
    </div>
    <div class="container">
        <div class="info-aluno">
                <span><strong class ="info">RA:</strong> {values[0]}</span>  
                <span><strong class ="info">ALUNO:</strong> {values[1]}</span> 
                <span><strong class ="info">TURMA:</strong> {values[2]}</span>  
            </div>
        <h1>Boletim de Notas do Técnico</h1>
        <table class="tabela-notas">
            <thead>
                <tr>
"""
    for _,materia in enumerate(materias):
        html += f'                    <th>{materia}</th>\n'

    html += """                </tr>
            </thead>
            <tbody>
                <tr>
"""
    for _, nota in enumerate(notas):
        try:
            if nota < 6:
                html += f'                    <td class="nota-vermelha">{nota:.1f}</td>\n'
            elif nota >= 6:
                html += f'                    <td class="nota-azul">{nota:.1f}</td>\n'       
        except:
            html += f'                    <td class="nota-nao-informada">NÃO INFORMADA</td>\n'

    if media < 6:
        html += f'                    <td class="media-vermelha">{media:.1f}</td>\n'
    else:
        html += f'                    <td class="media-azul">{media:.1f}</td>\n'

    html += f"""                </tr>
            </tbody>
        </table>
        <button class = btn-pdf download = "{values[0]}.pdf">Exportar para PDF</button>
        <div class="caixa-de-atenção">
            <p>• ATENÇÃO: NOTA(S) NÃO DIVULGADA(S), (PROVÁVEL MOTIVO) ==> Aluno não entregou projeto da referida disciplina.</p>
            <p>• Qualquer dúvida procure o professor da disciplina para maiores esclarecimentos.</p>
            <strong class="final">Cordialmente, Prof. Alberson Wander Sá dos Santos</li>
        </div>
    </div>
    <div class="creditos">
        <p>DESENVOLVIDO POR VITOR DORING LEITÃO · 2°J · 2025</p>
    </div>
</body>
</html>



"""
    arquivohtml = open(f'{caminho_notasAT}/{values[0]}.html','w', encoding= "utf-8")
    arquivohtml.write(html)
    arquivohtml.close()






#GERAÇÃO DOS PDFs
def gerarPDF(keys, values):
    def formulaCalcularMedia():
        formula = "("
        for i, disciplina in enumerate(materias[:-1]):  # Exclui "MÉDIA AT3"
            if i > 0:
                formula += " + "
            formula += f"AT {disciplina}"
        formula += f")/{len(materias)-1} = {materias[-1]}"
        return formula

    materias = [materia for materia in keys[3:]]
    notas = [nota for nota in values[3:]]

    cor_textos = (30/255, 58/255, 138/255)
    pdf = canvas.Canvas(
        f"{caminho_notasAT}/{values[0]}.pdf",
        pagesize=(595, 842)
    )
    width, height = 595, 842

    margem_esq = 50
    margem_dir = width - 50
    y_pos = height - 50

    # CABEÇALHO
    pdf.setFont("Helvetica-Bold", 16)
    pdf.setFillColorRGB(*cor_textos)
    pdf.drawString(margem_esq, y_pos, "BOLETIM DE NOTAS DO TÉCNICO")

    y_pos -= 30
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(margem_esq, y_pos, "INFORMAÇÕES DO ALUNO:")

    y_pos -= 25
    pdf.setStrokeColorRGB(*cor_textos)
    pdf.line(margem_esq, y_pos, margem_dir, y_pos)

    y_pos -= 30
    pdf.setFont("Helvetica-Bold", 12)
    pdf.setFillColorRGB(0, 0, 0)

    # Dados
    pdf.drawString(margem_esq, y_pos, "RA:")
    pdf.setFont("Helvetica", 11)
    pdf.drawString(margem_esq + 80, y_pos, str(values[0]))

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(margem_esq + 200, y_pos, "ALUNO:")
    pdf.setFont("Helvetica", 11)
    pdf.drawString(margem_esq + 250, y_pos, values[1])

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(margem_esq + 400, y_pos, "TURMA:")
    pdf.setFont("Helvetica", 11)
    pdf.drawString(margem_esq + 450, y_pos, values[2])

    y_pos -= 40

    # --- TABELA COMPLETA ---
    altura_linha_cab = 25
    altura_linha_valores = 25
    altura_total_tabela = altura_linha_cab + altura_linha_valores

    # Cabeçalho azul
    pdf.setFillColorRGB(*cor_textos)
    pdf.setStrokeColorRGB(0, 0, 0)
    pdf.rect(margem_esq, y_pos - altura_linha_cab, margem_dir - margem_esq, altura_linha_cab, fill=1, stroke=1)

    pdf.setFillColorRGB(1, 1, 1)
    largura_coluna = (margem_dir - margem_esq) / len(materias)
    for i, disciplina in enumerate(materias):
        x_pos = margem_esq + (i * largura_coluna) + 10
        pdf.drawString(x_pos, y_pos - 17, disciplina)

    # Linha de valores
    y_valores = y_pos - altura_linha_cab - altura_linha_valores
    pdf.setFont("Helvetica", 11)
    pdf.setFillColorRGB(0, 0, 0)
    pdf.rect(margem_esq, y_valores, margem_dir - margem_esq, altura_linha_valores, fill=0, stroke=1)

    for i, nota in enumerate(notas):
        x_pos = margem_esq + (i * largura_coluna) + 10
        pdf.setFillColorRGB(0, 0, 0)

        if nota == "NOTA NÃO INFORMADA":
            pdf.drawString(x_pos, y_valores + 8, "NA")
        else:
            pdf.setFillColorRGB(37/255, 99/255, 235/255) if float(nota) >= 6 else pdf.setFillColorRGB(220/255, 38/255, 38/255)
            pdf.drawString(x_pos, y_valores + 8, str(nota))

    # Borda preta em volta de toda a tabela
    pdf.setStrokeColorRGB(0, 0, 0)
    pdf.setLineWidth(1.5)
    pdf.rect(margem_esq, y_valores, margem_dir - margem_esq, altura_total_tabela, fill=0, stroke=1)

    pdf.setLineWidth(1)
    y_pos = y_valores - 60

    # --- CAIXA AMARELA ---
    pdf.setFont("Helvetica", 10)
    pdf.setFillColorRGB(0, 0, 0)

    texto_superior = [
        "Cálculo da média:",
        formulaCalcularMedia(),
        "",
        "• ATENÇÃO: NOTA(S) NÃO DIVULGADA(S):",
        "PROVÁVEL MOTIVO ==> Aluno não entregou projeto da referida disciplina.",
        "• Qualquer dúvida procure o professor da disciplina para maiores esclarecimentos.",
        "",
        "NA = Nota não informada"
    ]

    altura_linha = 15
    altura_caixa = (len(texto_superior) * altura_linha) + 20

    pdf.setStrokeColorRGB(255/255, 223/255, 43/255)
    pdf.setFillColorRGB(252/255, 238/255, 161/255)
    pdf.rect(margem_esq, y_pos - altura_caixa, margem_dir - margem_esq, altura_caixa, fill=1, stroke=1)

    pdf.setFillColorRGB(0, 0, 0)
    y_texto = y_pos - 15
    for linha in texto_superior:
        pdf.drawString(margem_esq + 10, y_texto, linha)
        y_texto -= altura_linha

    y_pos -= altura_caixa + 40

    # Assinatura
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(margem_esq, y_pos, "Cordialmente, Prof. Alberson Wander Sá dos Santos")

    pdf.save()




#GERAÇÃO DOS ARQUIVOS
dados = dict()

planilha = ler_excel()

for _, linha in planilha.iterrows():
    dados = linha.to_dict()
    keys = list(dados.keys())[:]
    values = ["NOTA NÃO INFORMADA" if pd.isna(dados[key]) else dados[key] for key in keys]
    table = PrettyTable()
    table.field_names = keys
    table.add_row(values)
    print(f"Aluno {values[1].upper()} está na linha {_ + 2}")
    print(f"{table}\n")
    gerarHtml(keys,values)
    #gerarPDF(keys,values)
    if _ == 0:
        break