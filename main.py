import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from prettytable import PrettyTable

#TRANSFORMAÇÃO DO EXCEL EM DF = LINHA 22
#GERAÇÃO DO HTML = LINHA 34
#GERAÇÃO DOS PDFs = LINHA 498
#GERAÇÃO DOS ARQUIVOS (main) = LINHA 692

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

        for i, materia in enumerate(materias):
            colunas += f'                    <th>{materia}</th>\n'

            nota = notas[i]

            if nota == "NOTA NÃO INFORMADA":
                valores += '<td class="nota-nao-informada">N/A</td>\n'
                continue

            if materia in eventos_notas_extras:
                valores += f'<td class="eventos">{nota:.1f}</td>\n'
                continue

            if i == len(materias) - 1:  # média
                classe = "media-azul" if nota >= 6 else "media-vermelha"
            else:
                classe = "nota-azul" if nota >= 6 else "nota-vermelha"

            valores += f'<td class="{classe}">{nota:.1f}</td>\n'

        return colunas, valores
    
    colunas, valores = gerarTabela(materias,notas)

    html = f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/png" href="../imagens/logo.png">
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

    .nav-tabela {{
        display: none !important;
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
        width: 200px;
    }}

    .logo-container {{
        margin-top: -7%;
        margin-bottom: -4%;
    }}

    .nav-tabela {{
        display: flex !important; 
        justify-content: space-between;
        align-items: center;
        margin-top: 28px;
        gap: 10px;
    }}
    
    .seta-nav {{
        background: #2e58a5;
        border: none;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.2s ease;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }}
    

    .seta-nav:first-child {{
        margin-right: auto;
    }}
    

    .seta-nav:last-child {{
        margin-left: auto;
    }}
    
    .seta-nav:active {{
        transform: scale(0.92);
        background: #1e3a6b;
    }}
    
    .seta-nav svg {{
        width: 24px;
        height: 24px;
        fill: none;
        stroke: white;
        stroke-width: 2.5;
        stroke-linecap: round;
        stroke-linejoin: round;
    }}

    .tabela-wrapper {{
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
        scrollbar-width: none;
        -ms-overflow-style: none;
    }}

    .tabela-wrapper::-webkit-scrollbar {{
        display: none;
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

    .btn-pdf {{
        margin-top: -8%;
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
        <img src="../imagens/logo_colegios_univap.jpg" alt="Logo da Escola" class="logo-escola">
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
        <div class="nav-tabela">
            <button class="seta-nav" id="seta-esquerda">
                <svg viewBox="0 0 24 24">
                    <path d="M15 18l-6-6 6-6"/>
                </svg>
            </button>
            <button class="seta-nav" id="seta-direita">
                <svg viewBox="0 0 24 24">
                    <path d="M9 18l6-6-6-6"/>
                </svg>
            </button>
        </div>
        <button class = btn-pdf onclick= "download()">Exportar para PDF</button>
        <div class="caixa-de-atenção">
            <p>• <strong>ATENÇÃO</strong> — Nota(s) não divulgada(s)</p>
            <p style="margin-left: 1.2rem;">Provável motivo: Aluno não entregou o projeto da disciplina.</p>
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

        document.addEventListener('DOMContentLoaded', function() {{
        const wrapper = document.querySelector('.tabela-wrapper');
        const setaEsquerda = document.getElementById('seta-esquerda');
        const setaDireita = document.getElementById('seta-direita');
        
        if (!wrapper || !setaEsquerda || !setaDireita) return;
        
        document.getElementById('seta-esquerda').onclick = () => {{
            document.querySelector('.tabela-wrapper').scrollBy({{ left: -300, behavior: 'smooth' }});
        }};

        document.getElementById('seta-direita').onclick = () => {{
            document.querySelector('.tabela-wrapper').scrollBy({{left: 300, behavior: 'smooth' }});
        }};
    }});
    </script>
</body>
</html>



"""
    arquivohtml = open(f'{caminho_notasAT}/{values[0]}.html','w', encoding= "utf-8")
    arquivohtml.write(html)
    arquivohtml.close()

def gerarPDF(keys, values):
    materias = keys[3:]
    notas = values[3:]

    pdf = canvas.Canvas(f"{caminho_notasAT}/{values[0]}.pdf", pagesize=A4)
    width, height = A4

    margem = 30
    y = height - 50

    # CORES
    azul_principal = colors.Color(30/255, 58/255, 138/255)
    azul_secundario = colors.Color(37/255, 99/255, 235/255)
    verde = colors.Color(34/255, 197/255, 94/255)
    vermelho = colors.Color(220/255, 38/255, 38/255)
    cinza_claro = colors.Color(240/255, 240/255, 240/255)

    # =========================
    # HEADER
    # =========================
    pdf.setFillColor(azul_principal)
    pdf.rect(0, height - 95, width, 95, fill=1, stroke=0)

    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 20)  # maior
    pdf.drawCentredString(width/2, height - 55, "Boletim de Notas do Técnico")

    # =========================
    # INFORMAÇÕES
    # =========================
    y -= 115

    pdf.setFillColor(azul_principal)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(margem, y, "INFORMAÇÕES DO ALUNO")

    y -= 32

    def linha_info(label, valor):
        nonlocal y
        pdf.setFont("Helvetica-Bold", 13)
        pdf.setFillColor(azul_principal)
        pdf.drawString(margem, y, label)

        pdf.setFont("Helvetica", 13)
        pdf.setFillColor(colors.black)
        pdf.drawString(margem + 80, y, str(valor))

        y -= 24

    linha_info("RA:", values[0])
    linha_info("ALUNO:", values[1])
    linha_info("TURMA:", values[2])

    # Linha separadora
    y -= 10
    pdf.setStrokeColor(azul_principal)
    pdf.setLineWidth(1.3)
    pdf.line(margem, y, width - margem, y)

    # =========================
    # TABELA
    # =========================
    y -= 70

    largura_total = width - 2 * margem
    largura_col = largura_total / len(materias)

    altura = 40

    # Cabeçalho
    pdf.setFillColor(azul_principal)
    pdf.rect(margem, y, largura_total, altura, fill=1, stroke=0)

    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 12)

    for i, materia in enumerate(materias):
        x_centro = margem + i * largura_col + largura_col / 2
        pdf.drawCentredString(x_centro, y + 13, materia[:12])

    y -= altura

    pdf.setFillColor(cinza_claro)
    pdf.rect(margem, y, largura_total, altura, fill=1, stroke=0)

    pdf.setFont("Helvetica-Bold", 13)

    for i, nota in enumerate(notas):
        x_centro = margem + i * largura_col + largura_col / 2

        if nota == "NOTA NÃO INFORMADA":
            pdf.setFillColor(colors.black)
            texto = "N/A"

        elif materias[i] in eventos_notas_extras:
            pdf.setFillColor(verde)
            texto = f"{float(nota):.1f}"

        else:
            cor = azul_secundario if float(nota) >= 6 else vermelho
            pdf.setFillColor(cor)
            texto = f"{float(nota):.1f}"

        pdf.drawCentredString(x_centro, y + 13, texto)

    # Borda externa
    pdf.setStrokeColor(colors.black)
    pdf.setLineWidth(1.5)
    pdf.rect(margem, y, largura_total, altura * 2, fill=0)

    # Linhas internas
    pdf.setStrokeColor(colors.Color(0.2, 0.2, 0.2))
    pdf.setLineWidth(1)

    # Linha horizontal (entre cabeçalho e notas)
    pdf.line(
        margem,
        y + altura,
        margem + largura_total,
        y + altura
    )

    # Linhas verticais (divisões das colunas)
    for i in range(1, len(materias)):
        x = margem + i * largura_col
        pdf.line(x, y, x, y + altura * 2)

    # =========================
    # AVISO
    # =========================
    y -= 70

    texto = [
        "ATENÇÃO — Nota(s) não divulgada(s)",
        "Provável motivo: aluno não entregou o projeto da disciplina.",
        "",
        "Em caso de dúvidas, consulte o professor responsável.",
        "N/A = Nota não informada"
    ]

    altura_linha = 17
    altura_box = len(texto) * altura_linha + 30

    pdf.setFillColor(colors.Color(0.94, 0.96, 0.98))
    pdf.rect(margem, y - altura_box, largura_total, altura_box, fill=1, stroke=0)

    # barra lateral
    pdf.setFillColor(azul_principal)
    pdf.rect(margem, y - altura_box, 7, altura_box, fill=1, stroke=0)

    # texto
    y_texto = y - 22
    for i, linha in enumerate(texto):
        if i == 0:
            pdf.setFont("Helvetica-Bold", 12)
        else:
            pdf.setFont("Helvetica", 12)

        pdf.setFillColor(colors.black)
        pdf.drawString(margem + 14, y_texto, linha)
        y_texto -= altura_linha

    # =========================
    # ASSINATURA
    # =========================
    y -= altura_box + 55

    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(margem, y, "Cordialmente,")
    pdf.drawString(margem, y - 20, "Prof. Alberson Wander Sá dos Santos")

    logo_path = "imagens/logo_colegios_univap.jpg"

    largura_logo = 350
    altura_logo = 175

    y_logo = y - 220

    pdf.drawImage(
        logo_path,
        margem + 270,
        y_logo,
        width=largura_logo,
        height=altura_logo,
        preserveAspectRatio=True,
        mask='auto'
    )

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
