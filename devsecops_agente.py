import re
import json

def analisar_codigo(caminho):
    with open(caminho, "r", encoding="utf-8") as arquivo:
        conteudo = arquivo.read()

    resultados = []

    # Regra 1: uso de eval()
    if "eval(" in conteudo:
        resultados.append({
            "tipo": "Uso de eval",
            "severidade": "Alta",
            "descricao": "Uso de eval pode executar código malicioso.",
            "correcao": "Evitar eval."
        })

    # Regra 2: senha hardcoded
    if re.search(r'password\s*=\s*["\'].*["\']', conteudo):
        resultados.append({
            "tipo": "Senha exposta",
            "severidade": "Alta",
            "descricao": "Senha hardcoded detectada.",
            "correcao": "Usar variável de ambiente."
        })

    # Regra 3: console.log sensível
    if "console.log" in conteudo:
        resultados.append({
            "tipo": "Exposição de dados",
            "severidade": "Média",
            "descricao": "console.log pode expor dados.",
            "correcao": "Remover logs sensíveis."
        })

    relatorio = {
        "total_vulnerabilidades": len(resultados),
        "detalhes": resultados
    }

    with open("resultado_devsecops.json", "w") as f:
        json.dump(relatorio, f, indent=4)

    print(json.dumps(relatorio, indent=4, ensure_ascii=False))

# EXECUÇÃO
analisar_codigo("app.js")