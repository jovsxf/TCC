# Correções nos indicadores de disciplinas: o que mudou, por quê e como chegamos nisso

Este relatório registra a segunda rodada de conferência da base, feita em 24/10/2026. Ela começou com uma pendência do relatório anterior (`relatorio_alteracoes_base_v2.md`): **5.388 linhas acadêmicas tinham mais disciplinas aprovadas do que matriculadas no semestre**, o que é impossível.

Investigar essa inconsistência levou a revisar todos os indicadores de disciplinas da base. Todos os números abaixo vêm de contagens agregadas feitas no sistema acadêmico. Nenhum deles identifica aluno. As consultas de conferência ficam guardadas fora do repositório, junto com a base.

A base foi reextraída com as correções e o notebook foi rodado de novo sobre ela. A base nova é a **`Base_academica_v3.csv`**, junto com a **legenda v2**. As duas estão na pasta compartilhada do grupo, fora do repositório. O resultado está nas seções 8 a 11. O notebook executado é o `pre_defesa_analise_exploratoria_v2_base_v3_legenda_v2.ipynb`.

---

## 1. Resumo

| Indicador | O que mede | O que mudou |
|---|---|---|
| `IA75_01` | Disciplinas exigidas pela grade | Passa a usar o critério de integralização, e não uma lista de categorias |
| `IA75_02` | Disciplinas concluídas, acumulado | Mesmo critério de `IA75_01`, e o acumulado deixa de voltar a zero |
| `IA75_03` | Disciplinas aprovadas no semestre | Só conta disciplinas cursadas em turma no semestre, sem atividade complementar |
| `IA75_04` | Disciplinas matriculadas no semestre | Mesmas categorias das aprovadas, sem atividade complementar |
| `IA75_05` | Disciplinas previstas para o período | Mesmo critério de `IA75_01` |
| `IA34_03` | Disciplinas reprovadas no semestre | Mesmas categorias das aprovadas, sem atividade complementar, só do currículo do aluno |
| `IA65_03` | Disciplinas retiradas ou canceladas pelo aluno no semestre | Igual a `IA34_03` |
| `ATIVCOMPL_*` (novos) | Atividades complementares matriculadas, aprovadas e reprovadas no semestre | Indicadores novos |
| `IA75_01` a `IA75_05` | — | Vazios nas linhas que vêm só de ocorrência, como os demais indicadores que dependem de matrícula |

---

## 2. Ponto de partida: aprovadas maiores que matriculadas

**Por que conferimos.** Se um aluno aparece com mais disciplinas aprovadas do que matriculadas, pelo menos uma das duas contagens está errada. As duas entram na comparação entre casos e referências e entrariam no modelo.

**O tamanho do problema.** Eram 5.388 das 44.417 linhas acadêmicas (12,13%). Não era um erro de uma disciplina a mais:

| Quanto as aprovadas passavam das matriculadas | Linhas |
|---|---|
| Nenhuma matriculada | 254 |
| 1 disciplina | 148 |
| 2 a 3 disciplinas | 316 |
| Mais de 3 disciplinas | 4.670 |

**Primeiras pistas:**

- **Não era aproveitamento no ingresso.** No 1º período, só 2,29% das linhas estavam inconsistentes. O problema se concentrava do 3º ao 7º período.
- **Concentração em poucos semestres.** Em 2016/1, eram 75,11% das linhas. Em 2026/1, 50,34%; em 2014/1, 38,66%; em 2016/2, 20,08%; em 2020/1, 19,51%. Nos demais semestres desde 2011/2, o percentual ficava entre 1,79% e 11,36%. Um salto assim sugere um evento em massa, e não um erro espalhado.

## 3. A causa: disciplinas relançadas na migração de currículo

**Hipótese.** Quando o aluno migra de currículo ou muda de curso, as disciplinas que ele já tinha cursado são relançadas no histórico do novo currículo, naquele semestre, como aprovadas. Elas entravam nas aprovadas do semestre, mas não têm turma naquele semestre, então não entravam nas matriculadas.

**Como testamos.**

