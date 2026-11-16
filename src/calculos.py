import csv
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def carregar_premissas():
    return json.loads((RAIZ / "data" / "premissas.json").read_text(encoding="utf-8"))


def carregar_equipamentos():
    with open(RAIZ / "data" / "equipamentos.csv", encoding="utf-8") as f:
        return [
            {"nome": r["equipamento"], "potencia_w": float(r["potencia_w"]),
             "horas_dia": float(r["horas_dia"]), "dias_mes": float(r["dias_mes"]),
             "qtd": int(r["quantidade"]), "origem": r["origem"]}
            for r in csv.DictReader(f)
        ]


def kwh_mes(e):
    return e["potencia_w"] * e["horas_dia"] * e["dias_mes"] * e["qtd"] / 1000


def consumo_por_equipamento():
    return {e["nome"]: kwh_mes(e) for e in carregar_equipamentos()}


def consumo_total():
    return sum(consumo_por_equipamento().values())


def _buscar(prefixo):
    c = consumo_por_equipamento()
    return next(v for k, v in c.items() if k.startswith(prefixo))


def custo_mensal(kwh, tarifa):
    return kwh * tarifa


def alternativa_eficiencia(p=None):
    p = p or carregar_premissas()
    lamp = _buscar("Lâmpadas")
    pot_atual = next(e for e in carregar_equipamentos() if e["nome"].startswith("Lâmpadas"))["potencia_w"]
    eco_led = lamp * (1 - p["led_w"] / pot_atual)
    eco_banho = _buscar("Chuveiro") * (1 - p["banho_min_depois"] / p["banho_min_antes"])
    eco_standby = _buscar("Stand-by") * p["standby_corte"]
    kwh = eco_led + eco_banho + eco_standby
    custo = 8 * p["custo_led_un"] + p["custo_regua"]
    return _resumo("A) Eficiência (LED + banho de 6 min + régua anti stand-by)", kwh, custo, p,
                   {"LED": eco_led, "Banho mais curto": eco_banho, "Stand-by": eco_standby})


def alternativa_solar_termico(p=None):
    p = p or carregar_premissas()
    kwh = _buscar("Chuveiro") * p["solar_termico"]["fracao_solar"]
    return _resumo("B) Aquecedor solar de água (renovável)", kwh, p["solar_termico"]["custo_rs"], p)


def alternativa_fotovoltaico(p=None):
    p = p or carregar_premissas()
    fv = p["fv"]
    geracao = fv["kwp"] * fv["hsp_kwh_m2_dia"] * 30 * fv["desempenho"]
    compensavel = max(consumo_total() - fv["custo_disponibilidade_kwh"], 0)
    kwh = min(geracao, compensavel)
    return _resumo("C) Energia solar fotovoltaica (renovável)", kwh, fv["custo_rs"], p,
                   {"Geração estimada (kWh/mês)": geracao}, fator_rs=fv["fator_compensacao"])


def _resumo(nome, kwh, custo, p, detalhe=None, fator_rs=1.0):
    eco_rs = kwh * p["tarifa_rs_kwh"] * fator_rs
    payback_meses = custo / eco_rs if eco_rs > 0 else float("inf")
    meses = p["horizonte_anos"] * 12
    return {
        "nome": nome,
        "economia_kwh_mes": kwh,
        "economia_rs_mes": eco_rs,
        "custo_inicial_rs": custo,
        "payback_anos": payback_meses / 12,
        "saldo_horizonte_rs": eco_rs * meses - custo,
        "co2_evitado_kg_ano": kwh * 12 * p["fator_emissao_kg_kwh"],
        "detalhe": detalhe or {},
    }


def comparar():
    p = carregar_premissas()
    return [alternativa_eficiencia(p), alternativa_solar_termico(p), alternativa_fotovoltaico(p)]


def gerar_relatorio():
    p = carregar_premissas()
    total = consumo_total()
    linhas = ["# Comparação das alternativas (gerado por `python -m src.calculos`)", "",
              f"**Consumo base estimado:** {total:.0f} kWh/mês (~R$ {custo_mensal(total, p['tarifa_rs_kwh']):.2f}/mês "
              f"à tarifa de R$ {p['tarifa_rs_kwh']:.2f}/kWh, valor **estimado**).", "",
              "## Consumo por equipamento (kWh/mês)", "", "| Equipamento | kWh/mês | % |", "|---|---|---|"]
    for k, v in sorted(consumo_por_equipamento().items(), key=lambda x: -x[1]):
        linhas.append(f"| {k} | {v:.1f} | {100 * v / total:.0f}% |")
    linhas += ["", f"## Alternativas (período de referência: 12 meses; saldo em {p['horizonte_anos']} anos)", "",
               "| Alternativa | Economia kWh/mês | Economia R$/mês | Custo inicial R$ | Payback (anos) | Saldo no horizonte R$ | CO₂ evitado kg/ano |",
               "|---|---|---|---|---|---|---|"]
    for r in comparar():
        linhas.append(f"| {r['nome']} | {r['economia_kwh_mes']:.0f} | {r['economia_rs_mes']:.2f} | "
                      f"{r['custo_inicial_rs']:.0f} | {r['payback_anos']:.1f} | {r['saldo_horizonte_rs']:.0f} | "
                      f"{r['co2_evitado_kg_ano']:.0f} |")
    linhas += ["", "> As alternativas **não são somáveis**: B e C atuam sobre o mesmo consumo (chuveiro). "
               "Valores são estimativas, sem inflação tarifária, degradação ou financiamento. "
               "Veja `docs/justificativas.md` e `docs/referencias.md`."]
    return "\n".join(linhas) + "\n"


if __name__ == "__main__":
    texto = gerar_relatorio()
    (RAIZ / "docs" / "comparacao.md").write_text(texto, encoding="utf-8")
    print(texto)
