# Decisões da reunião do TCC

Nov 4, 2026 · @karol

A variável-alvo passa a ser a **evasão da instituição sem retorno**, e os modelos serão escolhidos por uma métrica que não depende do limiar, com o limiar definido por regra só no treino. GAE e prazo de integralização esgotado ficaram para verificar.

| Tema | Decisão | Consequência | Issue |
| --- | --- | --- | --- |
| Variável-alvo | Evasão da instituição sem retorno | Trocar de curso dentro do Inatel não é evasão. As 78 trocas de vínculo deixam de ser positivas, salvo se o aluno sair de tudo depois | #18 |
| O que conta como retorno | Matrícula efetivada em qualquer curso do Inatel dentro da janela | As ocorrências de rematrícula e reingresso não são usadas como prova de retorno | #18 |
| Alunos com mais de um currículo | Mantidos | O aluno pode cursar mais de um curso. Só evade quando deixa todos | #18, #20 |
| Falecimento | Excluído | 15 linhas com a marcação saem da população | #18, #20 |
| Rematrícula e reingresso | Alunos mantidos | As ocorrências não definem retorno | #18 |
| Métrica de seleção | Métrica sem limiar: PR-AUC como principal, ROC-AUC como complementar (seção Métricas e limiar) | O documento de métricas da PR #65 precisa ser ajustado | #29, #30 |
| Limiar | Regra igual para todos os modelos, só no treino; 0,5 como sensibilidade | Idem | #29 |
| GAE | A verificar | — | #15, #18 |
| Prazo de integralização esgotado | A verificar | — | #18 |

## Variável-alvo: evasão da instituição sem retorno

**A regra.** Um aluno evadiu quando:

1. tem um evento de saída (desistência, abandono, cancelamento ou desligamento);
2. depois desse evento, não tem matrícula efetivada em **nenhum** curso do Inatel dentro de uma janela de N semestres.

Se ele voltar a ter matrícula efetivada em qualquer curso dentro da janela, aquele evento não é evasão.

**Por que da instituição.**

- As 78 saídas em que o aluno continuou em outro vínculo são trocas internas: 83,33% seguiram matriculados no semestre seguinte e 48,72% se diplomaram depois.
- A marcação de mudança de curso não aparece em nenhum desses casos, então uma regra "por curso" contaria essas trocas como evasão.
- A evasão por curso pode ficar como análise de sensibilidade.

**Por que sem retorno.** Muitos alunos voltam depois de um evento de saída. Depois da primeira saída, a base tem 138 reingressos formais, 398 matrículas efetivadas e 156 conclusões. Sem a janela, esses alunos seriam contados como evadidos.

**Ainda abertos dentro da regra** (proposta, para confirmar):

| Detalhe | Proposta | Por quê |
| --- | --- | --- |
| Tamanho da janela (N) | Escolher pela curva de retorno: quantos alunos voltam após 1, 2, 3 ou mais semestres | O ponto em que quase ninguém volta mais evita chutar um número. Dois semestres é um ponto de partida comum |
| Quando a evasão começa | No primeiro semestre em que o aluno deixa de cursar e não volta, mesmo que seja um trancamento | Das 212 linhas "Inativo" no semestre anterior à saída, 205 são semestres trancados. Datar pela saída formal faria o semestre trancado entrar no modelo como se fosse um semestre cursado |
| Unidade de análise | Uma linha por aluno e semestre cursado. A pergunta é se o aluno evade a partir do semestre seguinte | Segue a trajetória (Tinto) e repete o desenho da análise exploratória, que compara o semestre anterior à saída com referências do mesmo semestre, curso e período |
| Episódios | Só a primeira evasão de cada aluno. Quem volta dentro da janela segue no conjunto | Cobre os 202 alunos com mais de um semestre de saída sem complicar a validação |
| Semestres sem janela observável | Ficam fora | Os últimos N semestres da base não têm desfecho conhecido |

A #18 pede que o efeito da regra seja medido: quantos positivos, negativos e excluídos. Isso ainda não foi calculado.

## População

**Alunos com mais de um currículo: mantidos.** O aluno pode cursar mais de um curso, e isso não é erro da base: a chave aluno + semestre + currículo não tem nenhuma duplicidade. Duas consequências:

- **A evasão é do aluno, não do currículo.** Ele só evade quando deixa todos os vínculos sem voltar.
- **Se a unidade for aluno e semestre, os currículos do mesmo semestre viram uma linha só.** Falta definir como juntar os indicadores (somar disciplinas, combinar CRE e frequência). Isso fica para a #20.

