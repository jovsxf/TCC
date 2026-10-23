# Base v2 e notebook com as novas colunas: o que mudou, por quê e o que falta decidir

Este documento acompanha a nova extração da base, feita em 21 e 22/10/2026, e a versão do notebook que roda sobre ela (`pre_defesa_analise_exploratoria_v2_base_v2_novas_colunas.ipynb`).

Todos os números vêm de contagens agregadas ou das saídas do notebook. Nenhum deles identifica aluno. A base (`dados_alunos.csv`) continua fora do repositório.

---

## 1. Resumo

- A base agora traz a **data de cada ocorrência**, para analisar a ordem dos eventos dentro do semestre.
- Foram corrigidos **dois erros da extração anterior**:
  - nas linhas que vêm só de ocorrência, diplomação e transferência/afastamento estavam com os valores trocados;
  - reprovações (`IA34_03`) e `IA65_03` recebiam valores de outro currículo do mesmo aluno no mesmo semestre.
- Entraram **quatro indicadores novos**: rematrícula, falecimento, prazo de integralização esgotado e afastamento sem ocorrência. Nenhuma regra de análise foi alterada por causa deles.
- A estrutura da base continua a mesma: 59.059 registros, 7.615 alunos, 3.507 alunos com saída e 3.841 linhas positivas. Vários números da pré-defesa mudaram e precisam ser atualizados no artigo: amostras, CRE, frequência, contagens de disciplinas, indicadores financeiros, indicadores socioeconômicos e trajetória (seção 4). A maior parte das mudanças vem da correção da diplomação. Sexo e rendas parecem refletir dados atualizados entre as extrações.
- O notebook ganhou três células de análise (59, 60 e 61) e um ajuste na tabela de ausências (célula 67). Ele roda inteiro sem erros.

---

## 2. O que mudou na base e por quê

### 2.1 Datas das ocorrências

**O que entrou:** dois tipos de data, que não devem ser confundidos.

- **Data da ocorrência:** a data atribuída ao evento no registro do aluno. Ela aparece por tipo (`DATADESISTENCIA`, `DATAABANDONO`, `DATATRANCAMENTO`, `DATAREINGRESSO` etc.) e, para as saídas, em `DATAPRIMEIRASAIDA` e `DATAULTIMASAIDA` (primeira e última data de saída no semestre). Quando há mais de um registro do mesmo tipo no semestre, vale a primeira data.
- **Data de inclusão no sistema:** o dia em que a saída foi lançada, em `DATAINCLUSAOSAIDA`. Ela pode ser bem posterior à data da ocorrência, quando o lançamento é retroativo.

As análises de ordem dos eventos usam a data da ocorrência. A data de inclusão serve só como diagnóstico, para medir lançamentos retroativos (seção 3.3).

**Por quê:** a "ordem dos eventos dentro do semestre" estava nas pendências. Só com as flags não dá para saber, por exemplo, se um reingresso veio antes ou depois de uma desistência no mesmo semestre.

### 2.2 Correção: diplomação × transferência/afastamento

**O problema:** nas linhas com `ORIGEMREGISTRO = OCORRENCIA`, os valores de `TEVEDIPLOMACAO` e `TEVETRANSAFASTAMENTO` estavam trocados entre si.

**Efeito:** a base antiga tinha 2.884 diplomações e 85 transferências/afastamentos. O correto é **2.644 e 325**.

**Por que importa:** a conclusão do curso entra na escolha de quem vira caso e de quem vira referência nas comparações. Por isso a correção mudou alguns números da pré-defesa (seção 4).

### 2.3 Correção: reprovações (`IA34_03`) e `IA65_03`

**O problema:** quando o aluno tinha mais de um currículo no mesmo semestre (caso típico de migração de currículo), a linha do outro currículo recebia as reprovações do currículo em que ele estava matriculado.

**Efeito na versão anterior:** 5.793 linhas de origem ocorrência tinham mais reprovações do que disciplinas matriculadas.

**Correção:** cada linha passou a receber só os valores do próprio vínculo no semestre. Nas linhas só de ocorrência, `IA34_03` agora fica vazio, como já acontecia com a frequência (`IA04_01`, `IA04_02`) e com `IA65_03`.

**Resultado:** linhas de ocorrência com reprovadas maiores que matriculadas caíram de 5.793 para 0. Nas linhas acadêmicas, caíram de 140 para 138.

