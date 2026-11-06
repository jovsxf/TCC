## Definição da variável-alvo: evasão da instituição sem retorno

### 1. Objetivo

Definir uma regra reproduzível para identificação da evasão acadêmica, permitindo investigar fatores associados à interrupção definitiva da trajetória acadêmica dos estudantes do INATEL.

A análise tem como objetivo compreender características associadas à evasão, não realizar previsões individuais de desligamento.

### 2. Unidade de análise

Será utilizada uma observação por aluno e semestre cursado, considerando matrículas efetivadas.

Alunos com múltiplos currículos serão mantidos na análise, considerando a trajetória do estudante como uma única unidade. Os registros de diferentes currículos deverão ser consolidados em uma linha por aluno e semestre na construção do dataset.

### 3. Definição de evasão

Será considerada evasão institucional a situação em que o aluno apresenta um evento formal de saída (desistência, abandono, cancelamento, desligamento ou transferência para outra instituição) e não retorna a cursar nenhum curso do INATEL durante a janela de observação definida pelo grupo.

**Regra vigente nesta revisão:** N = 4 semestres sem matrícula acadêmica após o semestre do evento formal de saída. N = 2 semestres, com a mesma origem, será apresentado como sensibilidade.

A escolha busca equilibrar a identificação de saídas definitivas e a possibilidade de retorno posterior, evitando classificar interrupções temporárias como evasão.

### 4. Critério de retorno

Será considerado retorno a existência de matrícula efetivada em qualquer curso do INATEL, desconsiderando semestres marcados como trancamento.

Ocorrências administrativas de rematrícula e reingresso, isoladamente, não serão consideradas retorno sem matrícula efetivada.

A mudança de curso dentro da instituição não caracteriza evasão institucional.

O CRA esclareceu que `TEVETRANSAFASTAMENTO` corresponde a um requerimento do aluno para transferência a outra instituição. Portanto, é um evento formal de saída institucional, não uma pausa. Como nos demais eventos, só será evasão definitiva se não houver retorno ao INATEL dentro da janela aprovada.

### 5. Tratamento dos episódios de saída

Será considerado o primeiro episódio de saída que satisfaça a regra de ausência de retorno durante os N semestres subsequentes ao evento.

Episódios seguidos de retorno dentro da janela não serão classificados como evasão definitiva.

Caso exista um novo episódio posterior, a regra será reaplicada considerando a nova trajetória acadêmica.

### 6. Início da evasão

O início da janela de retorno será associado ao semestre do evento formal de saída, e não ao último semestre efetivamente cursado.

O último semestre acadêmico anterior à saída será a observação candidata a positiva, desde que o aluno não retorne durante os N semestres seguintes ao evento.

O semestre do próprio evento formal de saída não será utilizado como observação positiva quando apresentar informações que possam refletir o desligamento.

### 7. Classificação das observações

**Positiva (1):** último semestre cursado antes de um evento formal de saída, sem retorno em qualquer curso do INATEL durante os N semestres subsequentes ao semestre do evento (N = 4 na regra principal).

**Negativa (0):** semestre cursado seguido de continuidade acadêmica ou o último semestre de um estudante que concluiu o curso.

**Excluída:** observações sem desfecho suficientemente conhecido, incluindo:
- Semestre do evento formal de saída, quando houver risco de vazamento de informação.
- Semestres marcados com `TEVETRANCAMENTO`, que não serão tratados como semestres cursados.
- Saídas recentes sem N semestres completos de observação.
- Estudantes ainda sem desfecho observável.
- Estudantes que interromperam os estudos sem evento formal de saída.
- Estudantes falecidos.
- Casos classificados como GAE, até que seu tratamento seja validado. Prazo de integralização esgotado não é saída nem motivo de exclusão.

### 8. Casos especiais

- **Trancamento:** é solicitado semestralmente. O semestre trancado foi removido das observações. Se o trancamento não for renovado, o CRA registra desistência por abandono. Ainda está pendente decidir se o próprio trancamento, sem abandono registrado, abre uma janela de observação; o trancamento, por si só, não será contado como evasão.
- **Mudança de curso:** não caracteriza evasão institucional.
- **Transferência-afastamento:** segundo esclarecimento do CRA, é a transferência requerida pelo aluno para outra instituição e será tratada como evento formal de saída. A regra de ausência de retorno ao INATEL continua aplicável.
- **Falecimento:** estudantes falecidos serão excluídos.
- **Prazo de integralização esgotado:** não é uma saída do Inatel e não será usado como evento nem como exclusão. O estudante segue a regra comum; só um evento formal de saída sem retorno dentro da janela caracteriza evasão.
- **Saída sem evento formal:** será mantida como excluída na análise principal, evitando atribuir evasão sem evidência administrativa.
- **Múltiplos currículos:** serão consolidados por aluno e semestre.