1. **Cruzamento com migração e mudança de curso.** Das 5.388 linhas inconsistentes, 3.987 (74,0%) tinham migração de currículo no semestre, 759 (14,09%) tinham mudança de curso, 94 tinham currículo diferente do semestre anterior e só 548 eram do mesmo currículo. Nas linhas sem inconsistência, 98,6% eram do mesmo currículo.
2. **Quantas disciplinas do histórico tinham turma no semestre.** Nas linhas inconsistentes, o histórico tinha em média 29,72 disciplinas aprovadas por semestre, contra 4,65 nas demais. Dessas, 82,41% não tinham turma correspondente no semestre, embora o aluno tivesse outras turmas. Contando só as disciplinas com turma, as linhas inconsistentes ficavam com 5,22 por semestre, no mesmo patamar das demais (4,62). Nenhuma disciplina tinha só turma de laboratório.
3. **Se o próprio histórico identificava os relançamentos.** Ele tem campos de forma de lançamento e de motivo de aproveitamento (o mais comum é "Aproveitamento por Migração"). Mas 71,08% dos lançamentos sem turma, nas linhas inconsistentes, estavam registrados exatamente como uma disciplina cursada normalmente. Esses campos não bastam para separar os casos.

**Correção.** A partir de agora, uma disciplina só conta como **aprovada no semestre** se o aluno teve turma dela naquele semestre. O que foi relançado na migração deixa de contar como aprovação do semestre.

**Confirmamos também o que "aprovada" significa.** O histórico só tem notas de 50 a 100, ou o registro "APR". Nenhuma nota é menor que 50. Com a instituição, confirmamos que a nota mínima é 60 para aprovação direta e 50 com NP3, e que a situação da disciplina na turma pode ser pendente, aprovada ou reprovada. Ou seja, o histórico só guarda aprovações, e o indicador conta aprovações de fato.

## 4. Concluídas acumuladas: o acumulado voltava a zero

**Por que conferimos.** Ao testar a regra nova do total exigido (seção 5), recalculamos o acumulado de concluídas e os valores não bateram com a base, mesmo com a mesma regra: 19,005 de média na base contra 19,615 no recálculo.

**O que estava errado.** A soma corrida das disciplinas concluídas só era calculada nos semestres em que o aluno teve pelo menos uma conclusão. Num semestre sem nenhuma aprovação, o acumulado aparecia como 0, em vez de repetir o valor anterior. Esse é justamente o tipo de semestre que tende a anteceder uma saída, então o erro pesaria no semestre anterior à saída dos casos.

**Correção.** O acumulado passou a ser calculado sobre todos os semestres do aluno no currículo, em ordem de semestre.

**Por que o relançamento continua contando aqui.** Ao contrário das aprovadas do semestre, no acumulado as disciplinas relançadas na migração continuam valendo. Elas representam o progresso que o aluno leva para o novo currículo.

## 5. O que a grade exige: do critério de categoria ao critério de integralização

**Por que conferimos.** Os indicadores usavam listas de categorias diferentes. Os da grade (`IA75_01`, `IA75_02`, `IA75_05`) usavam a Eletiva, e as aprovadas usavam a Pré-Eletiva. Precisávamos saber se isso era um erro.

**O que encontramos nas categorias.**

- **Eletiva e Pré-Eletiva têm papéis diferentes.** A grade tem cerca de 2 Eletivas por currículo (88 em 44 currículos) e cerca de 55 Pré-Eletivas (2.191 em 40). A Eletiva é a vaga obrigatória, e a Pré-Eletiva é o cardápio de opções que preenche essa vaga. Nenhuma matrícula em turma é de Eletiva, e 2.841 são de Pré-Eletiva. A diferença entre os filtros era intencional.
- **A categoria Qualificada não entrava em nenhum indicador.** Ela existe em 24 currículos de 7 cursos, nas linhas de 2023/1 a 2026/1. Isso cobre 4.977 linhas acadêmicas (11,21%) e 1.653 alunos (21,71%). São atividades como Trilha, Comportamento Profissional e Feira Tecnológica, todas cadastradas como obrigatórias para a integralização.

**O critério de integralização resolve isso de forma mais direta.** Cada disciplina da grade tem um critério de integralização que diz se ela é obrigatória. A conferência mostrou que:

- **O critério está preenchido em todas as disciplinas de todos os currículos da base, de 2009 a 2026.** O receio de que os currículos antigos estivessem sem critério não se confirmou.
- **A categoria "Normal" continha 711 atividades complementares obrigatórias**, em 64 currículos, contadas como disciplinas exigidas pela grade.
- **Havia disciplinas obrigatórias em categorias que ficavam de fora:** 35 Isoladas (7 currículos), 6 de Educação Física (3), 4 Pré-Eletivas (2) e algumas Optativas em um currículo.
- **O critério confirma a leitura das eletivas:** a Eletiva é "obrigatória e eletiva", e a Pré-Eletiva é "atividade extracurricular", que não é obrigatória.

Comparando currículo a currículo, as duas regras davam o mesmo total em 67 currículos, e o critério dava de 1 a 21 disciplinas a mais em 13.