A comparação de reprovações entre casos e referências (3,282 × 1,593) não mudou, porque ela usa só linhas acadêmicas. O erro afetaria a modelagem, não a análise da pré-defesa.

### 2.4 Indicadores novos

| Coluna | O que indica | Por que foi trazida |
|---|---|---|
| `TEVEREMATRICULA` | Rematrícula | Verificar se representa retorno depois de uma saída |
| `TEVEFALECIMENTO` | Falecimento | Não é evasão; esses alunos precisam sair de casos e referências |
| `TEVEPRAZOESGOTADO` | Prazo de integralização esgotado | Verificar se encerra o vínculo |
| `TEVEAFASTAMENTOSEMOCORRENCIA` | Afastamento sem ocorrência | Verificar se é saída definitiva ou intervalo até o retorno |

Cada indicador vem com a data correspondente (`DATAREMATRICULA` etc.). Eles só trazem a informação. A decisão sobre cada um está na seção 6.

### 2.5 Identificação da extração

Para conseguirmos reproduzir a análise depois, a extração usada neste notebook fica identificada assim:

| Item | Valor |
|---|---|
| Data da extração | 22/10/2026 |
| Arquivo | `dados_alunos.csv` (59.059 linhas, fora do repositório) |
| SHA-256 do arquivo | `A PREENCHER` |
| Regras aplicadas | as descritas nas seções 2.1 a 2.4 |

O notebook já calcula o SHA-256 do CSV na célula 3 e confere, no fim da execução, se o arquivo não mudou durante a análise. Se o hash de uma execução futura for diferente, a base não é a mesma desta versão.

A consulta usada na extração fica guardada fora do repositório, junto com a base, porque descreve a estrutura do sistema acadêmico da instituição.

---

## 3. O que analisamos antes de mudar

Antes de alterar a base, conferimos a extração com contagens agregadas. Esta seção mostra o que foi verificado e o que encontramos.

### 3.1 A base nova bate com a validada

- 59.059 linhas: 44.417 de origem acadêmica e 14.642 só de ocorrência.
- 3.841 linhas com evento de saída: 1.488 acadêmicas e 2.353 de ocorrência. Nenhuma linha tem dois tipos de saída ao mesmo tempo.
- Nenhuma linha repetida para o mesmo aluno, semestre e currículo. Toda flag tem a data correspondente.
- Contados de forma independente, os alunos com reingresso depois da primeira saída são 138, o mesmo número do notebook v2.

### 3.2 Na graduação, o evento de saída tem três tipos

**Por que olhamos:** a base tinha uma única linha com desligamento, um número que parecia baixo demais.

**Resultado:** desligamento é praticamente exclusivo da pós-graduação. Só 4 de 823 registros são de cursos de graduação, e apenas 1 cai no período e no recorte do TCC. As desistências da base (2.313) batem exatamente com as desistências das 12 siglas de graduação.

**Implicação:** na prática, o evento de saída é desistência, abandono ou cancelamento.

### 3.3 A data da ocorrência é uma data administrativa

**Por que olhamos:** para saber se a data serve para ordenar os eventos e para dizer quando o aluno saiu.

**Resultados.** Os três primeiros itens foram medidos sobre todos os registros de ocorrência, sem filtrar por curso, então também incluem a pós-graduação:

- 93,76% das datas de ocorrência não têm hora, então só dá para ordenar eventos por dia;
- nas 7.510 saídas registradas, a data de inclusão no sistema ficou no mesmo dia da data da ocorrência em 40,56% dos casos, de 1 a 30 dias depois em 29,55%, de 31 a 180 dias depois em 3,01% e mais de 180 dias depois em 26,8%. Em 6 saídas (0,08%), a inclusão é anterior à data da ocorrência;
- entre 2009/1 e 2026/1, nos tipos de ocorrência usados na base, a data da ocorrência cai fora da metade do ano correspondente ao semestre em 22,38% das ocorrências de 1º semestre e em 19,61% das de 2º semestre, quase sempre na virada entre semestres.

Comparando a data da primeira saída com o período de aulas do semestre:

| Origem | Antes do início das aulas | Durante as aulas | Após o fim | Sem calendário confiável* |
|---|---|---|---|---|
| Acadêmica (1.488) | 277 (18,62%) | 1.158 (77,82%) | 33 | 20 |
| Só ocorrência (2.353) | 794 (33,74%) | 1.546 (65,7%) | 6 | 7 |

\* No cadastro de 2009/2, o período de aulas é igual ao de 2009/1.

