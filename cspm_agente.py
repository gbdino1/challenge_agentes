import re
import json

def analisar_terraform(caminho_arquivo):
    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        conteudo = arquivo.read()

    resultados = []

    # Regra 1: Bucket S3 público
    if 'acl    = "public-read"' in conteudo:
        resultados.append({
            "tipo": "S3 público",
            "severidade": "Alta",
            "descricao": "Bucket S3 com acesso público.",
            "correcao": "Definir ACL privada."
        })

    # Regra 2: SSH aberto
    padrao_ssh = r'from_port\s*=\s*22[\s\S]*?0\.0\.0\.0\/0'

    if re.search(padrao_ssh, conteudo):
        resultados.append({
            "tipo": "SSH aberto",
            "severidade": "Crítica",
            "descricao": "Porta 22 aberta para qualquer IP.",
            "correcao": "Restringir acesso SSH."
        })

    # Regra 3: RDP aberto
    padrao_rdp = r'from_port\s*=\s*3389[\s\S]*?0\.0\.0\.0\/0'

    if re.search(padrao_rdp, conteudo):
        resultados.append({
            "tipo": "RDP aberto",
            "severidade": "Crítica",
            "descricao": "Porta 3389 aberta para qualquer IP.",
            "correcao": "Restringir acesso RDP."
        })

    relatorio = {
        "total_vulnerabilidades": len(resultados),
        "detalhes": resultados
    }

    with open("resultado.json", "w") as arquivo_json:
        json.dump(relatorio, arquivo_json, indent=4)

    print(json.dumps(relatorio, indent=4, ensure_ascii=False))

# EXECUÇÃO
analisar_terraform("insecure.tf")