**Falecimento: excluído.** São 15 linhas com a marcação. Falecimento não é evasão nem permanência, então o aluno sai da população.

**Rematrícula e reingresso: os alunos ficam, mas as ocorrências não provam retorno.** O raciocínio está certo:

- **A ocorrência não é necessária.** O aluno pode voltar a estudar sem que a ocorrência seja lançada. O que mostra que ele voltou é ter matrícula efetivada num semestre depois da saída.
- **A ocorrência também não é suficiente.** Um reingresso lançado não garante que o aluno cursou. Em 17 semestres, o aluno reingressa e sai de novo no mesmo semestre.
- **Excluir esses alunos seria um erro.** Eles são justamente os que saem e voltam, então tirá-los distorceria a evasão.

Definição de retorno: **existe linha acadêmica (matrícula efetivada) do aluno, em qualquer currículo, num semestre dentro da janela depois da saída.** Na base, toda linha acadêmica tem matrícula efetivada, porque a extração só traz esses semestres. Se as ocorrências de rematrícula e reingresso virão variáveis do modelo, a decisão é da #26.

**Consequências da regra que não foram discutidas, para confirmar:**

- **Os 682 ingressos não efetivados (19,45% dos alunos com saída):** com a unidade aluno e semestre cursado, os 475 que nunca cursaram nada ficam fora naturalmente. Os outros 207 só contam se saírem de todos os vínculos. Vale reportar os 682 à parte no artigo.
- **Quem trancou e não voltou:** pela regra, é evasão. O ponto aberto é só em que semestre ela começa (seção anterior).

## Métricas e limiar (#29)

**Decisão:**

- a **PR-AUC** escolhe os hiperparâmetros e compara os quatro modelos;
- a **ROC-AUC** é reportada como complemento;
- o limiar é o que **maximiza o F2** nas previsões do treino, e o 0,5 vira análise de sensibilidade;
- o **Recall** é a métrica de destaque na leitura dos resultados, sempre ao lado da Precision.

### Por que PR-AUC com esta variável-alvo

**A evasão da instituição sem retorno tem menos positivos do que os eventos de saída que usávamos.** Hoje, os eventos de saída são 46,05% por aluno (3.507 de 7.615) e 7,73% por aluno e semestre (3.728 de 48.200). A regra nova tira desses números:

- os alunos que voltam;
- as trocas de vínculo;
- os ingressos que nunca cursaram.

Então as duas porcentagens são tetos, e a proporção real será menor. Com uma linha por aluno e semestre, os positivos devem ficar abaixo de 8%.

**Com positivos raros, a ROC-AUC fica otimista.** Ela mede os alarmes falsos como proporção de quem ficou. Como quem fica é a enorme maioria, muitos alarmes falsos viram uma porcentagem pequena e quase não pesam.

**A PR-AUC olha o que importa quando o grupo de interesse é pequeno:** dos alunos que o modelo coloca no topo do risco, quantos realmente evadiram (Precision), e quantos dos que evadiram ele encontrou (Recall). Ela faz isso ao longo de todos os limiares, então também não depende do corte.

**Por que não o Recall.** Num teste com dados simulados, a busca que otimizava só o Recall marcou todo mundo como saída: Recall 1,000, com a Precision igual à proporção de positivos. A PR-AUC não tem esse problema, porque um modelo que marca todo mundo tem PR-AUC igual à proporção de positivos, o mesmo valor de um modelo que só chuta.

**Mesmo que a unidade final seja um registro por aluno, com mais positivos, a PR-AUC continua válida.** Ela só fica parecida com a ROC-AUC. Por isso, a decisão não depende da unidade.

### Como calcular

| Item | Regra |
| --- | --- |
| PR-AUC | Precisão média (*average precision*), calculada sobre as probabilidades da classe positiva. No scikit-learn: `average_precision_score` ou `scoring="average_precision"`. Não usar a área por trapézios da curva Precision–Recall, que é otimista |
| Referência da PR-AUC | Um modelo que chuta tem PR-AUC igual à proporção de positivos. Reportar essa proporção ao lado, para dar escala ao número |
| ROC-AUC | Sobre as probabilidades, sem limiar. `scoring="roc_auc"` |
| Onde | Nas partições de validação da #28, agrupadas por aluno ou temporais, as mesmas para todos os modelos. Média e desvio entre as partições |
| Teste | Usado uma única vez, com os hiperparâmetros e o limiar já escolhidos |

### Regra do limiar

