## Definição da variável-alvo: evasão da instituição sem retorno

### 1. Objetivo

Definir uma regra reproduzível para identificação da evasão acadêmica, permitindo investigar fatores associados à interrupção definitiva da trajetória acadêmica dos estudantes do INATEL.

A análise tem como objetivo compreender características associadas à evasão, não realizar previsões individuais de desligamento.

### 2. Unidade de análise

Será utilizada uma observação por aluno e semestre cursado, considerando matrículas efetivadas.

Alunos com múltiplos currículos serão mantidos na análise, considerando a trajetória do estudante como uma única unidade. Os registros de diferentes currículos deverão ser consolidados em uma linha por aluno e semestre na construção do dataset.

### 3. Definição de evasão

Será considerada evasão institucional a situação em que o aluno apresenta um evento formal de saída (desistência, abandono, cancelamento ou desligamento) e não retorna a cursar nenhum curso do INATEL durante os dois semestres subsequentes ao último semestre efetivamente cursado.

A janela principal será de dois semestres (N = 2), aproximadamente um ano.

A escolha busca equilibrar a identificação de saídas definitivas e a possibilidade de retorno posterior, evitando classificar interrupções temporárias como evasão.

### 4. Critério de retorno

Será considerado retorno a existência de matrícula efetivada em qualquer curso do INATEL.

Ocorrências administrativas de rematrícula e reingresso, isoladamente, não serão consideradas retorno sem matrícula efetivada.

A mudança de curso dentro da instituição não caracteriza evasão institucional.

O indicador de transferência/afastamento não será utilizado isoladamente como evento de evasão, devido à impossibilidade de distinguir com segurança situações de transferência definitiva e afastamento temporário.

### 5. Tratamento dos episódios de saída

Será considerado o primeiro episódio de saída que satisfaça a regra de ausência de retorno durante os dois semestres subsequentes ao último semestre cursado.

Episódios seguidos de retorno dentro da janela não serão classificados como evasão definitiva.

Caso exista um novo episódio posterior, a regra será reaplicada considerando a nova trajetória acadêmica.

### 6. Início da evasão

O início da evasão será associado ao último semestre efetivamente cursado pelo estudante, e não necessariamente ao semestre de lançamento do evento administrativo.

Essa escolha busca representar o momento em que a trajetória acadêmica foi interrompida, reduzindo o efeito de atrasos nos registros administrativos.

O semestre do próprio evento formal de saída não será utilizado como observação positiva quando apresentar informações que possam refletir o desligamento.

### 7. Classificação das observações

**Positiva (1):** último semestre cursado antes de um evento formal de saída, sem retorno em qualquer curso do INATEL durante os dois semestres subsequentes.

**Negativa (0):** semestre cursado seguido de continuidade acadêmica ou o último semestre de um estudante que concluiu o curso.

**Excluída:** observações sem desfecho suficientemente conhecido, incluindo:
- Semestre do evento formal de saída, quando houver risco de vazamento de informação.
- Saídas recentes sem dois semestres completos de observação.
- Estudantes ainda sem desfecho observável.
- Estudantes que interromperam os estudos sem evento formal de saída.
- Estudantes falecidos.
- Casos classificados como GAE, até que seu tratamento seja validado. Prazo de integralização esgotado não é saída nem motivo de exclusão.

### 8. Casos especiais

- **Trancamento:** não será considerado evasão isoladamente. O estudante poderá ser classificado como evadido caso apresente evento formal de saída e cumpra o critério de ausência de retorno.
- **Mudança de curso:** não caracteriza evasão institucional.
- **Transferência/afastamento:** não será suficiente para caracterizar evasão sem confirmação de saída institucional definitiva.
- **Falecimento:** estudantes falecidos serão excluídos.
- **Prazo de integralização esgotado:** não é uma saída do Inatel e não será usado como evento nem como exclusão. O estudante segue a regra comum; só um evento formal de saída sem retorno dentro da janela caracteriza evasão.
- **Saída sem evento formal:** será mantida como excluída na análise principal, evitando atribuir evasão sem evidência administrativa.
- **Múltiplos currículos:** serão consolidados por aluno e semestre.

