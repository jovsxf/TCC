# Temporalidade dos campos: quando cada informação é conhecida em relação à saída (#51)

O modelo não pode usar informação que só existe depois da saída. Este relatório verifica, na base v3 (`Base_academica_v3.csv`), **quando cada campo da base é conhecido** e lista os campos que não podem entrar no modelo por vazamento (para a #26).

As análises estão no notebook `temporalidade_campos_v3.ipynb`, executado sobre a base v3 (SHA-256 `9CCE803735488354B820F9B1976612AB9D1DE5950EDB91BE57F85C415D6A2343`). Todos os números são agregados.

> **Atualização (27/10/2026):** a análise levou a uma correção na frequência, aplicada na base v4 (`Base_academica_v4.csv`). As seções 2 a 8 descrevem a base v3. O resultado da correção e o que mudou na v4 estão na seção 10.

**Termos usados:**

- **semestre da saída (t):** o semestre da primeira saída do aluno;
- **t−1:** o semestre imediatamente anterior;
- **evento de saída:** desistência, abandono, cancelamento ou desligamento. Não equivale a evasão definitiva.

---

## 1. Resumo

- **A situação do aluno (`STATUSALUNO`) não pode entrar no modelo, nem em t−1.** Ela é o retrato do fim do semestre: no semestre da saída, 99,93% das linhas estão como "Inativo". Em t−1, 14,24% já estão como "Inativo", contra 2,24% nos semestres mais antigos de quem saiu e 0,62% nos semestres de quem nunca saiu.
- **No semestre da saída, os indicadores de desempenho não descrevem o semestre.** O CRE do semestre está preenchido em só 4,30% das linhas. Frequência, aprovadas e reprovadas vêm zeradas. Em 96,57% das linhas acadêmicas com saída, o aluno tinha disciplinas matriculadas, mas nenhum resultado no semestre.
- **A frequência zero (`IA04_01` = 0) não era frequência zero.** Na v3, ela aparecia quando o aluno não tinha nenhuma turma ativa no semestre: em 100% das linhas do semestre da saída e em 14,44% das linhas de t−1. **Corrigido na base v4** (seção 10): a frequência agora fica vazia nesses casos, e a diferença de frequência entre casos e referências caiu de −22,440 para −11,446 pontos.
- **Para cerca de 14% dos casos, t−1 já mostra o aluno parado.** A proporção de "Inativo" em t−1 (14,24%) é parecida com a de t−1 sem turma ativa (14,44%) e reforça a leitura de que, para parte dos alunos, a saída de fato acontece em t−1 e só é registrada em t. Isso entra na definição da variável-alvo (#18).
- **Na graduação, a data da saída é lançada no sistema quase sempre a tempo.** 96,95% das saídas foram lançadas em até 30 dias. O número de 26,8% com mais de 180 dias, citado no relatório da base v2, incluía a pós-graduação.
- **Dentro do semestre, as movimentações administrativas vêm antes da saída.** Migração de currículo, rematrícula, reingresso e mudança de curso, quando aparecem junto com uma saída no mesmo semestre, vêm antes dela.

---

## 2. A situação do aluno é atualizada depois?

**Por que conferimos.** Se a situação de um semestre for atualizada depois que o aluno sai, ela carrega informação do futuro. Usá-la seria vazamento, mesmo em t−1.

**Situação do aluno nas linhas acadêmicas, por grupo:**

| Grupo | Linhas | Ativo | Inativo | Desconhecido | Matrícula pendente |
|---|---|---|---|---|---|
| Semestre da saída | 1.488 | 0,07% | **99,93%** | 0,00% | 0,00% |
| Semestre anterior à saída (t−1) | 1.489 | 84,49% | **14,24%** | 1,01% | 0,27% |
| Semestres mais antigos de quem saiu | 5.133 | 96,59% | 2,24% | 1,11% | 0,06% |
| Alunos sem saída | 34.131 | 98,84% | 0,62% | 0,50% | 0,03% |
| Depois da primeira saída | 2.176 | 97,61% | 2,07% | 0,23% | 0,09% |

**Situação × matrícula no semestre seguinte** (sem o último semestre da base):

| Situação | Linhas | Com matrícula efetivada no semestre seguinte |
|---|---|---|
| Ativo | 40.680 | 88,69% |
| Inativo | 2.007 | 10,96% |
| Desconhecido | 249 | 94,78% |
| Matrícula pendente | 16 | 56,25% |

**Leitura.**

- A situação é o retrato do semestre **no fim** dele, ou depois. No semestre da saída ela praticamente repete o evento de saída.
- Em t−1, "Inativo" é cerca de 6 vezes mais frequente do que nos semestres mais antigos de quem saiu. E "Inativo" separa fortemente quem continua de quem não continua: só 10,96% têm matrícula no semestre seguinte.
- Os dados não permitem distinguir se a situação é marcada no fim do semestre (porque o aluno parou de cursar) ou atualizada depois da saída. Nos dois casos, ela já descreve a decisão de sair.

**Consequência.** `STATUSALUNO` e `CODIGOSTATUSALUNO` não entram no modelo como variáveis explicativas. As análises V1 e V2 do notebook exploratório usam a situação "Ativo" em t−1 como filtro. Elas continuam válidas como sensibilidade, mas é preciso registrar que esse filtro tira justamente os casos em que a saída já aparece em t−1.

## 3. CRE, frequência e disciplinas no semestre da saída

**Por que conferimos.** Os indicadores de desempenho só fecham no fim do semestre. Se o aluno sai no meio, os valores desse semestre podem estar vazios, zerados ou incompletos por causa da própria saída.

**Preenchimento, zeros e média, por grupo (linhas acadêmicas):**

| Indicador | Semestre da saída | t−1 | Semestres mais antigos | Alunos sem saída |
|---|---|---|---|---|
| CRE no semestre: preenchido | **4,30%** | 86,23% | 97,86% | 99,46% |
| CRE no semestre: zeros entre os preenchidos | 35,94% | 20,79% | 6,89% | 1,32% |
| CRE acumulado: preenchido | **47,04%** | 90,46% | 98,62% | 99,68% |
| CRE acumulado: zeros entre os preenchidos | 77,14% | 8,31% | 1,24% | 0,17% |
| Frequência: zeros (na v4, vazia) | **100,00%** | 14,44% | 2,55% | 0,74% |
| Disciplinas aprovadas: zeros | **98,45%** | 58,90% | 27,78% | 5,33% |
| Disciplinas reprovadas: zeros | **100,00%** | 21,29% | 20,69% | 57,13% |
| Disciplinas matriculadas: média | 4,67 | 4,85 | 5,04 | 5,76 |
| Disciplinas aprovadas: média | 0,03 | 0,94 | 2,09 | 4,28 |
| Disciplinas reprovadas: média | 0,00 | 2,79 | 2,27 | 0,92 |
| Disciplinas retiradas/canceladas: média | 0,15 | 0,41 | 0,52 | 0,32 |
| Atividades complementares matriculadas: média | 1,07 | 1,00 | 1,01 | 1,21 |

**O semestre da saída foi cursado?** Das 1.488 linhas acadêmicas com saída:

| Situação | Linhas | % |
|---|---|---|
| Com disciplinas matriculadas, CRE vazio ou zero | 1.437 | 96,57% |
| Com disciplinas e CRE positivo | 41 | 2,76% |
| Sem disciplina matriculada | 10 | 0,67% |

**Leitura.**

- No semestre da saída, o aluno costuma estar matriculado em disciplinas, mas sai antes de ter resultado. CRE, frequência, aprovadas e reprovadas desse semestre não descrevem o desempenho: descrevem a saída.
- **A frequência zero era um artefato.** A frequência só é calculada sobre as turmas em que o aluno está ativo. Sem nenhuma turma ativa, na v3 ela vinha como 0, e não vazia. É o que acontecia em 100% das linhas do semestre da saída. Na v4, ela fica vazia (seção 10).
- **Em t−1, a mesma marca aparecia em 14,44% das linhas.** Também em t−1, 58,90% das linhas têm zero aprovadas e 20,79% dos CRE preenchidos são zero. A proporção sem turma ativa é parecida com a de "Inativo" em t−1 (14,24%). Isso sugere que, para esses alunos, o abandono de fato já aconteceu em t−1. A sobreposição entre os dois grupos ainda não foi medida linha a linha, mas a seção 10 traz um indício indireto.
- As linhas que vêm só de ocorrência não têm esses indicadores (ficam vazias). Na base v2, 93,29% das linhas de saída vindas só de ocorrência não tinham dado acadêmico nenhum.

## 4. Datas das ocorrências

**Por que conferimos.** As flags dizem a que semestre a ocorrência está ligada, mas não quando ela aconteceu.

**4.1 Lançamento da saída no sistema (só graduação):**

| Intervalo entre a data da saída e o lançamento | Linhas | % |
|---|---|---|
| Lançamento antes da data da saída | 2 | 0,05% |
| Mesmo dia | 1.805 | 46,99% |
| 1 a 30 dias depois | 1.919 | 49,96% |
| 31 a 180 dias depois | 105 | 2,73% |
| Mais de 180 dias depois | 10 | 0,26% |

Na graduação, 96,95% das saídas são lançadas em até 30 dias. A medida do `relatorio_alteracoes_base_v2.md` (26,8% com mais de 180 dias) foi feita sobre todos os registros do sistema, inclusive a pós-graduação, e não vale para a base do TCC.

**4.2 Data da ocorrência × metade do ano do semestre** (janeiro a junho para o 1º semestre, julho a dezembro para o 2º; aproximação, sem o calendário de aulas):

| Ocorrência | Linhas | Antes | Dentro | Depois |
|---|---|---|---|---|
| Desistência | 2.313 | 3,46% | 95,68% | 0,86% |
| Abandono | 761 | 0,00% | 100,00% | 0,00% |
| Cancelamento | 766 | 12,92% | 86,81% | 0,26% |
| Desligamento | 1 | 0,00% | 100,00% | 0,00% |
| Trancamento | 1.727 | 7,53% | 92,30% | 0,17% |
| Transferência/afastamento | 325 | 5,54% | 93,85% | 0,62% |
| Afastamento sem ocorrência | 331 | 0,60% | 7,55% | **91,84%** |
| Reingresso | 253 | 12,25% | 87,75% | 0,00% |
| Rematrícula | 593 | 17,20% | 82,63% | 0,17% |
| Mudança de curso | 892 | 0,11% | 99,89% | 0,00% |
| Migração de currículo | 4.445 | 18,20% | 81,80% | 0,00% |
| Diplomação | 2.644 | 0,00% | 27,95% | **72,05%** |
| Prazo esgotado | 26 | 0,00% | 50,00% | 50,00% |
| Falecimento | 15 | 6,67% | 93,33% | 0,00% |

**Leitura.**

- As saídas e os trancamentos ficam quase sempre dentro do semestre a que estão ligados.
- Uma parte de cancelamentos (12,92%) e trancamentos (7,53%) tem data anterior ao semestre: são pedidos feitos nas férias e ligados ao semestre seguinte. O aluno sai antes de começar a cursar.
- O afastamento sem ocorrência (91,84%) e a diplomação (72,05%) são registrados **depois** do semestre a que estão ligados. A diplomação, por exemplo, é lançada depois da colação.
- Nenhuma data tem hora, então eventos do mesmo dia não podem ser ordenados.

## 5. Ordem dos eventos no mesmo semestre

**Por que conferimos.** Quando há mais de uma ocorrência no mesmo semestre, só as flags não dizem qual veio primeiro.

**Pares que aparecem juntos no mesmo aluno/semestre** (ocorrências de todos os currículos do aluno; para cada tipo, a primeira data):

| Evento A | Evento B | Aluno-semestres | A antes de B | Mesmo dia | A depois de B |
|---|---|---|---|---|---|
| Saída | Migração de currículo | 136 | 2 | 0 | 134 |
| Trancamento | Migração de currículo | 123 | 4 | 1 | 118 |
| Migração de currículo | Diplomação | 122 | 122 | 0 | 0 |
| Rematrícula | Migração de currículo | 68 | 37 | 31 | 0 |
| Reingresso | Migração de currículo | 46 | 22 | 24 | 0 |
| Transferência/afastamento | Migração de currículo | 34 | 1 | 0 | 33 |
| Saída | Rematrícula | 23 | 0 | 0 | 23 |
| Rematrícula | Mudança de curso | 22 | 18 | 4 | 0 |
| Trancamento | Rematrícula | 21 | 0 | 0 | 21 |
| Reingresso | Mudança de curso | 17 | 11 | 6 | 0 |
| Saída | Reingresso | 17 | 0 | 0 | 17 |
| Saída | Mudança de curso | 16 | 0 | 0 | 16 |
| Rematrícula | Diplomação | 13 | 13 | 0 | 0 |
| Trancamento | Mudança de curso | 11 | 0 | 0 | 11 |
| Mudança de curso | Migração de currículo | 9 | 0 | 1 | 8 |
| Trancamento | Reingresso | 8 | 0 | 1 | 7 |
| Reingresso | Diplomação | 4 | 4 | 0 | 0 |
| Migração de currículo | Prazo esgotado | 3 | 3 | 0 | 0 |
| Transferência/afastamento | Reingresso | 3 | 0 | 0 | 3 |
| Saída | Trancamento | 2 | 2 | 0 | 0 |
| Trancamento | Prazo esgotado | 2 | 1 | 0 | 1 |
| Transferência/afastamento | Mudança de curso | 1 | 0 | 0 | 1 |
| Diplomação | Prazo esgotado | 1 | 0 | 0 | 1 |

**Mais de um tipo de saída no mesmo semestre:** só 5 aluno-semestres, todos com desistência e cancelamento. Nos 5, o cancelamento veio antes da desistência.

**Leitura.**

- **A ordem é bem definida.** Primeiro vêm as movimentações administrativas do início do semestre (rematrícula, reingresso, mudança de curso, migração de currículo). Depois vêm a saída, o trancamento ou a transferência. Por último, a diplomação.
- **Saída e trancamento quase nunca aparecem no mesmo semestre** (2 casos). O exemplo da issue, trancamento seguido de cancelamento no mesmo semestre, não ocorre na base.
- **Reingresso e saída no mesmo semestre** (17 casos): o reingresso vem sempre antes. É o aluno que volta e sai de novo no mesmo semestre. Isso entra na discussão de episódios da #18.
- **Saída depois de migração de currículo** (134 casos): a migração abre o semestre e a saída vem depois, no mesmo semestre.

## 6. Quando cada campo é conhecido

**Momentos:**

- **Antes do semestre:** conhecido no ingresso ou no cadastro.
- **Início do semestre:** conhecido na matrícula.
- **Fim do semestre:** só fecha quando o semestre termina.
- **Pode mudar depois:** pode ser atualizado depois do fim do semestre.

**Uso no modelo:** o desenho atual descreve o aluno em t−1 para explicar a saída em t. A coluna "Em t" vale para um eventual modelo que use informação do próprio semestre da saída.

| Campo | O que é | Quando é conhecido | Em t | Em t−1 | Observação |
|---|---|---|---|---|---|
| `SEXO` | Sexo | Antes do semestre | Sim | Sim | O cadastro pode ser atualizado: entre as bases v1 e v2, 2 alunos deixaram de estar sem informação |
| `INGRESSO`, `SIGLACURSO`, `TURNO` | Ingresso, curso e turno | Antes do semestre | Sim | Sim | Curso e turno mudam com mudança de curso ou migração |
| `APROVEIT` | Semestres aproveitados | Antes do semestre | Sim | Sim | Muda com migração ou mudança de curso |
| `PERIODO` | Período curricular | Início do semestre | Sim | Sim | — |
| `MATRICULAEFETIVADA`, `ORIGEMREGISTRO` | Matrícula efetivada e origem da linha | Início do semestre | **Não** | Sim | Em t, a falta de matrícula é a própria saída |
| `STATUSALUNO`, `CODIGOSTATUSALUNO` | Situação do aluno | Fim do semestre, ou depois | **Não** | **Não** | 99,93% "Inativo" em t; 14,24% "Inativo" em t−1 (seção 2) |
| `CRENOSEMESTRE` | CRE no semestre | Fim do semestre | **Não** | Sim | Em t, preenchido em 4,30% das linhas |
| `CREATESEMESTRE`, `MEDIANAATESEMESTRE` | CRE e mediana acumulados | Fim do semestre | **Não** | Sim | Em t, preenchido em 47,04%, e 77,14% dos preenchidos são zero |
| `IA04_01`, `IA04_02` | Frequência e disciplinas com >25% de faltas | Fim do semestre | **Não** | Sim | Na v4, vazia quando o aluno não tem turma ativa (seção 10) |
| `IA75_04`, `ATIVCOMPL_MATRICULADAS` | Disciplinas e atividades matriculadas | Início do semestre | Possível | Sim | Em t, o aluno costuma estar matriculado (média 4,67) |
| `IA75_03`, `IA34_03`, `IA65_03` | Aprovadas, reprovadas, retiradas | Fim do semestre | **Não** | Sim | Em t, 98,45% zero aprovadas e 100% zero reprovadas |
| `ATIVCOMPL_APROVADAS`, `ATIVCOMPL_REPROVADAS` | Resultado das atividades complementares | Fim do semestre | **Não** | Sim | Mesma lógica das disciplinas |
| `IA75_01`, `IA75_05` | Exigidas pela grade e previstas no período | Antes ou início do semestre | Sim | Sim | Dependem só da grade e do período |
| `IA75_02` | Concluídas acumuladas | Fim do semestre | **Não** | Sim | Em t, inclui o próprio semestre da saída |
| `VALORMENSALIDADE` | Mensalidade | Início do semestre | Sim | Sim | — |
| `IA12`, `IA12_01` | FIES no contrato do semestre | Início do semestre | **Não** | Sim | Em t, a falta de contrato pode ser consequência da saída |
| `IA13` | Perda de FIES (t−1 → t) | Início do semestre | **Não** | Sim | Em t, a perda pode ser consequência da saída |
| `IA09`, `IA09_02`, `IA10_01` | Bolsa negada, motivo e percentual concedido | Início do semestre | **Não** | Sim | Em t, a ausência de processo pode refletir a decisão de sair |
| `IA70_01` a `IA70_06` | Renda, escolaridade e patrimônio declarados | Início do semestre (processo de bolsa) | **Não** | Sim, com ressalva | Valores mudaram entre extrações com o mesmo número de linhas: podem ser atualizados depois |
| Flags de saída, trancamento e transferência (`TEVE*`) | Ocorrências do semestre | Durante o semestre, às vezes nas férias antes dele | **Não** | Sim, as de semestres anteriores | Em t, são o próprio desfecho ou o que acontece junto com ele |
| `TEVEREINGRESSO`, `TEVEREMATRICULA`, `TEVEMUDANCACURSO`, `TEVEMIGRACAOCURRICULO` | Movimentações administrativas | Início do semestre | Com cuidado | Sim | Vêm antes da saída no mesmo semestre (seção 5) |
| `TEVEAFASTAMENTOSEMOCORRENCIA`, `TEVEDIPLOMACAO` | Afastamento e diplomação | Depois do semestre | **Não** | **Não** | 91,84% e 72,05% registrados depois do semestre |
| `TEVEPRAZOESGOTADO`, `TEVEFALECIMENTO` | Prazo esgotado e falecimento | Durante o semestre | **Não** | Decisão da #18 | Usados para exclusão ou definição do alvo, não como variáveis |
| `QUANTIDADEOCORRENCIAS` | Ocorrências do semestre | Durante o semestre | **Não** | Com cuidado | Mistura tipos de antes e de depois da saída |
| `DATA*` | Datas das ocorrências | Durante ou depois do semestre | **Não** | **Não** | Servem só para ordenar eventos; nunca como variável |

**Correção da frequência (feita na base v4).** Na v3, `IA04_01` e `IA04_02` vinham como 0 quando o aluno não tinha nenhuma turma ativa no semestre. Na v4, ficam vazios nesse caso, como os indicadores das linhas que vêm só de ocorrência. O efeito está na seção 10.

## 7. Lista de vazamento para a #26

**Nunca entram no modelo:**

- `STATUSALUNO` e `CODIGOSTATUSALUNO`, em qualquer semestre;
- todas as colunas de data (`DATA*`), inclusive `DATAINCLUSAOSAIDA`;
- `TEVEAFASTAMENTOSEMOCORRENCIA` e `TEVEDIPLOMACAO`, porque são registrados depois do semestre.

**Não entram quando forem do semestre da saída (t) ou posteriores:**

- `MATRICULAEFETIVADA` e `ORIGEMREGISTRO`;
- `CRENOSEMESTRE`, `CREATESEMESTRE` e `MEDIANAATESEMESTRE`;
- `IA04_01` e `IA04_02`;
- `IA75_02`, `IA75_03`, `IA34_03` e `IA65_03`;
- `ATIVCOMPL_APROVADAS` e `ATIVCOMPL_REPROVADAS`;
- `IA12`, `IA12_01`, `IA13`, `IA09`, `IA09_02`, `IA10_01` e `IA70_01` a `IA70_06`;
- todas as flags `TEVE*` e `QUANTIDADEOCORRENCIAS`.

**Entram com ressalva:**

- `IA04_01` e `IA04_02` em t−1, usando a base v4 (ou, nas bases anteriores, tratando o 0 como ausente);
- `IA70_*`, que podem ter sido atualizados depois da coleta;
- `SEXO`, `SIGLACURSO`, `TURNO` e `APROVEIT`, que podem mudar com atualização de cadastro, mudança de curso ou migração.

## 8. O que isso muda na #18

- **t−1 nem sempre é "antes da saída".** Em cerca de 14% dos casos, t−1 já mostra o aluno parado ("Inativo", sem turma ativa, sem aprovação). A saída de fato pode ter acontecido em t−1 e só ter sido registrada em t. Opções para levar à orientação:
  - manter t−1 e registrar a limitação;
  - usar o último semestre com o aluno cursando (por exemplo, t−2 para esses casos);
  - tratar como sensibilidade, como a V1 já faz ao exigir "Ativo" em t−1.
- **A data da saída é confiável para ordenar eventos na graduação.** Ela é lançada em até 30 dias em 96,95% dos casos. Ainda assim, não indica o dia em que o aluno parou de frequentar.
- **Episódios:** os 17 casos de reingresso e saída no mesmo semestre mostram que um aluno pode voltar e sair de novo dentro de um semestre só.
- **Saídas antes de cursar:** 12,92% dos cancelamentos e 7,53% dos trancamentos têm data anterior ao início do semestre a que estão ligados.

## 9. Pendências

- ~~Aplicar a correção da frequência e rodar de novo a análise exploratória.~~ Feito na base v4 (seção 10).
- Medir, linha a linha, a sobreposição entre "Inativo" em t−1 e t−1 sem turma ativa.
- Atualizar a legenda com a informação de que, na graduação, 96,95% das saídas são lançadas em até 30 dias.

---

## 10. Correção da frequência: base v4

**O que mudou.** A base v4 (`Base_academica_v4.csv`) foi extraída só com a correção da frequência. Colunas, número de linhas e ordem são os mesmos da v3. Mudaram apenas `IA04_01` e `IA04_02`: em 2.136 linhas acadêmicas, o valor passou de 0 para vazio.

| Item | Valor |
|---|---|
| Data da extração | 27/10/2026 |
| Arquivo | `Base_academica_v4.csv` (59.059 linhas) |
| SHA-256 | `A37D9F2F12CB0A19DF1011BE6BA61D64E644A4C01717714DCD0B62C782DE3646` |
| Única mudança em relação à v3 | `IA04_01` e `IA04_02` vazios quando o aluno não tem turma ativa no semestre |

Na v4, uma única linha continua com frequência 0. Pela regra nova, isso só acontece se o aluno tem turma ativa e faltou a todas as aulas. Ainda não conferimos esse caso.

Os dois notebooks foram executados de novo na v4, com o mesmo código, sem erros:

- `temporalidade_campos_v4.ipynb`;
- `pre_defesa_analise_exploratoria_v2_base_v4.ipynb`.

O notebook de temporalidade avisa que o arquivo não é a v3. É o esperado, porque a conferência compara com o hash da v3.

### 10.1 Temporalidade (seção 3, na v4)

| Indicador | Semestre da saída | t−1 | Semestres mais antigos | Alunos sem saída |
|---|---|---|---|---|
| Frequência: preenchida | 0,00% | 85,56% | 97,45% | 99,26% |
| Frequência: zeros entre as preenchidas | — | 0,00% | 0,00% | 0,00% |
| Frequência: média | — | 79,33 | 85,18 | 92,28 |
| Disciplinas com >25% de faltas: média | — | 1,17 | 0,60 | 0,15 |

No semestre da saída, a frequência agora fica vazia em todas as linhas, em vez de vir zerada. Em t−1, 14,44% das linhas ficaram sem frequência: os mesmos 14,44% que antes vinham zerados. Nenhuma outra tabela do notebook mudou.

### 10.2 Análise exploratória

Mudaram 5 células, todas sobre frequência. Saídas, CRE, disciplinas, finanças, perfil, trajetória e as células 59 a 61 ficaram iguais.

**Frequência em t−1** (média dos casos / média padronizada das referências / diferença):

| Versão | Base v3 | Base v4 |
|---|---|---|
| V0 | 68,042 / 90,483 / −22,440 (1.468 casos) | **79,275 / 90,721 / −11,446** (1.260 casos) |
| V1 | 78,920 / 90,566 / −11,646 (1.244 casos) | **79,302 / 90,675 / −11,372** (1.238 casos) |
| V2 | 78,920 / 90,727 / −11,807 (1.244 casos) | **79,302 / 90,835 / −11,533** (1.238 casos) |

**Disciplinas com mais de 25% de faltas (V0):**

| | Base v3 | Base v4 |
|---|---|---|
| Média: casos / referências / diferença | 1,004 / 0,236 / 0,768 | **1,170 / 0,225 / 0,945** |
| Com alguma disciplina acima de 25%: casos / referências | 37,807% / 13,017% | **44,048% / 12,586%** |

**Leitura.**

- **A diferença de frequência na comparação principal (V0) caiu pela metade**, de −22,440 para −11,446 pontos. Parte da diferença da v3 vinha dos zeros de quem não tinha turma ativa.
- **O resultado principal agora é quase igual ao das variantes V1 e V2**, que exigem situação "Ativo" em t−1. Na v3, só elas descartavam esses alunos. É um indício indireto de que os casos sem turma ativa em t−1 são, em boa parte, os mesmos com situação "Inativo" em t−1.
- **A direção não muda:** antes da saída, os casos têm frequência menor que as referências e mais disciplinas com faltas acima de 25%.
- Essas diferenças são descritivas e não indicam causa.

**Amostra da comparação de frequência.** Os casos com frequência informada caíram de 1.468 para 1.260: 208 ficaram sem valor. Com isso, a coluna `refs_informadas_fora_suporte` passou de 0 para 1.520. Isso é esperado e não indica erro:

- a comparação é padronizada por semestre, curso e período, e só usa estratos com pelo menos um caso e uma referência informados;
- os 208 casos sem frequência deixaram 62 estratos sem nenhum caso informado (de 596 para 534);
- as 1.520 referências desses estratos ficam fora da comparação de frequência, porque não há caso com quem compará-las.

Na v3 isso não acontecia, porque todos os casos tinham frequência, mesmo que fosse um 0 artificial. A comparação de frequência da v4 vale para o subconjunto de 1.260 casos e 15.153 referências.

**Validação numérica:** `IA04_01` e `IA04_02` passaram de 14.642 nulos (24,792% das linhas) para 16.778 (28,409%). A diferença é de 2.136 linhas.