**Correção.** O total exigido, as concluídas acumuladas e as previstas no período passam a contar as disciplinas com critério obrigatório, **exceto a atividade complementar obrigatória**, que não é disciplina. A Qualificada entra, porque é obrigatória. As previstas no período também passaram a desconsiderar as partes de disciplina, como os outros dois indicadores já faziam.

**Teste de coerência.** Pela regra nova, nenhuma linha tem mais concluídas do que exigidas, e nenhuma fica sem total exigido.

## 6. Indicadores do semestre: o mesmo conjunto para todos

**Por que conferimos.** Aprovadas, matriculadas e reprovadas precisam olhar para o mesmo conjunto de disciplinas para que a comparação entre elas faça sentido. Não era o caso:

| Indicador | Antes |
|---|---|
| Aprovadas | Normal, Estágio, Tópicos Especiais, Pré-Eletiva e TCC |
| Matriculadas | Todas as categorias, inclusive Optativa, Isolada e Educação Física |
| Reprovadas e `IA65_03` | Só Normal, e de qualquer currículo |

**A descoberta: as atividades complementares.** Ao medir o efeito de alinhar as categorias, vimos que as atividades complementares obrigatórias têm turma e nota e contavam como disciplinas:

- **Aparecem em 73,9% das linhas** (32.822). São rotina, quase todo semestre de quase todo aluno.
- **Matriculadas:** 51.921 matrículas em turma, em média 1,169 por linha.
- **Reprovadas:** 6.878 reprovações, 12,09% das reprovações contadas antes. **2.664 alunos reprovaram em pelo menos uma**, 37,32% dos 7.138 alunos com registro acadêmico.
- **O comportamento é diferente do das disciplinas.** Nas atividades complementares, as aprovadas são 81,09% das matriculadas e as reprovadas, 13,26%. Nas disciplinas, são 66,76% e 20,19%.

Também testamos tirar a atividade complementar só das matriculadas. Isso criava 12.594 linhas com aprovadas maiores que matriculadas. Ela precisa sair dos indicadores todos juntos.

**Correção.**

- Aprovadas, matriculadas, reprovadas e `IA65_03` passam a usar **Normal, Estágio, Tópicos Especiais, Pré-Eletiva e TCC, sem atividade complementar**, e só disciplinas do currículo do aluno.
- As atividades complementares passam para **três indicadores próprios**: matriculadas, aprovadas e reprovadas no semestre. Com 37% dos alunos reprovando em ao menos uma, descartar a informação seria perder um dado que pode estar associado à saída.

**Efeito medido antes da reextração** (média por linha acadêmica):

| Indicador | Antes | Depois | Atividade complementar (novo) |
|---|---|---|---|
| Matriculadas | 6,779 | 5,608 | 1,169 |
| Aprovadas | 4,691 | 3,744 | 0,948 |
| Reprovadas | 1,281 | 1,132 | 0,155 |
| `IA65_03` | 0,362 | 0,347 | — |

- As categorias que passaram a contar nas reprovações (Estágio, Tópicos Especiais, Pré-Eletiva e TCC) somam só 250 reprovações. A queda vem quase toda da saída das atividades complementares.
- Pela regra nova, **nenhuma linha tem aprovadas maiores que matriculadas**.
- Antes do filtro de currículo, 138 linhas tinham reprovadas maiores que matriculadas. A causa era que as reprovadas contavam turmas de qualquer currículo, e as matriculadas, só do currículo do aluno. Na base v3, com o filtro de currículo, essas linhas são **0** (seção 9).

### 6.1 Vazio nas linhas que vêm só de ocorrência

**Por que mudamos.** As linhas que vêm só de ocorrência não têm matrícula efetivada no semestre. Nelas, frequência, reprovações, `IA65_03` e atividades complementares já vinham vazios, mas os `IA75_*` vinham com 0. Esse 0 podia ser lido como "o aluno não teve nenhuma disciplina", quando o certo é "não há registro acadêmico".

**Correção.** Os cinco `IA75_*` passam a vir vazios nessas linhas. Nas linhas acadêmicas nada muda: 0 continua querendo dizer que o aluno não teve nenhuma disciplina naquela contagem.

## 7. Limitações que continuam

