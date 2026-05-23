import json

def consolidar():
    with open("resultado.json", "r") as f:
        cspm = json.load(f)

    with open("resultado_devsecops.json", "r") as f:
        devsecops = json.load(f)

    todos = cspm["detalhes"] + devsecops["detalhes"]
    criticas = sum(1 for v in todos if v["severidade"] == "Crítica")
    altas    = sum(1 for v in todos if v["severidade"] == "Alta")
    medias   = sum(1 for v in todos if v["severidade"] == "Média")

    relatorio_final = {
        "resumo": {
            "total_geral": len(todos),
            "criticas": criticas,
            "altas": altas,
            "medias": medias
        },
        "cspm": cspm,
        "devsecops": devsecops
    }

    with open("relatorio_consolidado.json", "w") as f:
        json.dump(relatorio_final, f, indent=4, ensure_ascii=False)

    print("Relatório consolidado gerado!")
    print(json.dumps(relatorio_final["resumo"], indent=4, ensure_ascii=False))

consolidar()
