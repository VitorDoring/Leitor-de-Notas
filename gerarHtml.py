def run (keys, values):
    
    def formulaCalcularMedia():
    
        calculo = f"((AT {materias[0]}"
        for x in range(1,len(materias)-1):
            calculo += f" + AT {materias[x]}"
        calculo += f")/{len(materias)-1}) = {materias[len(materias)-1]}"
        return calculo
    
    materias = [materia for materia in keys[3:]]
    notas = [nota for nota in values[3:]]
    media = notas.pop(len(notas)-1)
    html = f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Boletim de Notas</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: 'Arial', sans-serif;
            background-color: #e9e9e9;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }}

        .logo-container {{
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: -2%;
            margin-bottom: -56%;
        }}

        .logo-escola {{
            width: 310px;
        }}   

        .container {{
            background: white;
            margin-top: 2%;
            border-radius: 10px;
            justify-content: center;
            align-items: center;
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
            border-bottom: 1px solid #1e3a8a;
            padding-bottom: 30px;
        }}

        .info {{
            text-align: center;
            justify-content: center;
            color: #1e3a8a;
        }}

        .caixa-de-atenção {{
            text-align: left;
            margin-top: 40px;
            padding: 5px;
            font-size: 18px;
            display: flex;
            flex-direction: column;
            gap: 35px;
            border: 3px solid #ffdf2b;
            border-radius: 10px;
            background-color: #fceea1bb;
            font-weight: 349;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }}

        .final {{
            text-align: center;
            font-weight: 600;
        }}

        .tabela-notas {{
            width: 100%;
            border-collapse: collapse;
            margin: 0 auto;
            font-size: 16px;
            border: 1px solid #1e3a8a
        }}

        .tabela-notas th {{
            background-color: #1e3a8a;
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

        h1 {{
            text-align: center;
            color: #1e3a8a;
            margin-bottom: 30px;
            font-size: 24px;
        }}
    </style>
</head>
<body>
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
        <button class = btn-pdf onclick="downloadpdf()">Exportar para PDF</button>
        <div class="caixa-de-atenção">
            <li>{formulaCalcularMedia()}</strong>
            <li>ATENÇÃO: NOTA(S) NÃO DIVULGADA(S), (PROVÁVEL MOTIVO) ==> Aluno não entregou projeto da referida disciplina.</li>
            <li>Qualquer dúvida procure o professor da disciplina para maiores esclarecimentos.</li>
            <strong class="final">Cordialmente, Prof. Alberson Wander Sá dos Santos</li>
        </div>
    </div>
    <div class="logo-container">
        <img src="https://www.reforco.net/imgempresas/colegio-univap-villa-branca-ja-491-OJ0a.jpg" alt="Logo da Escola" class="logo-escola">
    </div>
    <script>
        function downloadpdf() {{
            const link = document.createElement('a');
            link.href = '../arquivos_pdf/{values[0]}.pdf';
            link.download = 'notas-tecnico.pdf';
            link.click();
        }}
    </script>
</body>
</html>



"""
    arquivohtml = open(f'C:/Users/Master/Desktop/Leitor-de-notas/arquivos_html/{values[0]}.html','w', encoding= "utf-8")
    arquivohtml.write(html)
    arquivohtml.close()