### 9. Janela de observação e retorno

**Decisão registrada após a revisão da PR #68:** usar N = 4 semestres e contar a janela a partir do semestre do evento formal de saída. N = 2, contado da mesma origem, será análise de sensibilidade. A janela de quatro semestres corresponde ao prazo informado de dois anos para retorno após trancamento.

**Ainda pendente:** decidir se o próprio trancamento, sem abandono registrado, abre a janela de retorno como pausa. Os semestres trancados já foram removidos das observações e do cálculo de retorno. Por enquanto, a janela é aberta por evento formal de saída; se o trancamento não for renovado, o CRA informou que lança desistência por abandono. A transferência para outra instituição foi incluída como evento formal de saída, conforme esclarecimento do CRA.

Para avaliar o retorno com a origem agora definida, a curva foi recalculada desde o semestre da primeira saída formal. Foram considerados alunos com saída formal, excluídos falecidos e GAE, retorno por matrícula acadêmica em qualquer curso e apenas alunos com pelo menos k semestres observáveis após a saída. Assim, os denominadores variam com k para não tratar saídas recentes como não-retornos.

| k | Alunos observáveis | Voltaram até k (%) | Voltaram exatamente em k (%) |
|---:|---:|---:|---:|
| 1 | 3.155 | 5,39 | 5,39 |
| 2 | 3.101 | 8,06 | 2,58 |
| 3 | 2.984 | 9,08 | 1,01 |
| 4 | 2.917 | 9,80 | 0,72 |
| 5 | 2.819 | 10,18 | 0,39 |
| 6 | 2.741 | 10,25 | 0,18 |
| 7 | 2.653 | 10,52 | 0,19 |
| 8 | 2.578 | 10,90 | 0,27 |
| 9 | 2.474 | 11,20 | 0,16 |
| 10 | 2.419 | 11,20 | 0,08 |

A curva de retorno desde o evento mostra que 8,06% dos observáveis retornaram até k = 2 e 9,80% até k = 4. A decisão registrada é N = 4; o número de retornos continua aumentando depois desse ponto, então a janela permanece sujeita à revisão do grupo/orientadora.

### 10. Resultados quantitativos e decisões aplicadas

**Fonte:** `Base_academica_v4.csv`, 59.059 linhas, 81 colunas, SHA-256 `A37D9F2F12CB0A19DF1011BE6BA61D64E644A4C01717714DCD0B62C782DE3646`; último semestre observado: 2026/1. O CSV contém 44.417 linhas acadêmicas e 14.642 de ocorrência. Antes de remover trancamentos, havia 44.370 unidades únicas aluno-semestre acadêmico; 47 pares aluno-semestre repetiam por currículo. Foram removidas 436 unidades com flag de trancamento; uma pertence a trajetória já excluída por falecimento/GAE, restando 43.934 unidades acadêmicas após o filtro. `MATRICULA` e `DATANASCIMENTO` não foram carregados pelo script nem reproduzidos.

**Exclusão especial provisória:** são excluídas as trajetórias completas de estudantes com registro de falecimento e, provisoriamente, de GAE até validação do recorte. Na base, há 14 estudantes falecidos (100 aluno-semestres) e 26 com GAE (24 aluno-semestres); os grupos não se sobrepõem. Três dos 40 estudantes sinalizados não têm linha acadêmica na extração. Depois de remover os semestres trancados, restam 7.088 estudantes com algum semestre cursado; o prazo esgotado **não é excluído**. A exclusão provisória de GAE ainda depende de confirmação do grupo/orientadora.

Os 26 estudantes com `TEVEPRAZOESGOTADO` permanecem na análise. O flag descreve o limite de 20 semestres e a necessidade de novo vestibular; não indica desligamento. Desconsiderando os semestres trancados, a conferência encontrou 23 com matrícula efetivada em algum dos dois semestres posteriores ao flag; 13 com `DATADIPLOMACAO` posterior à data de `DATAPRAZOESGOTADO` (um desses pares de eventos cai no mesmo semestre, mas a data da diplomação é posterior); e 9 com evento formal de saída no mesmo semestre ou depois, agora incluindo transferência para outra instituição. Esses grupos se sobrepõem: 7 das 9 saídas formais também estão entre os 23 que retornaram, e 12 dos 13 diplomados também retornaram. Portanto, os totais não são aditivos. O prazo em si não muda a classificação; cada estudante segue os critérios normais de retorno e evento formal.