**Implicação:** a data serve para ordenar eventos, mas não para medir quando o aluno deixou de frequentar. No artigo, ela deve ser tratada como data de registro da saída.

### 3.4 Não há indicador acadêmico no semestre da saída

**Por que olhamos:** para saber se daria para trazer CRE, frequência e notas do próprio semestre da saída nas linhas que vêm só de ocorrência.

**Resultado:** das 2.353 linhas de saída que vêm só de ocorrência, **2.195 (93,29%) não têm nenhum dado acadêmico**. Em 684 não há registro nenhum do semestre. Nas outras 1.511 há só uma matrícula não efetivada, sem disciplinas, histórico ou CRE.

**Implicação:**

- o semestre da saída quase sempre é um semestre que o aluno não cursou, e o t−1 continua sendo o único retrato acadêmico;
- mesmo quando houver dado, o semestre da saída não deve entrar como variável do modelo, porque frequência e notas desse semestre são consequência da saída e não algo que veio antes dela.

### 3.5 A maioria das linhas de ocorrência sem saída é de outro currículo

**Resultado:** das 12.289 linhas só de ocorrência sem saída, **9.990 (81,29%)** são de alunos com matrícula efetivada em outro currículo no mesmo semestre. Na maior parte, são casos de migração de currículo ou mudança de curso, e o semestre já está na base como linha acadêmica do outro currículo.

**Implicação:** se essas linhas entrarem no modelo como semestres próprios, a base ganha milhares de semestres repetidos e sem indicador.

### 3.6 Pontos menores

- 51 pares aluno/semestre com dois currículos efetivados ao mesmo tempo. Resolvido pela correção 2.3.
- 24 ocorrências registradas em semestre anterior ao ingresso do aluno no currículo.
- Ficam fora do recorte 131 desistências de alunos que ingressaram antes de 2009/1 e 20 desistências de 2026/2.

---

## 4. Números do notebook: base antiga × base nova

Comparamos célula a célula as saídas do `pre_defesa_analise_exploratoria_v2.ipynb` (base antiga) com as do notebook novo. Mudaram as seções de eventos, sexo, amostras, CRE, frequência, contagens de disciplinas, trancamento, indicadores financeiros, indicadores socioeconômicos e trajetória. As saídas idênticas não aparecem nas tabelas abaixo.

Diferenças entre as duas bases que explicam a maior parte das mudanças:

- **correção da diplomação (2.2).** A primeira conclusão do curso decide quem pode entrar como caso e como referência. Com 240 diplomações a menos nas linhas de ocorrência, as amostras ganham alunos, e todas as comparações feitas sobre elas mudam um pouco;
- **atualização dos dados entre as extrações.** Algumas mudanças não dependem das correções (sexo e rendas, abaixo). A hipótese é que o cadastro foi atualizado entre a extração antiga e a nova, mas isso ainda não foi verificado.

### 4.1 Estrutura e eventos

| Indicador | Base antiga | Base nova |
|---|---|---|
| Registros / estudantes / semestres / cursos | 59.059 / 7.615 / 35 / 12 | igual |
| Alunos com saída / linhas positivas / pares / mais de um semestre | 3.507 / 3.841 / 3.728 / 202 | igual |
| Alunos com transferência/afastamento | 84 | **323** |
| Alunos com conclusão observada | 2.867 | **2.634** |
| Conclusão sem saída | 2.690 | **2.475** |
| Conclusão antes ou no semestre da 1ª saída | 21 | **17** |
| Conclusão após 1ª saída | 156 | **142** |
| Reingresso formal após 1ª saída / após a última saída | 138 / 68 | igual |
| Matrícula efetivada após 1ª saída | 398 | igual |
| Status final sem saída: Inativo / indefinidos / conflitos | 267 / 946 / 15 | igual |

### 4.2 Sexo

| Indicador | Base antiga | Base nova |
|---|---|---|
| Feminino: alunos / com saída / % | 1.678 / 698 / 41,597% | **1.680 / 698 / 41,548%** |
| Masculino: alunos / com saída / % | 5.928 / 2.806 / 47,335% | igual |
| Sem informação: alunos / com saída | 9 / 3 | **7 / 3** |
| χ² / p (n) | 17,098 / 3,55e-05 (7.606) | **17,413 / 3,01e-05 (7.608)** |

Sexo não depende das correções. Dois alunos passaram de "sem informação" para feminino, o que é compatível com cadastro preenchido entre as extrações.

### 4.3 Amostras de comparação