### 9. Janela de observação e retorno

A janela principal proposta é N = 2 semestres, aproximadamente um ano, com N = 3 como sensibilidade. A regra de início na data formal da saída também é comparada em N = 2.

Para alinhar a escolha de N à regra final, a curva foi recalculada desde o último semestre acadêmico até a primeira saída formal. Foram considerados alunos com saída formal, excluídos falecidos e GAE, retorno por matrícula acadêmica em qualquer curso e apenas alunos com pelo menos k semestres observáveis após o último semestre cursado. Assim, os denominadores variam com k para não tratar saídas recentes como não-retornos.

| k | Alunos observáveis | Voltaram até k (%) | Voltaram exatamente em k (%) |
|---:|---:|---:|---:|
| 1 | 2.925 | 3,83 | 3,83 |
| 2 | 2.883 | 6,63 | 2,74 |
| 3 | 2.789 | 8,28 | 1,69 |
| 4 | 2.723 | 9,81 | 1,43 |
| 5 | 2.613 | 10,83 | 0,96 |
| 6 | 2.560 | 10,82 | 0,16 |
| 7 | 2.466 | 11,07 | 0,24 |
| 8 | 2.417 | 11,67 | 0,41 |
| 9 | 2.317 | 11,83 | 0,09 |
| 10 | 2.257 | 12,05 | 0,18 |

A curva alinhada ao último semestre cursado continua subindo depois de N = 2: 6,63% retornaram até k = 2, 8,28% até k = 3 e 10,83% até k = 5 entre os observáveis. Isso difere da curva antiga do guia, que contava o prazo desde a saída formal. Mantemos N = 2 como decisão provisória do grupo e N = 3 como sensibilidade, mas a orientadora/revisor deve confirmar se o aumento de retornos até k = 5 justifica ampliar a janela. A tabela de resultados da seção 10 mostra o efeito de N = 1, 2 e 3.

### 10. Resultados quantitativos e decisões aplicadas

**Fonte:** `Base_academica_v4.csv`, 59.059 linhas, 81 colunas, SHA-256 `A37D9F2F12CB0A19DF1011BE6BA61D64E644A4C01717714DCD0B62C782DE3646`; último semestre observado: 2026/1. O CSV contém 44.417 linhas acadêmicas e 14.642 de ocorrência. Para a rotulagem, foram consideradas 44.370 unidades únicas aluno-semestre acadêmico; 47 repetições de aluno-semestre em currículos diferentes foram consolidadas. `MATRICULA` e `DATANASCIMENTO` não foram carregados pelo script nem reproduzidos.

**Exclusão especial provisória:** são excluídas as trajetórias completas de estudantes com registro de falecimento e, provisoriamente, de GAE até validação do recorte. Na base, há 14 estudantes falecidos (100 aluno-semestres) e 26 com GAE (24 aluno-semestres); os grupos não se sobrepõem. Três dos 40 estudantes sinalizados não têm semestre acadêmico na base. O prazo esgotado **não é excluído**. Restam 7.101 estudantes com pelo menos um semestre acadêmico após as exclusões provisórias por falecimento e GAE. A exclusão provisória de GAE ainda depende de confirmação do grupo/orientadora.

Os 26 estudantes com `TEVEPRAZOESGOTADO` permanecem na análise. O flag descreve o limite de 20 semestres e a necessidade de novo vestibular; não indica desligamento. A conferência encontrou 24 com matrícula efetivada em algum dos dois semestres posteriores ao flag; 13 com `DATADIPLOMACAO` posterior à data de `DATAPRAZOESGOTADO` (um desses pares de eventos cai no mesmo semestre, mas a data da diplomação é posterior); e 8 com evento formal de saída no mesmo semestre ou depois. Esses grupos se sobrepõem: os 8 com saída formal também estão entre os 24 que retornaram, e 12 dos 13 diplomados também retornaram. Portanto, os totais não são aditivos. O prazo em si não muda a classificação; cada estudante segue os critérios normais de retorno e evento formal.