Não há retorno se não existir outro semestre acadêmico nos N semestres após o semestre do evento formal. O primeiro episódio formal que satisfaz a regra determina o corte da trajetória. A observação positiva é o último semestre acadêmico antes da saída; o semestre da própria saída é excluído para evitar vazamento. Distâncias entre a observação positiva e a saída formal são mantidas sem corte máximo e descritas abaixo.

| N | Linhas positivas | Linhas negativas | Proporção positiva | Linhas excluídas | Estudantes com linha positiva | Evadidos sem semestre anterior utilizável |
|---:|---:|---:|---:|---:|---:|---:|
| **4 (principal)** | **1.878** | **38.520** | **4,65%** | **3.972** | **1.878** | **895** |
| 2 (sensibilidade) | 2.014 | 38.304 | 5,00% | 4.052 | 2.014 | 966 |

Para N = 4, há 2.773 estudantes com episódio que satisfaz a regra; 895 (32,28%) não têm semestre anterior utilizável como linha positiva. Eles não entram como positivos no dataset, embora contem como evadidos confirmados na descrição da população. Entre as 40.398 linhas classificadas (positivas + negativas), 4,65% são positivas.

Os totais anteriores a estas decisões (N = 2 desde o último semestre cursado, sem transferência-afastamento como saída e contando os semestres trancados) eram 1.840 positivas e 38.664 negativas. Ficam registrados apenas como referência histórica e não devem ser comparados diretamente com os resultados atuais.

**Sensibilidade à duração da janela (N = 2 desde o evento):** 2.014 positivas, 38.304 negativas, 5,00% positivos e 4.052 excluídas. **Sensibilidade à origem (N = 4 desde o último semestre cursado):** 1.975 positivas, 38.388 negativas, 4,89% positivos e 4.007 excluídas.

O semestre da saída também é excluído quando há retorno: a apuração identificou 173 dessas linhas para N = 4 e 148 para N = 2. A estimativa de 150 linhas da revisão é próxima ao resultado N = 2; as diferenças decorrem de contar semestres trancados fora do retorno e de incluir transferência-afastamento como evento formal. Com essa exclusão adicional, o N = 4 cai de 1.887 para 1.878 positivas: em 9 casos, a observação que era candidata a positiva também coincidia com um semestre de saída anterior.

**Exclusões para N = 4:**

| Motivo | Aluno-semestres |
|---|---:|
| Falecimento (trajetória completa excluída) | 100 |
| GAE (trajetória completa excluída; provisório) | 24 |
| Semestre da saída formal | 1.603 |
| Saída sem quatro semestres completos de observação | 236 |
| Ainda sem desfecho observável | 1.367 |
| Parou sem evento formal de saída | 7 |
| Semestres após o primeiro episódio que satisfaz a regra | 200 |
| Semestre trancado removido da unidade cursada | 435 |
| **Total de linhas excluídas** | **3.803** |

**Distância entre a linha positiva e a saída formal, N = 4:** 1 semestre: 1.373; 2 semestres: 390; 3 semestres: 76; 4 ou mais: 39 (máximo observado: 21 semestres).

O script reproduzível é `scripts/analysis/rotular_variavel_alvo.py`. Ele lê o caminho configurado em `TCC_CSV_PATH`, não carrega `MATRICULA` nem `DATANASCIMENTO` e imprime somente contagens agregadas. Como conferência da fonte, reproduz também a regra antiga do guia (sem tratar transferência-afastamento como saída): N = 2 retornou os valores de referência de 1.751 positivas, 38.832 negativas e 4,31%. Esses valores são apenas uma conferência histórica, não os resultados da regra atualizada.

Após a revisão da definição e aprovação do grupo, atualizar as issues relacionadas à modelagem com a proporção recalculada.

### 11. Justificativa metodológica

A definição prioriza a evasão institucional, distinguindo interrupções temporárias, mudanças de curso e saídas definitivas.

A utilização de uma janela de quatro semestres, contada desde a saída formal, considera o prazo de dois anos informado para retorno após trancamento. Casos sem observação suficiente ficam excluídos para evitar atribuições incorretas de classe. A sensibilidade N = 2 é reportada para mostrar como a duração afeta os rótulos.

A unidade aluno/semestre permite investigar características acadêmicas ao longo da trajetória estudantil, mantendo o foco na compreensão dos fatores associados à evasão.

### 12. Impactos nas próximas etapas

A definição deverá orientar:
- Construção e rotulagem do dataset final (#20).
- Atualização da proporção de positivos no documento de métricas (#29).
- Atualização da análise de desbalanceamento (#54).
- Definição das métricas de avaliação e metodologia do artigo.

### 13. Validação

Definição provisória adotada pelo grupo, pendente de validação da orientação acadêmica.

A regra poderá ser atualizada caso a orientação indique ajustes metodológicos.










