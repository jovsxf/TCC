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
- A estrutura da base continua a mesma: 59.059 registros, 7.615 alunos, 3.507 alunos com saída e 3.841 linhas positivas. Alguns números da pré-defesa mudaram por causa da correção da diplomação e precisam ser atualizados no artigo (seção 4).
- O notebook ganhou três células de análise (59, 60 e 61) e um ajuste na tabela de ausências (célula 67). Ele roda inteiro sem erros.

---

## 2. O que mudou na base e por quê

### 2.1 Datas das ocorrências

**O que entrou:** para cada tipo de ocorrência, a data em que ela foi registrada (`DATADESISTENCIA`, `DATAABANDONO`, `DATATRANCAMENTO`, `DATAREINGRESSO` etc.). Também entraram três colunas sobre a saída:

- `DATAPRIMEIRASAIDA` e `DATAULTIMASAIDA`: a primeira e a última data de saída no semestre;
- `DATAINCLUSAOSAIDA`: quando a saída foi lançada no sistema.

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

### 3.3 A data da ocorrência é a data de registro

**Por que olhamos:** para saber se a data serve para ordenar os eventos e para dizer quando o aluno saiu.

**Resultados:**

- 93,76% das datas não têm hora, então só dá para ordenar eventos por dia;
- 26,8% das saídas foram lançadas no sistema mais de 180 dias depois da data registrada;
- a data da ocorrência cai fora da metade do ano correspondente ao semestre a que ela está ligada em 22,38% das ocorrências de 1º semestre e em 19,61% das de 2º semestre, quase sempre na virada entre semestres.

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

| Indicador | Base antiga (v2) | Base nova |
|---|---|---|
| Registros / estudantes / semestres / cursos | 59.059 / 7.615 / 35 / 12 | igual |
| Alunos com saída / linhas positivas / pares / mais de um semestre | 3.507 / 3.841 / 3.728 / 202 | igual |
| Reingresso formal após 1ª saída | 138 | 138 |
| Matrícula efetivada após 1ª saída | 398 | 398 |
| **Conclusão após 1ª saída** | 156 | **142** |
| **CRE em t−1, casos (n)** | 23,65 (1.266) | **23,669 (1.270)** |
| **CRE em t−1, referências (aluno/semestre)** | 51,83 (15.042) | **51,727 (15.254)** |
| **Diferença do CRE em t−1** | −28,18 | **−28,058** |
| **Trajetória do CRE (alunos)** | 464 | **466** |
| **Trajetória t−3 / t−2 / t−1** | 33,25 / 29,32 / 21,70 | **33,303 / 29,350 / 21,777** |
| **Sexo com saída F / M** | 41,60% / 47,33% | **41,548% / 47,335%** |
| **Sexo χ² / p** | 17,098 / 3,55e-05 | **17,413 / 3,01e-05** |
| Status final sem saída: Inativo / indefinidos / conflitos | 267 / 946 / 15 | igual |

- **Conclusões, CRE e trajetória** mudaram por causa da correção da diplomação, que mexe em quem entra como caso e como referência. Com 240 diplomações a menos nas linhas de ocorrência, entram 4 casos e 212 referências a mais. A conclusão sobre o CRE continua a mesma.
- **Sexo** não depende dessa correção: só o grupo feminino mudou (698 de 1.680, com 7 alunos sem informação). Hipótese ainda não verificada: o cadastro foi atualizado entre as duas extrações. Para conferir, basta ver se a base antiga tinha 9 alunos sem informação de sexo.
- Alunos com transferência/afastamento na base nova: 323.

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
