from reportlab.pdfgen import canvas

def run(keys, values):

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
        f"C:/Users/Master/Desktop/Leitor-de-notas/arquivos_pdf/{values[0]}.pdf",
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
