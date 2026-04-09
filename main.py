import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from prettytable import PrettyTable

#TRANSFORMAÇÃO DO EXCEL EM DF = LINHA 30
#GERAÇÃO DO HTML = LINHA 39
#GERAÇÃO DOS PDFs = LINHA 338
#GERAÇÃO DOS ARQUIVOS (main) = LINHA 481

#####################################################################################################################
caminho_planilha = 'planilhas/planilha.xlsx'
nome_pagina_planilha = 'Planilha1'
caminho_notasAT = 'notasAT'
#COLOQUE AQUI NOMES DE EVENTOS QUE CONTAM COMO NOTA EXTRA E NÃO NOTA ESSENCIAL
eventos_notas_extras = ["FEIRA",]
#####################################################################################################################

#TRANSFORMAÇÃO DO EXCEL EM DF
def ler_excel():
    excel = pd.ExcelFile(caminho_planilha)
    planilha = excel.parse(nome_pagina_planilha)
    return planilha

#GERAÇÃO DO HTML
def gerarHtml(keys,values):
    
    materias = [materia for materia in keys[3:]]
    notas = [nota for nota in values[3:]]


    #GERA A TABELA DE NOTAS
    def gerarTabela(materias,notas):
        colunas = ""
        valores = ""
        for x in range(0,len(materias)):
            colunas = colunas + f'                    <th>{materias[x]}</th>\n'
            if materias[x].upper() not in eventos_notas_extras and materias[x] != materias[len(materias)-1]:
                if notas[x] == "NOTA NÃO INFORMADA":
                    valores += f'                    <td class="nota-nao-informada">N/A</td>\n'
                elif notas[x] < 6:
                    valores += f'                    <td class="nota-vermelha">{notas[x]:.1f}</td>\n'
                elif notas[x] >= 6:
                    valores += f'                    <td class="nota-azul">{notas[x]:.1f}</td>\n'
            elif materias[x] == materias[len(materias)-1]:
                if notas[x] == "NOTA NÃO INFORMADA":
                    valores += f'                    <td class="nota-nao-informada">N/A</td>\n'
                elif notas[x] < 6:
                    valores += f'                    <td class="media-vermelha">{notas[x]:.1f}</td>\n'
                else:
                    valores += f'                    <td class="media-azul">{notas[x]:.1f}</td>\n'
            else:
                try:
                    valores += f'                    <td class="eventos">{notas[x]:.1f}</td>\n'
                except:
                    valores += f'                    <td class="nota-nao-informada">NULO</td>\n'   
        return colunas, valores
    
    colunas, valores = gerarTabela(materias,notas)

    html = f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/png" href="../logo.png">
    <title>NOTAS DE PROJETOS</title>
    <style>
    * {{
        box-sizing: border-box;
    }}

    body {{
    margin: 0;
    padding: 0;
    font-family: 'Arial', sans-serif;
    background-color: #e9e9e9;
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
    min-height: 100vh;
    }}
    
    h1 {{
        text-align: center;
        color: #2e58a5;
        margin-bottom: 3vh;
        font-size: clamp(16px, 5vw, 24px);
    }}

    .logo-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: -4%;
        margin-bottom: -3%;
        width: 100%;
    }}

    .logo-escola {{
        width: min(310px, 80%);
        height: auto;
    }}

    .container {{
        background: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        padding: 2%;
        max-width: 1100px;
        width: 95%;
    }}

    .info-aluno {{
        text-align: center;
        display: flex;
        gap: clamp(15px, 4vw, 80px);
        justify-content: center;
        flex-wrap: wrap;
        margin-bottom: 4vh;
        margin-top: 1vh;
        color: #000000;
        font-size: clamp(14px, 3vw, 21px);
        font-weight: 500;
        border-bottom: 1px solid #2e58a5;
        padding-bottom: 3vh;
    }}

    .info {{
        text-align: center;
        justify-content: center;
        color: #2e58a5;
    }}

    .tabela-wrapper {{
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
        width: 100%;
        margin: 0 auto;
    }}

    .tabela-notas {{
        width: 100%;
        border-collapse: collapse;
        font-size: clamp(12px, 3vw, 16px);
        border: 1px solid #2e58a5;
        min-width: 600px;
    }}

    .tabela-notas th {{
        background-color: #2e58a5;
        color: white;
        padding: 2vh 2%;
        text-align: center;
        font-weight: bold;
        border: none;
        font-size: clamp(12px, 3vw, 16px);
    }}

    .tabela-notas td {{
        padding: 2vh 2%;
        text-align: center;
        border: none;
        font-weight: 600;
        font-size: clamp(14px, 3vw, 18px);
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
        font-size: clamp(14px, 3vw, 18px);
    }}

    .nota-vermelha {{
        color: #dc2626;
        font-weight: bold;
        font-size: clamp(14px, 3vw, 18px);
    }}

    .eventos {{
        color: #4ea522;
        font-weight: bold;
        font-size: clamp(14px, 3vw, 18px);
    }}

    .nota-nao-informada{{
        color: #000000;
        font-weight: 500;
        font-size: clamp(12px, 2.5vw, 16px);
    }}

    .media-azul {{
        background-color: #dbeafe !important;
        color: #1e40af;
        font-weight: bold;
        font-size: clamp(14px, 3vw, 18px);
    }}

    .media-vermelha {{
        background-color: #fee2e2 !important;
        color: #dc2626;
        font-weight: bold;
        font-size: clamp(14px, 3vw, 18px);
    }}

    .btn-pdf {{
        background-color: #ac1f1f;
        color: white;
        padding: 1.5% 1%;
        border-radius: 10px;
        margin: 3vh auto;
        display: block;
        cursor: pointer;
        font-size: clamp(14px, 3vw, 16px);
        font-weight: bold;
        transition: background-color 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        border: none;
        outline: none;
        width: auto;
        min-width: 200px;
        max-width: 90%;
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
        padding: 1rem;
        margin: 2rem auto 1rem;
        font-size: clamp(12px, 2.5vw, 18px);
        border-left: 6px solid #2e58a5;
        border-radius: 12px;
        background-color: #eef3fc;
        font-weight: 500;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    }}

    .caixa-de-atenção p:first-child {{
    color: #1e3a6b;
    font-weight: 700;
}}

    .final {{
        margin-top: 1rem;
        text-align: right;
        font-weight: 549;
        color: #000000;
        border-top: 1px solid #d4e2f5;
        padding-top: 0.75rem;
    }}

    .creditos{{
        display: flex;
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        margin-top: 4vh;
        padding: 1.5vh 2%;
        color: #e9e9e9;
        background-color: #2e58a5;
        border-radius: 8px 8px 0px 0px;
        width: 100%;
        font-size: clamp(10px, 2.5vw, 14px);
        font-weight: 549;
        text-align: center;
        justify-content: center;
        letter-spacing: 0.5px;
        box-shadow: 0 -2px 6px rgba(0, 0, 0, 0.3);
    }}

    .creditos p {{
        margin: 0;
    }}

    /* ===== AUMENTO DE LETRAS APENAS PARA CELULAR ===== */
    @media (max-width: 768px) {{
    
    .logo-escola {{
        width: 200px;  /* ou qualquer tamanho que preferir */
    }}

    .logo-container {{
        margin-top: -5%;
        margin-bottom: -4%;
    }}

    .tabela-notas {{
        min-width: 0px !important;
        width: 100% !important;
        font-size: 13px !important;
    }}
    
    .tabela-notas td {{
        font-size: 15px !important;
        padding: 20px;
        white-space: nowrap;
    }}
    
    .tabela-notas th {{
        font-size: 13px !important;
        padding: 20px;
        white-space: nowrap;
    }}
    
    h1 {{
        font-size: 18px !important;
    }}
    
    .info-aluno {{
        font-size: 15px !important;
    }}
    
    .btn-pdf {{
        font-size: 12px !important;
        padding: 2%;
    }}
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
                <span><strong class ="info">TURMA:</strong> {values[2]}</span> 
                <span><strong class ="info">ALUNO:</strong> {values[1]}</span>  
            </div>
        <h1>Boletim de Notas do Técnico</h1>
        <div class ="tabela-wrapper">
            <table class="tabela-notas">
                <thead>
                    <tr>
{colunas}
                    </tr>
                </thead>
                <tbody>
                    <tr>
{valores}
                    </tr>
                </tbody>
            </table>
        </div>
        <button class = btn-pdf onclick= "download()">Exportar para PDF</button>
        <div class="caixa-de-atenção">
            <p>• <strong>ATENÇÃO</strong> — Nota(s) não divulgada(s)</p>
            <p style="margin-left: 1.2rem;">Motivo: Aluno não entregou o projeto da disciplina.</p>
            <p>• Em caso de dúvidas, consulte o professor responsável.</p>
            <div class="final">
                Cordialmente,<br>
                <strong>Prof. Alberson Wander Sá dos Santos</strong>
            </div>
        </div>
    </div>
    <div class="creditos">
        <p>DESENVOLVIDO POR: VITOR DORING | CAUÃ MACEDO | JEAN MACHADO · 2°J · 2025</p>
    </div>
    <script>
        function download()
        {{
            const link = document.createElement('a');
            link.href = '{values[0]}.pdf';
            link.download = 'notas-tecnico.pdf';
            link.click();
        }}
    </script>
</body>
</html>



"""
    arquivohtml = open(f'{caminho_notasAT}/{values[0]}.html','w', encoding= "utf-8")
    arquivohtml.write(html)
    arquivohtml.close()

#GERAÇÃO DOS PDFs
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def gerarPDF(keys, values):
    materias = [materia for materia in keys[3:]]
    notas = [nota for nota in values[3:]]

    # Cores
    cor_titulo = (30/255, 58/255, 138/255)
    cor_azul = (37/255, 99/255, 235/255)
    cor_vermelho = (220/255, 38/255, 38/255)
    cor_verde = (78/255, 165/255, 34/255)

    # Configuração do PDF
    pdf = canvas.Canvas(f"{caminho_notasAT}/{values[0]}.pdf", pagesize=A4)
    width, height = A4
    margem_esq = 50
    margem_dir = width - 50
    y_pos = height - 80

    # Título
    pdf.setFont("Helvetica-Bold", 16)
    pdf.setFillColorRGB(*cor_titulo)
    pdf.drawCentredString(width / 2, y_pos, "BOLETIM DE NOTAS DO TÉCNICO")

    # Informações do aluno
    y_pos -= 45
    pdf.setFont("Helvetica-Bold", 13)
    pdf.setFillColorRGB(*cor_titulo)
    pdf.drawString(margem_esq, y_pos, "INFORMAÇÕES DO ALUNO")

    y_pos -= 40
    pdf.setFont("Helvetica-Bold", 12)

    # Labels em azul, valores em preto
    espacamento_vertical = 18
    pdf.setFillColorRGB(*cor_titulo)
    pdf.drawString(margem_esq, y_pos, "RA:")
    pdf.setFillColorRGB(0, 0, 0)
    pdf.setFont("Helvetica", 11)
    pdf.drawString(margem_esq + 35, y_pos, str(values[0]))
    y_pos -= espacamento_vertical

    pdf.setFont("Helvetica-Bold", 12)
    pdf.setFillColorRGB(*cor_titulo)
    pdf.drawString(margem_esq, y_pos, "ALUNO:")
    pdf.setFillColorRGB(0, 0, 0)
    pdf.setFont("Helvetica", 11)
    pdf.drawString(margem_esq + 55, y_pos, values[1])
    y_pos -= espacamento_vertical

    pdf.setFont("Helvetica-Bold", 12)
    pdf.setFillColorRGB(*cor_titulo)
    pdf.drawString(margem_esq, y_pos, "TURMA:")
    pdf.setFillColorRGB(0, 0, 0)
    pdf.setFont("Helvetica", 11)
    pdf.drawString(margem_esq + 55, y_pos, values[2])
    y_pos -= 25

    # Linha azul abaixo das informações
    pdf.setStrokeColorRGB(*cor_titulo)
    pdf.line(margem_esq, y_pos, margem_dir, y_pos)
    y_pos -= 30

    # Tabela de notas
    altura_cab = 25
    altura_valores = 25
    largura_coluna = (margem_dir - margem_esq) / len(materias)

    # Cabeçalho
    pdf.setFillColorRGB(*cor_titulo)
    pdf.rect(margem_esq, y_pos - altura_cab, margem_dir - margem_esq, altura_cab, fill=1, stroke=0)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.setFillColorRGB(1, 1, 1)

    for i, materia in enumerate(materias):
        x = margem_esq + i * largura_coluna + 5
        pdf.drawString(x, y_pos - 17, materia)

    # Notas
    y_pos -= altura_cab
    pdf.setFillColorRGB(0, 0, 0)
    pdf.rect(margem_esq, y_pos - altura_valores, margem_dir - margem_esq, altura_valores, fill=0, stroke=1)
    pdf.setFont("Helvetica-Bold", 11)

    for i, nota in enumerate(notas):
        x = margem_esq + i * largura_coluna + 10
        if nota == "NOTA NÃO INFORMADA":
            pdf.setFillColorRGB(0, 0, 0)
            pdf.drawString(x, y_pos - 17, "NA")
        elif materias[i] in eventos_notas_extras:
            cor = cor_verde
            pdf.setFillColorRGB(*cor)
            pdf.drawString(x, y_pos - 17, f"{float(nota):.1f}")
        else:
            cor = cor_azul if float(nota) >= 6 else cor_vermelho
            pdf.setFillColorRGB(*cor)
            pdf.drawString(x, y_pos - 17, f"{float(nota):.1f}")

    # Moldura preta ao redor da tabela completa (cabeçalho + valores)
    pdf.setStrokeColorRGB(0, 0, 0)
    pdf.setLineWidth(1.3)
    pdf.rect(margem_esq, y_pos - altura_valores, margem_dir - margem_esq, altura_cab + altura_valores, fill=0, stroke=1)

    # Caixa amarela (informações e observações)
    y_pos -= altura_valores + 50
    pdf.setStrokeColorRGB(255/255, 223/255, 43/255)
    pdf.setFillColorRGB(252/255, 238/255, 161/255)

    texto = [
        "• ATENÇÃO: NOTA(S) NÃO DIVULGADA(S):",
        "   Provável motivo → Aluno não entregou projeto da referida disciplina.",
        "",
        "• Qualquer dúvida procure o professor da disciplina para maiores esclarecimentos.",
        "",
        "• NA = Nota não informada"
    ]

    altura_linha = 15
    altura_caixa = len(texto) * altura_linha + 20
    pdf.rect(margem_esq, y_pos - altura_caixa, margem_dir - margem_esq, altura_caixa, fill=1, stroke=1)

    pdf.setFont("Helvetica", 10)
    pdf.setFillColorRGB(0, 0, 0)
    y_texto = y_pos - 15
    for linha in texto:
        pdf.drawString(margem_esq + 10, y_texto, linha)
        y_texto -= altura_linha

    # Assinatura
    y_pos -= altura_caixa + 40
    pdf.setFont("Helvetica-Bold", 11)
    pdf.setFillColorRGB(0, 0, 0)
    pdf.drawString(margem_esq, y_pos, "Cordialmente, Prof. Alberson Wander Sá dos Santos")

    pdf.save()


#GERAÇÃO DOS ARQUIVOS

planilha = ler_excel()

dados = dict()

for _, linha in planilha.iterrows():
    dados = linha.to_dict()
    keys = list(dados.keys())[:]
    values = ["NOTA NÃO INFORMADA" if pd.isna(dados[key]) else dados[key] for key in keys]
    print (f'valueeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee {values}')
    table = PrettyTable()
    table.field_names = keys
    table.add_row(values)
    print(f"Aluno {values[1].upper()} está na linha {_ + 2}")
    print(f"{table}\n")
    gerarHtml(keys,values)
    gerarPDF(keys,values)
