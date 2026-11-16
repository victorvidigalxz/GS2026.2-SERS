# Citizen Assist AI — Energia e Sustentabilidade

Global Solution 2026 — Soluções em Energias Renováveis e Sustentáveis (SERS) — Ciência da Computação / 1CC

Contribuição de SERS ao Citizen Assist AI: `src/`, `data/` e `docs/` deste repositório.

## Integrantes
| Nome | RM |
|---|---|
| Victor Vidigal | 571318 |
| Gabriel Savoy | 568991 |
| Raphael Tien | 570261 |

## Público e problema
**Público:** famílias urbanas de 4 pessoas em São Paulo, sem conhecimento técnico de energia.

**Problema:** a conta de luz pesa no orçamento e as pessoas não sabem quais hábitos e investimentos reduzem o gasto. Na estimativa do grupo, o chuveiro elétrico responde por cerca de 40% do consumo.

**Contribuição do assistente:** responde em linguagem simples quanto cada aparelho gasta e compara alternativas de economia e de fonte renovável, informando premissas e limitações.

## Funcionalidades de energia
1. Cálculo do consumo de qualquer aparelho (ex.: "aparelho de 1500 W por 2 horas").
2. Diagnóstico do consumo típico da casa por equipamento.
3. Comparação de três alternativas para a mesma necessidade (reduzir a conta de luz, base de 12 meses):
   - A) Eficiência: LED, banho mais curto e régua anti stand-by
   - B) Aquecedor solar de água (renovável)
   - C) Energia solar fotovoltaica (renovável)
4. Respostas com custo, retorno do investimento, CO₂ evitado, limitações e referências.

## Como executar
Requer Python 3.9 ou superior, sem bibliotecas externas. Na pasta do projeto:
```
python -m src.calculos
python -m src.assistente
```
O primeiro comando gera `docs/comparacao.md`. O segundo abre o assistente no terminal (digite `sair` para encerrar). Para integrar ao assistente principal: `from src.assistente import responder`.

## Estrutura
```
data/equipamentos.csv    consumo base dos equipamentos (origem indicada em cada linha)
data/premissas.json      tarifa, custos, irradiação, fatores e demais premissas
src/calculos.py          cálculos de consumo e comparação das alternativas
src/assistente.py        respostas do assistente
docs/comparacao.md       cálculos e comparação das alternativas
docs/justificativas.md   justificativas (custos, viabilidade e impactos ambientais)
docs/referencias.md      referências utilizadas
docs/testes_usuarios.md  testes com usuários e ajustes realizados
```

## Dados e premissas
Os dados de consumo, a tarifa, os preços, a irradiação solar e o fator de emissão são estimativas e estão identificados como tais em `data/equipamentos.csv` e `data/premissas.json`. Fontes em `docs/referencias.md`.

## Resultados (estimativas)
| Alternativa | Economia por mês | Custo inicial | Retorno |
|---|---|---|---|
| A) Eficiência | ~42 kWh (~R$ 38) | ~R$ 136 | ~4 meses |
| B) Aquecedor solar de água | ~62 kWh (~R$ 55) | ~R$ 4.500 | ~6,8 anos |
| C) Fotovoltaico 1,5 kWp | ~162 kWh (~R$ 124) | ~R$ 7.500 | ~5,0 anos |