| Amostra | Base antiga | Base nova |
|---|---|---|
| Casos elegíveis antes dos estratos | 1.480 | **1.484** |
| V0: casos / referências aluno-semestre / referências pessoas / estratos | 1.464 / 16.511 / 4.915 / 595 | **1.468 / 16.697 / 4.933 / 596** |
| V1: casos / referências aluno-semestre / referências pessoas | 1.240 / 14.945 / 4.889 | **1.244 / 15.157 / 4.907** |
| V2: casos / referências aluno-semestre / referências pessoas | 1.240 / 14.651 / 4.831 | **1.244 / 14.729 / 4.834** |
| Referências V1 com matrícula confirmada em t / não confirmada | 14.651 / 294 | **14.729 / 428** |

Os casos excluídos por falta de estrato comum continuam 16, e os excluídos de V1 em relação a V0 continuam 224.

### 4.4 CRE e frequência em t−1

Valores: média dos casos / média padronizada das referências / diferença.

| Indicador | Base antiga | Base nova |
|---|---|---|
| CRE V0 (n casos / n referências) | 23,652 / 51,829 / −28,177 (1.266 / 15.042) | **23,669 / 51,727 / −28,058 (1.270 / 15.254)** |
| CRE V1 | 23,803 / 51,841 / −28,038 | **23,820 / 51,737 / −27,917** |
| CRE V2 | 23,803 / 52,308 / −28,505 | **23,820 / 52,315 / −28,495** |
| Frequência V0 (%) | 68,002 / 90,525 / −22,523 | **68,042 / 90,483 / −22,440** |
| Frequência V1 (%) | 78,908 / 90,603 / −11,695 | **78,920 / 90,566 / −11,646** |
| Frequência V2 (%) | 78,908 / 90,733 / −11,825 | **78,920 / 90,727 / −11,807** |
| Disciplinas com mais de 25% de faltas, V0 | 1,005 / 0,233 / 0,772 | **1,004 / 0,236 / 0,768** |
| Com alguma disciplina acima de 25% de faltas: casos % / referências % | 37,705 / 12,879 | **37,807 / 13,017** |

### 4.5 Contagens de disciplinas e trancamento (V0)

Valores: média dos casos / média padronizada das referências / diferença.

| Indicador | Base antiga | Base nova |
|---|---|---|
| Aprovadas registradas (`IA75_03`) | 2,278 / 4,917 / −2,639 | **2,296 / 4,927 / −2,631** |
| Reprovadas registradas (`IA34_03`) | 3,279 / 1,584 / 1,695 | **3,282 / 1,593 / 1,689** |
| Matriculadas (`IA75_04`) | 5,856 / 5,935 / −0,079 | **5,858 / 5,937 / −0,079** |
| `IA65_03` | 0,427 / 0,372 / 0,055 | **0,426 / 0,374 / 0,051** |
| Trancamento no histórico até o retrato: casos % / referências % | 16,872 / 2,371 | **16,894 / 2,365** |
| Linhas com aprovadas > matriculadas: acadêmicas | 5.388 | igual |
| Linhas com reprovadas > matriculadas: acadêmicas / ocorrência | 140 / 5.793 | **138 / 0** |

As mudanças de reprovações na comparação V0 vêm das amostras (4.3), não da correção 2.3: com a base nova, rodar o notebook antes e depois dessa correção deu a mesma comparação.

### 4.6 Indicadores financeiros (V0)

| Indicador | Base antiga | Base nova |
|---|---|---|
| Bolsa positiva entre informados: n casos / n referências | 369 / 3.419 | **369 / 3.427** |
| Bolsa positiva: casos % / referências % | 96,206 / 96,615 | **96,206 / 96,629** |
| FIES no retrato: casos % / referências % | 2,801 / 5,116 | **2,793 / 5,094** |
| Perda de FIES no retrato: casos % / referências % | 1,025 / 0,131 | **1,022 / 0,129** |
| Percentual de bolsa (`IA10_01`): casos / referências / diferença | 36,775 / 38,419 / −1,644 | **36,775 / 38,421 / −1,646** |
| Mensalidade: casos / referências (n casos / n referências) | 1.807,943 / 1.807,943 (1.417 / 15.989) | **1.807,694 / 1.807,694 (1.421 / 16.171)** |

### 4.7 Indicadores socioeconômicos

**Rendas, descrição geral da base:**