- **Registro das eletivas.** A vaga de Eletiva e a Pré-Eletiva cursada nem sempre aparecem no histórico no mesmo semestre. Em 587 aluno-semestres há só a Pré-Eletiva, e em 221 há só a Eletiva. A contagem de eletivas concluídas pode ter pequenas diferenças. Eletivas e pré-eletivas somam 5.253 lançamentos no histórico, contra 333.133 de disciplinas da categoria Normal.
- **Significado da atividade complementar com nota.** A hipótese é que a reprovação ocorre quando o aluno não completa os créditos exigidos pela atividade no semestre. Precisa ser confirmada com a instituição antes de interpretar os indicadores novos.
- **Curso Aluno Especial (`GAE`).** É uma das 12 siglas da base (26 alunos), mas não é um curso de graduação regular. A decisão de mantê-lo ou tirá-lo da análise e do modelo vai junto com a definição da variável-alvo (#18).
- **Aprovação por NP3.** Notas de 50 a 59 indicam aprovação pela NP3, e daria para criar um indicador de "disciplinas aprovadas só na NP3". Ele contaria o mínimo, e não o total, porque quem passa pela NP3 com 60 ou mais não aparece nessa faixa. Fica como proposta, fora do escopo atual.

## 8. Base v3 e legenda v2

**Nome dos arquivos.** Na pasta compartilhada, cada versão da base passa a se chamar `Base_academica_` seguido da versão:

| Versão | Arquivo | Usada em |
|---|---|---|
| v1 | `dados_alunos.csv` (nome antigo) | Pré-defesa (`pre_defesa_analise_exploratoria_v2.ipynb`) |
| v2 | `Base_academica_v2.csv` | `relatorio_alteracoes_base_v2.md` (`pre_defesa_analise_exploratoria_v2_base_v2_novas_colunas.ipynb`) |
| v3 | `Base_academica_v3.csv` | Este relatório (`pre_defesa_analise_exploratoria_v2_base_v3_legenda_v2.ipynb`) |

Para usar no notebook, aponte a variável `TCC_CSV_PATH` para o arquivo da versão desejada.

**Identificação da base v3:**

| Item | Valor |
|---|---|
| Data da extração | 24/10/2026 |
| Arquivo | `Base_academica_v3.csv` (59.059 linhas) |
| SHA-256 do arquivo | `9CCE803735488354B820F9B1976612AB9D1DE5950EDB91BE57F85C415D6A2343` |
| Regras aplicadas | as do `relatorio_alteracoes_base_v2.md` (seções 2.1 a 2.4) e as deste relatório (seções 3 a 6.1) |

**A legenda foi reescrita (legenda v2)** e substitui a anterior. Ela descreve as 81 colunas da base v3. O que mudou:

- **Colunas novas:** datas das ocorrências, flags de rematrícula, falecimento, prazo esgotado e afastamento sem ocorrência, `ORIGEMREGISTRO`, `QTDOCORRENCIASSEMDATA` e os três `ATIVCOMPL_*`.
- **Organização da base:** uma seção nova explica que a base tem uma linha por aluno, semestre e currículo, o recorte, a diferença entre linhas acadêmicas e de ocorrência, e a diferença entre vazio e zero.
- **Descrições revistas** de acordo com as regras deste relatório: `IA75_01` a `IA75_05`, `IA34_03`, `IA65_03` e frequência (`IA04_*`).
- **Situações confirmadas com a instituição:**
  - situação do aluno no semestre e na turma (1 Ativo, 2 Inativo, 3 Desistente etc.);
  - situação da nota na turma (1 pendente, 3 aprovado, 4 reprovado);
  - bolsa classificada (`IA10_01`, percentual concedido) e desclassificada (`IA09`, bolsa não concedida, com o motivo em `IA09_02`).
- **Pendências antigas resolvidas:**
  - a grafia de `TEVETRANSAFASTAMENTO` (a legenda anterior escrevia `TEVETRASAFASTAMENTO`);
  - a definição de `ORIGEMREGISTRO` e `QUANTIDADEOCORRENCIAS`;
  - a sigla `GAE`, que é o Curso Aluno Especial.
- **Mantido da legenda anterior:** a tabela de cursos e as descrições de `APROVEIT` e `IA12_01` (percentual de financiamento pelo FIES).
- **Anonimização:** a legenda reforça que `MATRICULA`, `DATANASCIMENTO` e os códigos internos não devem aparecer em tabelas, gráficos ou texto.

A legenda continua fora do repositório, junto com a base.

## 9. Resultado na base v3

Comparamos célula a célula as saídas do notebook na base v2 (`Base_academica_v2.csv`, notebook `pre_defesa_analise_exploratoria_v2_base_v2_novas_colunas.ipynb`) e na base v3 (`pre_defesa_analise_exploratoria_v2_base_v3_legenda_v2.ipynb`). O código do notebook é o mesmo nas duas execuções, e o notebook roda inteiro sem erros.

**Conferências de coerência:**

| Conferência | Base v2 | Base v3 |
|---|---|---|
| Linhas acadêmicas com aprovadas maiores que matriculadas | 5.388 | **0** |
| Linhas acadêmicas com reprovadas maiores que matriculadas | 138 | **0** |
| Linhas de ocorrência com reprovadas maiores que matriculadas | 0 | 0 |

A terceira conferência da seção anterior (nenhuma linha com mais concluídas do que exigidas) foi feita no sistema acadêmico, antes da reextração, porque o notebook não calcula essa comparação. Pela regra nova, nenhuma linha tinha mais concluídas do que exigidas.

**O que mudou nas comparações entre casos e referências (V0)** (média dos casos / média padronizada das referências / diferença):

| Indicador | Base v2 | Base v3 |
|---|---|---|
| Aprovadas no semestre (`IA75_03`) | 2,296 / 4,927 / −2,631 | **0,933 / 3,115 / −2,183** |
| Reprovadas no semestre (`IA34_03`) | 3,282 / 1,593 / 1,689 | **2,809 / 1,405 / 1,404** |
| Matriculadas no semestre (`IA75_04`) | 5,858 / 5,937 / −0,079 | **4,845 / 4,919 / −0,074** |
| Disciplinas retiradas ou canceladas (`IA65_03`) | 0,426 / 0,374 / 0,051 | **0,407 / 0,360 / 0,047** |

- A **direção** das quatro comparações continua a mesma. No semestre anterior à saída, os casos têm menos aprovações e mais reprovações que as referências, e um número parecido de disciplinas matriculadas.
- **Os valores absolutos caíram**, como esperado, porque as atividades complementares e as disciplinas relançadas na migração saíram das contagens.
- **As aprovadas dos casos caíram mais** que as das referências: de 2,296 para 0,933, contra 4,927 para 3,115. A diferença diminuiu de −2,631 para −2,183. Uma parte do que antes aparecia como aprovação dos casos não era disciplina cursada no semestre.
- Essas diferenças são descritivas e não indicam causa.

**O que não mudou:** amostras, CRE, frequência, trancamento, indicadores financeiros, socioeconômicos, trajetória e sexo. Os números da base v2, já registrados no `relatorio_alteracoes_base_v2.md`, continuam valendo para eles. A amostra V0 continua com 1.468 casos e 16.697 referências.

**Validação numérica (célula 34):**

| Indicador | Nulos | Zeros explícitos na base v3 |
|---|---|---|
| `IA75_01` (exigidas pela grade) | 14.642 (antes 0) | 0 |
| `IA75_02` (concluídas acumuladas) | 14.642 (antes 0) | 2.411 |
| `IA75_03` (aprovadas no semestre) | 14.642 (antes 0) | 5.872 |
| `IA75_04` (matriculadas no semestre) | 14.642 (antes 0) | 329 |
| `IA75_05` (previstas no período) | 14.642 (antes 0) | 34 |
| `IA34_03` (reprovadas) | 14.642 | 23.377 (antes 22.227) |
| `IA65_03` | 14.642 | 35.656 (antes 35.509) |

Os 14.642 nulos são as linhas que vêm só de ocorrência (seção 6.1). Nenhuma linha acadêmica ficou com 0 disciplinas exigidas pela grade.

## 10. Alterações no notebook

O código do notebook não mudou nesta rodada. As saídas mudaram só nas células 34 (validação numérica), 40 (contagens de disciplinas) e 67 (tabela de ausências, que agora mostra os `IA75_*` e os `ATIVCOMPL_*` com os nulos das linhas de ocorrência).

Ajustes que ainda precisam ser feitos no notebook:

- A tabela de pendências de documentação (célula 67) ainda lista transferência/afastamento, `ORIGEMREGISTRO` e `GAE`, que a legenda v2 resolveu. Podem sair da tabela.
- Os três `ATIVCOMPL_*` ainda não são lidos nem analisados pelo notebook.

## 11. Próximos passos

1. Tirar da tabela de pendências do notebook os itens resolvidos pela legenda v2.
2. Decidir se as atividades complementares entram na análise e no modelo e, se entrarem, acrescentar a leitura e as comparações dos `ATIVCOMPL_*` no notebook.
3. Atualizar no artigo os números das comparações de disciplinas (seção 9).
4. Levar à #18, junto com a definição da variável-alvo: o Curso Aluno Especial (`GAE`) e a interpretação da reprovação em atividade complementar.
