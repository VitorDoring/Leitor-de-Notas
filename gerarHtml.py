def run (keys,values):
    media = values.pop(len(values)-1)
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
            background-color: #f5f5f5;
            display: flex;
            justify-content: center;
            margin-top: 10%;
            min-height: 100vh;
        }}

        .container {{
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            padding: 30px;
            max-width: 1000px;
            max-height: 250px;
            width: 90%;
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
        <h1>Boletim de Notas do Técnico</h1>
        <table class="tabela-notas">
            <thead>
                <tr>
"""
    for _,materia in enumerate(keys[3:]):
        html += f'                    <th>{materia}</th>\n'

    html += """                </tr>
            </thead>
            <tbody>
                <tr>
"""
    for _, nota in enumerate(values[3:]):
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

    html += """                </tr>
            </tbody>
        </table>
    </div>
</body>
</html>

"""
    arquivohtml = open(f'C:/Users/Master/Desktop/Leitor-de-notas/arquivos_html/{values[0]}.html','w', encoding= "utf-8")
    arquivohtml.write(html)
    arquivohtml.close()