| Variável | Base antiga: linhas informadas / média | Base nova: linhas informadas / média |
|---|---|---|
| Renda da mãe (`IA70_01`) | 15.190 / 4.009,278 | 15.190 / **4.007,687** |
| Renda do estudante (`IA70_03`) | 15.190 / 1.149,233 | 15.190 / **1.148,867** |
| Renda do pai (`IA70_05`) | 15.190 / 4.017,481 | 15.190 / **4.013,288** |

O número de linhas informadas é o mesmo, mas as médias mudaram. Isso não vem das correções. É compatível com dados socioeconômicos atualizados entre as extrações, o que reforça a pendência sobre a data de coleta e a atualização retrospectiva desses dados.

**Rendas no retrato, V0** (média dos casos / média padronizada das referências / diferença):

| Variável | Base antiga | Base nova |
|---|---|---|
| Renda da mãe | 2.445,185 / 2.859,346 / −414,161 | **2.441,233 / 2.847,769 / −406,536** |
| Renda do estudante | 909,378 / 917,410 / −8,032 | **907,081 / 938,843 / −31,762** |
| Renda do pai | 2.493,372 / 3.077,317 / −583,945 | **2.495,578 / 3.061,735 / −566,157** |
| Ausência de renda: casos % / referências % | 72,746 / 66,053 | **72,752 / 66,263** |

A renda do estudante é a que mais muda em termos relativos: a diferença passa de −8,032 para −31,762. Antes de usar essa variável no artigo, vale olhar com cuidado.

O patrimônio familiar e a escolaridade da mãe e do pai também tiveram mudanças pequenas nas distribuições: a maior variação de uma categoria foi de 0,097 ponto percentual. Os valores completos estão nas células 52 e 54 dos dois notebooks.

### 4.8 Trajetória do CRE

| Painel | Base antiga: alunos / t−3 / t−2 / t−1 | Base nova: alunos / t−3 / t−2 / t−1 |
|---|---|---|
| T0 (painel completo) | 464 / 33,246 / 29,325 / 21,700 | **466 / 33,303 / 29,350 / 21,777** |
| T1 (curso estável) | 431 / 32,895 / 29,095 / 21,922 | **433 / 32,959 / 29,123 / 22,004** |
| T2 (vínculo curricular estável) | 340 / 33,493 / 29,688 / 22,422 | **342 / 33,570 / 29,719 / 22,522** |
| Queda média de t−3 a t−1 (T0 / T1 / T2) | −11,546 / −10,973 / −11,071 | **−11,526 / −10,955 / −11,047** |
| Alunos com queda (T0 / T1 / T2) | 62,716% / 61,717% / 61,471% | **62,876% / 61,894% / 61,696%** |

### 4.9 O que muda para o artigo

A direção de todas as comparações continua a mesma. Os números citados na pré-defesa e no artigo precisam ser trocados pelos da base nova. As mudanças maiores estão nas contagens de conclusão e de transferência/afastamento (4.1) e na renda do estudante (4.7).

---

## 5. Alterações no notebook

O código das células já existentes não mudou, exceto o filtro da célula 67. Comparamos as saídas célula a célula com a execução anterior: fora as diferenças desta seção e da seção 4, tudo ficou igual.

### Célula 59 — indicadores novos em relação à primeira saída (nova)

**Por quê:** para ver se cada indicador novo aparece em quem nunca saiu, antes da saída, junto com ela ou depois. É isso que diz como ele deve ser tratado.

| Ocorrência | Sem saída | Antes da 1ª saída | Mesmo semestre | Depois da 1ª saída |
|---|---|---|---|---|
| Rematrícula | 227 (214) | 105 (94) | 21 (21) | 25 (23) |
| Falecimento | 13 (13) | 0 | 0 | 1 (1) |
| Prazo esgotado | 17 (17) | 8 (8) | 0 | 1 (1) |
| Afastamento sem ocorrência | 1 (1) | 2 (1) | 0 | 183 (73) |

Valores em semestres, com o número de alunos distintos entre parênteses. Os alunos batem exatamente com a contagem feita na extração. Os semestres ficam abaixo do número de registros porque um mesmo semestre pode ter registro em mais de um currículo do aluno, e o notebook conta cada aluno/semestre uma vez.

### Célula 60 — o que vem depois do afastamento e do prazo esgotado (nova)

**Afastamento sem ocorrência depois da 1ª saída (73 alunos)**

**Por quê:** quase todo afastamento aparece depois de uma saída. Precisávamos saber se ele indica saída definitiva ou intervalo até o retorno.