A janela é contada do último semestre com matrícula efetivada: não há retorno se não existir outro semestre acadêmico nos N semestres seguintes. O primeiro episódio formal que satisfaz a regra determina o corte da trajetória. O último semestre acadêmico antes do semestre da saída é a observação positiva; se a própria saída ocorre em um semestre acadêmico, essa linha é excluída para evitar vazamento. Distâncias entre a observação positiva e a saída formal são mantidas sem corte máximo, pois o início da interrupção é ancorado no último semestre cursado, não na data administrativa. A distribuição é mostrada abaixo para tornar visíveis os registros muito tardios.

| N | Linhas positivas | Linhas negativas | Proporção positiva | Linhas excluídas | Estudantes com linha positiva | Evadidos sem semestre anterior utilizável |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1.889 | 38.206 | 4,71% | 4.275 | 1.889 | 983 |
| **2 (principal)** | **1.840** | **38.664** | **4,54%** | **3.866** | **1.840** | **947** |
| 3 (sensibilidade) | 1.773 | 38.919 | 4,36% | 3.678 | 1.773 | 894 |

Para N = 2, há 2.787 estudantes com episódio que satisfaz a regra; 947 (33,98%) não têm semestre anterior utilizável como linha positiva. Eles não entram como positivos no dataset, embora contem como evadidos confirmados na descrição da população. Entre as 40.504 linhas classificadas (positivas + negativas), 4,54% são positivas.

Manter os estudantes com prazo esgotado, em comparação com excluí-los, acrescenta 8 linhas positivas e 445 negativas, reduz as exclusões em 453 e altera a proporção positiva em −0,03 ponto percentual. A escolha tem efeito pequeno nos totais e segue a interpretação de que o prazo exige novo vestibular, mas não é desligamento.

**Sensibilidade ao início da janela (N = 2, mesmas exclusões por falecimento e GAE):** se a janela for contada do semestre do evento formal, em vez do último semestre cursado, o resultado é 1.753 positivas, 38.941 negativas, 4,31% positivos e 3.676 excluídas. A regra principal produz 87 positivas a mais, 277 negativas a menos e 190 exclusões a mais. Mantemos o último semestre cursado como origem porque representa quando o estudante parou, enquanto o registro formal pode ser tardio.

**Exclusões para N = 2:**

| Motivo | Aluno-semestres |
|---|---:|
| Falecimento (trajetória completa excluída) | 100 |
| GAE (trajetória completa excluída; provisório) | 24 |
| Semestre da saída formal | 1.364 |
| Saída sem dois semestres completos de observação | 48 |
| Ainda sem desfecho observável | 1.351 |
| Parou sem evento formal de saída | 300 |
| Semestres após o primeiro episódio que satisfaz a regra | 679 |
| **Total de linhas excluídas** | **3.866** |

**Distância entre a linha positiva e a saída formal, N = 2:** 1 semestre: 1.420; 2 semestres: 340; 3 semestres: 50; 4 ou mais: 30 (máximo observado: 21 semestres). A regra principal mantém todas as distâncias; limitar a 2 semestres retiraria 80 das 1.840 linhas positivas (4,35%) e exigiria recalcular as contagens completas.

O script reproduzível é `scripts/analysis/rotular_variavel_alvo.py`. Ele lê o caminho configurado em `TCC_CSV_PATH`, não carrega `MATRICULA` nem `DATANASCIMENTO` e imprime somente contagens agregadas. Como conferência da fonte, reproduzimos também o código antigo do guia com a janela iniciada na saída formal: N = 2 retornou exatamente os valores de referência (1.751 positivas, 38.832 negativas e 4,31%). Esses valores antigos não são os resultados finais da definição corrigida.

A proporção provisória de positivos (N = 2) foi registrada também em `docs/decisoes_metricas_modelagem.md`. Atualizar as issues #29 e #54 com o mesmo número quando o grupo aprovar a exclusão provisória de GAE.

### 11. Justificativa metodológica

A definição prioriza a evasão institucional, distinguindo interrupções temporárias, mudanças de curso e saídas definitivas.

A utilização de uma janela de dois semestres busca reduzir falsos positivos decorrentes de retornos tardios, enquanto a exclusão de casos sem observação suficiente evita atribuições incorretas de classe.

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










