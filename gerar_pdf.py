import json
import subprocess
from datetime import datetime

def gerar_pdf():
    with open("relatorio_consolidado.json", "r") as f:
        data = json.load(f)

    resumo   = data["resumo"]
    cspm     = data["cspm"]["detalhes"]
    devsecops = data["devsecops"]["detalhes"]
    agora    = datetime.now().strftime("%d/%m/%Y %H:%M")

    def linha_tabela(v):
        cor = {"Crítica": "#ff4444", "Alta": "#ff8800", "Média": "#ffcc00"}.get(v["severidade"], "#333")
        return f"""
        <tr>
            <td>{v['tipo']}</td>
            <td style='color:{cor}'><b>{v['severidade']}</b></td>
            <td>{v['descricao']}</td>
            <td>{v['correcao']}</td>
        </tr>"""

    html = f"""
    <html>
    <head>
        <meta charset='utf-8'>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                color: #1a1a2e;
            }}
            h1 {{
                color: #1a1a2e;
                border-bottom: 3px solid #0f3460;
                padding-bottom: 10px;
            }}
            h2 {{
                color: #16213e;
                border-bottom: 2px solid #0f3460;
                padding-bottom: 6px;
                margin-top: 30px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 30px;
                font-size: 13px;
            }}
            th {{
                background: #0f3460;
                color: white;
                padding: 10px;
                text-align: left;
            }}
            td {{
                padding: 8px 10px;
                border: 1px solid #ddd;
            }}
            tr:nth-child(even) {{
                background: #f5f5f5;
            }}
            .resumo {{
                background: #f0f4ff;
                padding: 15px 20px;
                border-radius: 8px;
                border-left: 5px solid #0f3460;
                margin-bottom: 20px;
            }}
            .resumo p {{
                margin: 6px 0;
                font-size: 15px;
            }}
            .badge {{
                display: inline-block;
                padding: 3px 10px;
                border-radius: 12px;
                color: white;
                font-weight: bold;
                margin-right: 10px;
            }}
            .critica {{ background: #ff4444; }}
            .alta    {{ background: #ff8800; }}
            .media   {{ background: #ccaa00; }}
            .total   {{ background: #0f3460; }}
            footer {{
                margin-top: 40px;
                font-size: 11px;
                color: #888;
                border-top: 1px solid #ddd;
                padding-top: 10px;
            }}
        </style>
    </head>
    <body>

        <h1>🔐 Relatório Consolidado de Segurança</h1>
        <p>Gerado automaticamente via GitHub Actions em: <b>{agora}</b></p>

        <div class='resumo'>
            <h2>📊 Resumo Geral</h2>
            <p>
                <span class='badge critica'>🔴 Críticas: {resumo['criticas']}</span>
                <span class='badge alta'>🟠 Altas: {resumo['altas']}</span>
                <span class='badge media'>🟡 Médias: {resumo['medias']}</span>
                <span class='badge total'>📊 Total: {resumo['total_geral']}</span>
            </p>
        </div>

        <h2>🔍 Agente CSPM — Infraestrutura (Terraform)</h2>
        <table>
            <tr>
                <th>Tipo</th>
                <th>Severidade</th>
                <th>Descrição</th>
                <th>Correção</th>
            </tr>
            {''.join(linha_tabela(v) for v in cspm)}
        </table>

        <h2>🛡️ Agente DevSecOps — Código (app.js)</h2>
        <table>
            <tr>
                <th>Tipo</th>
                <th>Severidade</th>
                <th>Descrição</th>
                <th>Correção</th>
            </tr>
            {''.join(linha_tabela(v) for v in devsecops)}
        </table>

        <footer>
            Relatório gerado automaticamente pelo pipeline CSPM + DevSecOps | GitHub Actions
        </footer>

    </body>
    </html>
    """

    with open("relatorio.html", "w", encoding="utf-8") as f:
        f.write(html)

    subprocess.run(
        ["wkhtmltopdf", "--encoding", "utf-8", "relatorio.html", "relatorio_final.pdf"],
        check=True
    )

    print("✅ PDF gerado com sucesso: relatorio_final.pdf")

gerar_pdf()