- 71 têm reingresso formal depois do primeiro afastamento;
- 68 têm matrícula efetivada depois do último afastamento;
- 15 concluíram o curso depois;
- 3 ainda estavam afastados no último semestre da base (2026/1);
- em 62, o afastamento começa no semestre logo seguinte à saída;
- duração: 1 semestre para 36 alunos e 2 semestres para 15.

**Leitura:** a flag marca o intervalo entre a saída e o retorno, não uma saída definitiva.

**Prazo esgotado antes da 1ª saída (8 alunos)**

**Por quê:** se o prazo esgotado encerrasse o vínculo, não deveria vir antes de outra saída.

- a saída seguinte foi abandono em 4 alunos e desistência em 4, sem semestre com os dois tipos ao mesmo tempo;
- ela acontece de 1 a 5 semestres depois do prazo esgotado;
- 7 dos 8 tiveram matrícula entre o prazo e a saída. O único sem matrícula desistiu no semestre seguinte.

Detalhe de implementação: a tabela mostra todos os tipos de saída marcados no semestre (ex.: "ABANDONO + CANCELAMENTO"), e não só o primeiro da lista.

### Célula 61 — prazo esgotado sem nenhuma saída (nova)

**Por quê:** hoje esses alunos contam como permanência. Se o prazo esgotado encerra o vínculo, eles estariam mal classificados.

- 17 alunos têm prazo esgotado e nenhuma saída;
- 15 tiveram matrícula efetivada depois do prazo;
- 13 concluíram no semestre do prazo ou depois;
- 1 não tem nenhum registro depois do prazo;
- nenhum tem o prazo no último semestre da base.

**Leitura:** na prática, o prazo esgotado não encerra o vínculo. Hipótese ainda não verificada: houve prorrogação de prazo.

### Célula 67 — tabela de ausências (alterada; era a 64)

As colunas de data foram retiradas da tabela, porque ficam vazias por definição quando o evento não acontece e ocupavam as 20 primeiras posições. Agora o topo mostra as variáveis com ausência real (FIES, bolsa, renda familiar etc.). `IA34_03` aparece com 24,792% de nulos: são as 14.642 linhas só de ocorrência, o efeito esperado da correção 2.3.

---

## 6. Decisões

Todas as decisões abaixo entram na definição da variável-alvo e devem ser fechadas junto com a #18.

### 6.1 Em aberto (levar à orientação)

1. **Evento de saída oficial.** Assumimos desistência + abandono + cancelamento e registramos na metodologia que desligamento não ocorre na graduação (1 linha na base)?
2. **Falecimento.** 14 alunos, sendo 13 sem saída, que hoje estão entre as referências. Proposta: excluir dos dois grupos.
3. **Rematrícula.** 350 alunos, mas a maioria nunca teve saída (214) ou tem a rematrícula antes da saída (94). Só 23 têm rematrícula depois da 1ª saída. Proposta: não usar como retorno sem antes entender o que esse registro representa.
4. **Uma linha por aluno e semestre na preparação para o modelo.** As 9.990 linhas de outro currículo seriam juntadas à linha acadêmica do mesmo semestre, aproveitando só as flags (como a de migração). As linhas de saída sem matrícula ficariam apenas como marcador do evento, sem indicadores.

### 6.2 Respondidas pelos dados (confirmar com o grupo)

5. **Afastamento sem ocorrência.** É o intervalo entre a saída e o retorno: 71 de 73 alunos têm reingresso. Como quase todos já aparecem como retorno pelo reingresso, a flag muda a classificação de no máximo 2 alunos. Proposta: tratar como vínculo mantido e confirmar o significado formal com a secretaria.
6. **Prazo de integralização esgotado.** Não é saída: 13 dos 17 alunos sem saída concluíram o curso depois. Proposta: manter como está.

### 6.3 Pendências que continuam

- Linhas acadêmicas com aprovadas (`IA75_03`) maiores que matriculadas (`IA75_04`): 5.388. Faz parte da validação das contagens e não tem relação com as correções acima.
- Significado formal de rematrícula, prazo esgotado e afastamento sem ocorrência: confirmar com a secretaria acadêmica.
- Atualizar no artigo os números da seção 4.

---

## 7. O que revisar neste PR

- Se a explicação de cada correção (seção 2) está clara o suficiente para entrar na metodologia.
- Se as leituras das células 60 e 61 fazem sentido.
- As decisões da seção 6: concordar, discordar ou propor outra saída.
- Os números da seção 4 que vão substituir os da pré-defesa.