1. **Previsões fora da partição.** Com os hiperparâmetros escolhidos, gerar as probabilidades de cada linha do treino quando ela estava na partição de validação (*out-of-fold*).
2. **Escolher o limiar.** Nessas previsões, escolher o limiar que maximiza o F2. O F2 é a variante do F1 que dá duas vezes mais peso ao Recall do que à Precision. Ele preserva a preocupação de não perder casos de saída, sem permitir que o modelo marque todo mundo.
3. **Aplicar no teste.** Usar esse limiar, fixo, no conjunto de teste.
4. **Mesmo procedimento em todos os modelos.** É isso que deixa a comparação justa, e não um número fixo: cada modelo, com ou sem peso de classe (#54), fica no seu próprio ponto equivalente.
5. **Sensibilidade.** Reportar também Recall, Precision e F1 no limiar 0,5, marcados como análise de sensibilidade.

### O que reportar por modelo

| Validação cruzada | Teste, no limiar do F2 | Teste, no limiar 0,5 (sensibilidade) |
| --- | --- | --- |
| PR-AUC (média ± desvio), ROC-AUC (média ± desvio), limiar escolhido | PR-AUC, ROC-AUC, **Recall**, Precision, F1, F2, matriz de confusão (TN, FP, FN, TP) | Recall, Precision, F1, matriz de confusão |

Junto da tabela: a proporção de positivos no treino e no teste, a regra da variável-alvo, a divisão e a validação usadas e a semente.

### O que mudar no `decisoes_metricas_modelagem.md` (PR #65)

- **Linha "Recall (sensibilidade) — principal":** vira "métrica principal de leitura". O Recall continua em destaque, mas não escolhe hiperparâmetros.
- **Nova linha PR-AUC:** métrica de seleção e comparação, com a justificativa acima.
- **Linha ROC-AUC:** fica como complementar, com a observação de que é otimista com positivos raros.
- **Nova linha F2:** usada só para escolher o limiar.
- **"Critério primário de hiperparâmetros":** trocar "maximizar o Recall" por "maximizar a PR-AUC (precisão média) na validação cruzada".
- **"Desempate":** pode sair. Se ficar, definir que empate é uma diferença menor que o desvio entre partições.
- **"Limiar: usar 0,5":** trocar pela regra do F2 acima e manter o 0,5 como sensibilidade.
- **Tabela de resultados:** usar as colunas da tabela acima.
- **O que fica como está:** a regra da matriz de confusão, a ROC-AUC calculada sem limiar, o cuidado com a proporção de positivos e a seção de limites.

O `modelos_utilizados.md` (#30) será ajustado para a mesma regra antes de subir: a busca do Optuna passa a otimizar a PR-AUC.

## Pendências

**A verificar:**

| Ponto | O que sabemos | O que verificar | Opções |
| --- | --- | --- | --- |
| GAE (Curso Aluno Especial) | 27 linhas e 26 alunos, 3 deles com evento de saída. 24 das 33 linhas com período 0 são do GAE | O que é o aluno especial no Inatel: se faz disciplinas avulsas sem vínculo de graduação e se pode migrar para um curso regular | Excluir da população; manter só se for graduação |
| Prazo de integralização esgotado | 26 alunos: 24 voltaram a cursar em até 2 semestres; 13 têm data de diplomação posterior à data do prazo (um no mesmo semestre, mas em data posterior); 8 tiveram saída formal no mesmo semestre ou depois. Os grupos se sobrepõem. | O prazo indica limite de 20 semestres e necessidade de novo vestibular; não é desligamento por si só. | Manter os alunos e não usar o flag como saída ou exclusão. Aplicar a regra usual: só evento formal sem retorno na janela classifica evasão. |

**Cálculos para fechar a #18:**

- [x] Recalcular a curva de retorno ancorada no último semestre cursado. N = 2 permanece provisório; a curva ainda sobe até k = 5 e requer confirmação da orientadora/revisor.
- [x] Quantificar positivos, negativos, excluídos e proporção na base v4; ver `docs/definicao_variavel_alvo.md`.
- [x] Usar como início o último semestre cursado, uma linha por aluno-semestre, e registrar a sensibilidade pela saída formal.
- [ ] Definir a consolidação dos indicadores de currículos diferentes no mesmo aluno-semestre para a preparação do dataset (#20).

**Ajustes nos documentos:**

- [ ] Ajustar o documento de métricas da PR #65 (seção Métricas e limiar).
- [ ] Ajustar o `modelos_utilizados.md` para otimizar a PR-AUC e abrir a PR da #30.
- [ ] Registrar a regra da variável-alvo na #18 e levar à orientação.
