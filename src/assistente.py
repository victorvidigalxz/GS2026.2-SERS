import re
import unicodedata

from src import calculos as c

AVISO = ("\n\nSão estimativas baseadas em premissas (tarifa, hábitos, clima), não garantias. "
         "Confira sua fatura de luz. Fontes: docs/referencias.md")


def _n(t):
    return "".join(ch for ch in unicodedata.normalize("NFD", t.lower()) if unicodedata.category(ch) != "Mn")


def _num(s):
    return float(s.replace(",", "."))


def _calculo_aparelho(t):
    w = re.search(r"(\d+[.,]?\d*)\s*(w|watts?)\b", t)
    h = re.search(r"(\d+[.,]?\d*)\s*(h|hora|horas)\b", t)
    if not (w and h):
        return None
    p = c.carregar_premissas()
    kwh_dia = _num(w.group(1)) * _num(h.group(1)) / 1000
    return (f"Esse aparelho gasta ~{kwh_dia:.2f} kWh por dia, ~{kwh_dia * 30:.1f} kWh/mês "
            f"(≈ R$ {kwh_dia * 30 * p['tarifa_rs_kwh']:.2f}/mês). Conta: potência (W) × horas ÷ 1000.")


def _tempo(anos):
    if anos < 1:
        return f"{anos * 12:.0f} meses"
    return f"{anos:.1f}".replace(".", ",") + " anos"


def _linha(r):
    return (f"• {r['nome']}: economiza ~{r['economia_kwh_mes']:.0f} kWh/mês (≈ R$ {r['economia_rs_mes']:.0f}/mês), "
            f"custo ~R$ {r['custo_inicial_rs']:.0f}, o investimento se paga em ~{_tempo(r['payback_anos'])}.")


def responder(pergunta):
    t = _n(pergunta)
    p = c.carregar_premissas()
    a, b, f = c.comparar()
    total = c.consumo_total()
    COMPARAR_TEXTO = ("Para uma casa de 4 pessoas (~%.0f kWh/mês):\n%s\n%s\n%s\n"
                      "Comece pela A (barata e rápida); B e C custam mais e se sobrepõem no consumo do chuveiro."
                      % (total, _linha(a), _linha(b), _linha(f))) + AVISO

    r = _calculo_aparelho(t)
    if r:
        return r + AVISO
    if "kwh" in t and ("o que" in t or "significa" in t):
        return ("kWh (quilowatt-hora) é a unidade que a conta de luz cobra: 1 kWh é usar 1000 W durante 1 hora. "
                "Exemplo: um aparelho de 1000 W ligado por 1 hora gasta 1 kWh.") + AVISO
    if any(k in t for k in ["compar", "alternativ"]):
        return COMPARAR_TEXTO
    if any(k in t for k in ["aquecedor solar", "solar termic", "agua quente"]):
        return (_linha(b) + f"\nFunciona melhor com bom sol; em dias nublados o chuveiro elétrico "
                f"complementa (premissa: {p['solar_termico']['fracao_solar']:.0%} coberto pelo sol).") + AVISO
    if any(k in t for k in ["fotovoltaic", "painel", "placa", "energia solar", "solar"]):
        return (_linha(f) + f"\nSistema de {str(p['fv']['kwp']).replace('.', ',')} kWp. Mesmo gerando mais, ainda se paga a taxa mínima "
                f"da distribuidora ({p['fv']['custo_disponibilidade_kwh']} kWh) e parte das tarifas de rede.") + AVISO
    if any(k in t for k in ["led", "lampada"]):
        return (f"Trocar 8 lâmpadas por LED de {p['led_w']} W economiza ~{a['detalhe']['LED']:.0f} kWh/mês "
                f"(≈ R$ {a['detalhe']['LED'] * p['tarifa_rs_kwh']:.0f}/mês).") + AVISO
    if any(k in t for k in ["chuveiro", "banho"]):
        ch = c.consumo_por_equipamento()["Chuveiro elétrico"]
        return (f"O chuveiro elétrico é o maior gasto: ~{ch:.0f} kWh/mês ({100 * ch / total:.0f}% da casa). "
                f"Reduzir o banho de {p['banho_min_antes']} para {p['banho_min_depois']} min economiza "
                f"~{a['detalhe']['Banho mais curto']:.0f} kWh/mês.") + AVISO
    if any(k in t for k in ["standby", "stand-by", "tomada", "carregador"]):
        return (f"Aparelhos em stand-by gastam ~{a['detalhe']['Stand-by'] / p['standby_corte']:.0f} kWh/mês. "
                f"Uma régua com interruptor corta cerca de {p['standby_corte']:.0%}.") + AVISO
    if any(k in t for k in ["vale a pena", "qual melhor", "economizar"]):
        return COMPARAR_TEXTO
    for nome, kwh in c.consumo_por_equipamento().items():
        chave = _n(nome).split()[0].strip(",()")
        if chave in t:
            return (f"{nome}: ~{kwh:.0f} kWh/mês (≈ R$ {kwh * p['tarifa_rs_kwh']:.0f}/mês), "
                    f"cerca de {100 * kwh / total:.0f}% do consumo da casa.") + AVISO
    if any(k in t for k in ["garantia", "certeza", "confiavel", "limite", "limitac"]):
        return ("Limitações: consumo, tarifa, sol e preços foram estimados; sua casa pode ser diferente. "
                "Não são promessas de economia. Use sua fatura para ajustar.") + AVISO
    if any(k in t for k in ["fonte", "referencia", "de onde"]):
        return "Fontes: ANEEL, Lei 14.300/2022, Atlas Solar (INPE/LABREN), Procel/Inmetro, MCTI. Veja docs/referencias.md."
    return ("Posso ajudar com: quanto gasta um aparelho (ex.: 'aparelho de 1500 W por 2 horas'), "
            "chuveiro, LED, stand-by, aquecedor solar, energia solar fotovoltaica ou 'comparar alternativas'.")


if __name__ == "__main__":
    print("Citizen Assist AI - módulo Energia (digite 'sair' para encerrar)")
    while True:
        q = input("Você: ").strip()
        if q.lower() in {"sair", "exit"}:
            break
        print("Assistente:", responder(q), "\n")
