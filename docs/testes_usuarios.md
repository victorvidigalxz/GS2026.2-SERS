# Testes com usuários e ajustes realizados

**Natureza dos testes:** os testes abaixo foram **simulados**. Foram usados perfis fictícios e perguntas reais executadas no assistente. Não houve participação de pessoas reais, e nenhum dado pessoal foi coletado. Os comentários da coluna "Comentário (simulado)" são hipóteses de compreensão, não depoimentos.

## Parte 1 — Execução do assistente (resultados reais)

| Pergunta | Resultado na 1ª versão | Problema | Ajuste |
|---|---|---|---|
| "quanto gasta minha geladeira?" | Resposta genérica de ajuda | Só aparelhos citados em regras específicas eram reconhecidos | Passou a consultar todos os equipamentos de `data/equipamentos.csv` |
| "o que é kWh?" | Resposta genérica de ajuda | Termo técnico sem explicação | Criada resposta explicando kWh com exemplo |
| "vale a pena colocar placa solar?" | Comparação das três alternativas | Pergunta sobre solar recebia resposta genérica | Perguntas sobre solar agora recebem a resposta específica da fonte renovável |
| "qual alternativa vale mais a pena?" | "retorno em ~0.3 anos" | Prazo em decimal de ano era confuso | Prazos menores que 1 ano aparecem em meses e o texto passou a dizer "o investimento se paga em" |

## Parte 2 — Perfis simulados

| Usuário | Perfil (fictício) | Situação testada | Compreendeu? | Comentário (simulado) | Ajuste realizado |
|---|---|---|---|---|---|
| 1 | Pessoa jovem, mora com a família, sem conhecimento técnico | "quanto gasta o chuveiro?" | Sim | Entende que o chuveiro é o maior gasto; pode não saber o que é kWh | Explicação de kWh adicionada |
| 2 | Responsável pela conta de luz da casa | "qual alternativa vale mais a pena?" | Parcialmente | Prazo em "0.3 anos" é confuso | Prazos curtos em meses |
| 3 | Pessoa interessada em energia solar | "vale a pena colocar placa solar?" | Sim, após o ajuste | Esperava resposta só sobre solar | Resposta específica para solar |

