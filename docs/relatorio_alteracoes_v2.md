# Alterações da análise consolidada — 01/10/2026

Entrega: [pre_defesa_analise_exploratoria_v2.ipynb](pre_defesa_analise_exploratoria_v2.ipynb), derivado das 64 células do notebook original do OneDrive. As 22 perguntas mantêm sua ordem, assim como os tipos de gráficos úteis e a bibliografia integral. As versões revisada (`analise_evasao_revisada.ipynb`, referência local não publicada) e complementar (`analise_evasao_complementar.ipynb`, referência local não publicada) servem de referência técnica e permanecem intactas, junto com seus relatórios.

Os identificadores `original-00` a `original-63` nas células permitem localizar a seção de origem; células de apoio têm prefixo `apos-`. A redação foi encurtada e os cálculos necessários foram substituídos dentro da sequência original. Este documento concentra a auditoria para evitar repeti-la no notebook.

## Critérios usados antes dos resultados

Os quatro flags de desistência, abandono, cancelamento e desligamento identificam **eventos de saída observados**, sem fixar evasão definitiva. Transferência/afastamento, trancamento, retorno e conclusão são tratados separadamente. Um flag positivo é preservado pela união dos registros do mesmo aluno/semestre; a contagem de linhas não identifica episódios.

O retrato anterior é o registro acadêmico do maior semestre **estritamente anterior à primeira saída**. Havendo múltiplos registros acadêmicos nesse último semestre, o retrato é ambíguo e não se escolhe uma linha nem se recua para um semestre menos recente. Ocorrências e mudanças de vínculo são preservadas na base em memória. Comparações exigem o semestre calendário imediatamente anterior, informação de curso/período e estrato comum.

- **V0:** primeira saída em `t`, registro acadêmico único em `t−1`, sem conclusão até `t`. Referências Ativo e com matrícula efetivada em `t−1`, sem primeira saída/conclusão até `t`, no mesmo semestre, curso e período curricular. Podem sair posteriormente.
- **V1:** acrescenta Ativo e matrícula efetivada em `t−1` também aos casos.
- **V2:** mantém V1 e exige nas referências ao menos uma matrícula `ACADEMICA` efetivada em `t`, em qualquer curso. Essa confirmação não exige status Ativo nem unicidade do registro em `t`; não confirmação não implica evasão.

V0 permanece como referência descritiva explícita; V1/V2 são sensibilidades. Para cada indicador, ausências e estratos sem informação nos dois grupos são retirados da comparação e contabilizados. O peso das referências em cada estrato é `n_casos / n_referências`; a soma dos pesos corresponde ao número de casos informados. Pessoas podem ser referências em vários semestres. A padronização não elimina confundimento.

As trajetórias T0/T1/T2 usam os mesmos alunos em cada um dos três semestres anteriores, independentemente de V1/V2. T1 exige curso estável; T2 exige o mesmo vínculo **aluno–currículo**, com informação completa. Não se exige estabilidade em toda a carreira.

## Auditoria por seção original

Cada tabela distingue o que foi preservado, corrigido ou suspenso. Suspensão significa que a interpretação ou cálculo exige definição institucional, não que os registros foram apagados.

### 1. O que a base representa?

| Componente | Situação | Motivo e tratamento |
|---|---|---|
| Cobertura e estrutura longitudinal | Preservada | Confirmados 59.059 registros, 7.615 alunos, 35 semestres (2009/1–2026/1) e 12 siglas de curso. Mantidos CRISP-DM e Tinto como apoio. |
| Leitura e unidade dos registros | Corrigida | Caminhos configuráveis; leitura direta do OneDrive. Separados 44.417 registros acadêmicos e 14.642 ocorrências. Matrícula e nascimento não são carregados; nenhum identificador é salvo nas saídas. |

### 2. Os estudantes aparecem em vários semestres?

| Componente | Situação | Motivo e tratamento |
|---|---|---|
| Histograma de semestres distintos por aluno | Preservada | A operação original já usava semestres distintos. Mantida como cobertura observada, sem equivaler a duração contínua ou tempo de exposição comparável. |

### 3. Distribuição por curso

| Componente | Situação | Motivo e tratamento |
|---|---|---|
| Alunos distintos por curso e gráfico de barras | Preservada | Conta vínculos observados em cada curso; alunos com mudanças podem aparecer em mais de um curso. A sigla GAE existe nos dados, mas não está documentada. |

### 4. Quantos estudantes apresentam eventos de saída?

| Componente | Situação | Motivo e tratamento |
|---|---|---|
| Conjunto provisório dos quatro eventos e alunos com saída | Preservada | Mantidos os 3.507 alunos e a separação de transferência/afastamento. O original já distinguia evento de evasão definitiva. |
| Quantidade de ocorrências | Corrigida | Há 3.841 linhas positivas e 3.728 pares aluno/semestre positivos. A soma de linhas deixou de ser denominada número de ocorrências independentes. Flags completos e binários: a antiga imputação de flags de saída não alterava o resultado atual. |

### 5. Tipos de saída

| Componente | Situação | Motivo e tratamento |
|---|---|---|
| Tabela e gráfico por tipo | Corrigida | Mostram linhas, alunos/semestres e pessoas separadamente. O gráfico conta 2.267 pares com desistência, 700 com abandono, 765 com cancelamento e 1 com desligamento. Tipos podem se sobrepor; valores pequenos recebem rótulos. |

### 6. Distribuição temporal das saídas

| Componente | Situação | Motivo e tratamento |
|---|---|---|
| Alunos distintos com saída por semestre | Preservada | O original já evitava somar linhas no gráfico. A série inclui semestres sem positivos; mantém-se a distinção entre quantidade de eventos e taxa de evasão. |

### 7. Proporções por curso

| Componente | Situação | Motivo e tratamento |
|---|---|---|
| Proporção histórica no curso observado | Preservada | Mantido numerador de pessoas com flag no curso e denominador de pessoas observadas no curso. Não é incidência por coorte nem comparação ajustada por seguimento. Sobreposição entre cursos é explícita. |

### 8. Sexo e turno

| Componente | Situação | Motivo e tratamento |
|---|---|---|
| Sexo e qui-quadrado exploratório | Corrigida | Uma observação por pessoa com sexo consistente; categoria sem informação explícita (9 pessoas). F/M reproduzem 41,60% e 47,33% com saída. Teste com 7.606 pessoas: χ²=17,09785; p=0,00003550; menor esperado=773,04. A associação bruta não ajusta curso, coorte ou duração observada. |
| Turno e gráfico | Preservada | Recuperados os resultados originais: Integral 2.405/5.774 (41,65%) e Noturno 1.164/2.666 (43,66%). Há 825 pessoas em ambos os turnos; categorias não são grupos exclusivos. |

### 9. Semestre anterior, referências e status

| Componente | Situação | Motivo e tratamento |
|---|---|---|
| Seleção anterior à saída | Corrigida | A antiga escolha recuava uma linha: 139 de 1.896 retratos eram do semestre de saída e 546 eram ocorrências, com sobreposição. Agora são 1.489 retratos únicos em t−1, 390 com lacuna, 1 ambíguo e 1.627 sem semestre acadêmico anterior. |
| Repetições e mudanças de vínculo | Corrigida | Zero duplicatas integrais na auditoria anterior. Dos 48.200 pares aluno/semestre, 8.825 são repetidos com vínculos curriculares distintos; 1.104 têm vínculos semestrais distintos e 972 múltiplos cursos. Só 47 pares têm múltiplas linhas acadêmicas. Repetição não é excluída indiscriminadamente. |
| Comparabilidade e situação final | Corrigida | Critérios V0/V1/V2 e pesos aparecem antes dos resultados. Todos os status do último semestre são considerados: sem saída há 267 Inativo unívocos, 946 indefinidos e 15 conflitos, em vez dos 314 obtidos pela antiga última linha. Nenhum é automaticamente evadido. |
| Evasão definitiva e resolução dos empates | Suspensa | Faltam regra institucional, ordenação intrassemestre e vínculo do desfecho. Conclusão existe em 2.867 alunos: 21 antes/no semestre da primeira saída e 156 depois dela; categorias não são exclusivas. |

### 10. Preparação numérica

| Componente | Situação | Motivo e tratamento |
|---|---|---|
| Conversão decimal | Preservada | A conversão de vírgula para ponto era adequada. Centralizada em uma função, sem sobrescrever valores originais em memória. |
| Domínios, unidades e ausências | Corrigida | Ausências não viram zero ou “não”. Dois valores de frequência acima de 100% são mascarados somente na coluna analítica; nenhuma falha de conversão. CRE é apresentado na escala observada 0–100; contagens e categorias têm unidades próprias. |

### 11. CRE antes da saída

| Componente | Situação | Motivo e tratamento |
|---|---|---|
| Comparação e distribuição de CRE | Corrigida | Substituído o último registro de pessoas sem saída por referências comparáveis no calendário/curso/período. Mantido gráfico de caixas, agora com quantis ponderados e hastes P5–P95. Sensibilidades V1/V2 permanecem explícitas. |

### 12. Aprovação e reprovação

| Componente | Situação | Motivo e tratamento |
|---|---|---|
| Distribuições das contagens registradas | Corrigida | Mantidos os dois gráficos, com unidade quantidade e rótulo de janela pendente. IA75_03 e IA34_03 não são percentuais. |
| Taxas e interpretação como desempenho do semestre | Suspensa | Em linhas acadêmicas há 5.388 contagens de aprovadas acima de matriculadas e 140 de reprovadas acima. Confirmar SQL, janela acumulada/semestral, aproveitamentos e vínculos antes de dividir por IA75_04 ou atribuir significado ao contraste. |

### 13. Frequência e faltas por disciplina

| Componente | Situação | Motivo e tratamento |
|---|---|---|
| Frequência, gráfico e sensibilidades | Corrigida | Mesmos critérios temporais e pesos do CRE. Excluídos valores fora do domínio; zeros conhecidos preservados. |
| Disciplinas com mais de 25% de faltas | Corrigida | Mantida pergunta, com denominadores e proporções, além da quantidade média. Em V0: 1,005 contra 0,233 disciplinas; ao menos uma em 37,70% contra 12,88% das referências padronizadas. Não é comparação de contagens brutas de grupos de tamanhos diferentes. |

### 14. Trancamento anterior

| Componente | Situação | Motivo e tratamento |
|---|---|---|
| Histórico e gráfico | Corrigida | Histórico termina em t−1 para ambos os grupos V0. A regra antiga incorporava trancamento somente posterior à primeira saída em 56 pessoas. Agora 16,87% dos casos versus 2,37% das referências padronizadas têm flag anterior; a duração de exposição ao histórico continua variável. |

### 15. Dimensão financeira

| Componente | Situação | Motivo e tratamento |
|---|---|---|
| Bolsa, FIES, perda de FIES e gráfico | Corrigida | Indicadores do retrato t−1, sem máximos sobre toda a trajetória. A antiga regra incorporava positivos apenas posteriores em 82, 25 e 15 pessoas, respectivamente. Bolsa ausente permanece desconhecida; proporção de bolsa positiva é entre percentuais informados. |
| Explicação financeira da saída | Suspensa | Bolsa positiva 96,21%/96,61% é condicional à informação: 369 casos e 3.419 referências. FIES 2,80%/5,12%; perda de FIES 1,02%/0,13%. Esses números não comprovam cobertura populacional ou efeitos. Confirmar nulos e atualização retrospectiva. |

### 16. Renda, patrimônio e escolaridade

| Componente | Situação | Motivo e tratamento |
|---|---|---|
| Resumo geral de renda | Preservada | Mantidos quantidade informada, média, desvio-padrão e quartis da extração. O denominador é linha e inclui repetições e registros posteriores; é descrição da base, não fator anterior à saída. Extremos individuais não são exibidos. |
| Comparações e gráficos familiares | Corrigida | Retratos V0, pesos comuns e zeros preservados. Rendas usam escala symlog, que inclui zero. Patrimônio/escolaridade incluem ausências no denominador e não descartam categorias por reindexação. Corrigida a renderização de R$ nos rótulos. |
| Interpretação socioeconômica | Suspensa | Rendas entram com 395 casos e 3.998 referências; faltam em 72,75%/66,05% das respectivas amostras V0. Data de coleta, atualização e comparabilidade monetária não estão documentadas. |

### 17. Momento da saída na trajetória

| Componente | Situação | Motivo e tratamento |
|---|---|---|
| Contagem e histograma | Corrigida | A posição da primeira linha positiva contava linhas, inclusive repetições. Agora são semestres distintos anteriores: média 2,065 com qualquer origem e 1,887 acadêmicos, ambos com mediana 1, entre 3.507 pessoas. Zero não significa ingresso e saída imediatos; faltam registros anteriores em parte das trajetórias. |
| Duração desde ingresso e risco por semestre | Suspensa | Exigem data de ingresso, população em risco e seguimento/censura; não são estimados a partir dessa distribuição. |

### 18. Retorno após saída

| Componente | Situação | Motivo e tratamento |
|---|---|---|
| Reingresso após a última saída | Preservada | Os 68 casos do original continuam reproduzidos. “Não reingressou” foi substituído por ausência de flag posterior observado. |
| Evidências após a primeira saída | Corrigida | Acrescentados 138 reingressos formais, 398 matrículas acadêmicas efetivadas e 156 conclusões posteriores, com sobreposição. Primeira e última saída respondem a perguntas diferentes. |
| Retorno no mesmo semestre e saída definitiva | Suspensa | Não há ordem intrassemestre nem janela institucional de ausência; nenhum grupo sem evidência posterior é automaticamente evadido. |

### 19. Múltiplas saídas

| Componente | Situação | Motivo e tratamento |
|---|---|---|
| Histograma e contagem por estudante | Corrigida | Contam semestres distintos positivos, evitando confundir várias linhas de um semestre com vários episódios. Há 202 pessoas com mais de um semestre positivo; máximo de 4. Identificar episódios exige regra e datas institucionais. |

### 20. Trajetória de CRE

| Componente | Situação | Motivo e tratamento |
|---|---|---|
| Curva de média e mediana | Corrigida | t−3/t−2/t−1 são semestres calendário, não posições de linhas. O painel principal contém os mesmos 464 alunos em todos os pontos. A cobertura disponível por semestre é mostrada separadamente. |
| Estabilidade de curso e vínculo | Corrigida | Preservadas sensibilidades da revisão complementar: 431 e 340 alunos, excluindo 33 e 124 do painel. São populações diferentes; não se interpreta a diferença como efeito da mudança curricular. |

### 21. Qualidade dos dados

| Componente | Situação | Motivo e tratamento |
|---|---|---|
| Gráfico e tabela de ausência | Corrigida | Usa apenas colunas originais; separa nulos de categorias sem informação. Evita repetir colunas convertidas no ranking e documenta zeros. |
| Dicionário e temporalidade | Suspensa | Legenda contém TEVETRASAFASTAMENTO, mas CSV TEVETRANSAFASTAMENTO. Faltam ORIGEMREGISTRO, QUANTIDADEOCORRENCIAS e GAE (27 linhas). Confirmar status, datas e disponibilidade histórica. |

### 22. Síntese da análise

| Componente | Situação | Motivo e tratamento |
|---|---|---|
| Síntese e conclusões descritivas | Corrigida | Atualizada com médias executadas, dependência da frequência à elegibilidade, seleção dos painéis e limitações financeiras. Retiradas conclusões apoiadas na antiga última linha ou em unidades incorretas. |

### Encerramento e referências

| Componente | Situação | Motivo e tratamento |
|---|---|---|
| Planejamento da apresentação | Suspensa | O pedido atual é análise; substituído por pontos de discussão metodológica, sem slides ou planejamento de fala. O texto original permanece no OneDrive. |
| Bibliografia | Preservada | Última célula mantida integralmente, com Tinto, Oliveira/Medeiros, Barbosa et al. e CRISP-DM. Completude e formatação das referências bibliográficas continuam para revisão acadêmica. |

## Reconciliação com as revisões anteriores

As amostras, médias de CRE/frequência V0/V1/V2 e trajetórias T0/T1/T2 reproduzem as saídas executadas da revisão complementar, dentro da precisão salva de seis casas decimais. V0 e T0 também mantêm a revisão inicial. Valores abaixo são arredondados diretamente do cálculo.

| Versão | Indicador | Casos usados | Referências aluno/semestre usadas | Média casos | Média referências padronizada | Diferença |
|---|---|---:|---:|---:|---:|---:|
| V0 | CRE | 1.266 | 15.042 | 23,65 | 51,83 | −28,18 |
| V1 | CRE | 1.239 | 14.945 | 23,80 | 51,84 | −28,04 |
| V2 | CRE | 1.239 | 14.651 | 23,80 | 52,31 | −28,50 |
| V0 | Frequência (%) | 1.464 | 16.511 | 68,00 | 90,53 | −22,52 pp |
| V1 | Frequência (%) | 1.240 | 14.945 | 78,91 | 90,60 | −11,70 pp |
| V2 | Frequência (%) | 1.240 | 14.651 | 78,91 | 90,73 | −11,82 pp |

V0 parte de 1.480 casos elegíveis; 16 não têm estrato comum e restam 1.464, com 16.511 referências de 4.915 pessoas. V1 exclui 224 casos: 205 Inativo, 15 Desconhecido e 4 Matrícula Pendente. Restam 1.240 casos, 14.945 referências de 4.889 pessoas e 531 estratos. CRE ausente cai de 198 casos para 1; o número informado cai apenas 27. As 1.469 referências com CRE fora do suporte de casos informados em V0 são contabilizadas, não ausentes.

Em V1, 14.651 referências têm matrícula acadêmica efetivada em t e 294 não têm essa confirmação. V2 retira as 294, mantendo os casos e os estratos. A distribuição alvo dos casos é a mesma; **os pesos das referências são recalculados** com o novo denominador de cada estrato. Frente a V0, V1 aumenta a média dos casos em 0,151 ponto de CRE e 10,905 pp de frequência. Frente a V1, V2 aumenta as médias das referências em 0,467 ponto de CRE e 0,130 pp de frequência. V2 seleciona continuidade observada e usa informação posterior ao retrato; é sensibilidade, não fator preditor.

| Painel | Alunos | Excluídos de T0 | CRE t−3 | CRE t−2 | CRE t−1 | Variação média |
|---|---:|---:|---:|---:|---:|---:|
| T0 completo | 464 | 0 | 33,25 | 29,32 | 21,70 | −11,55 |
| T1 curso estável | 431 | 33 | 32,90 | 29,10 | 21,92 | −10,97 |
| T2 vínculo curricular estável | 340 | 124 | 33,49 | 29,69 | 22,42 | −11,07 |

A queda média aparece nos três painéis; isso não demonstra causa nem representa todas as trajetórias de saída. O valor 29,33 em t−2 do primeiro relatório foi um arredondamento intermediário: o valor reproduzido é 29,3246767 e arredonda diretamente para **29,32**, como no complemento.

Diferenças adicionais têm motivo explícito:

- O CRE original 24,01/69,65 mistura períodos e escolhas de registro; foi substituído, não reconciliado como estimativa equivalente.
- Os gráficos de caixas agora representam os mesmos pesos das tabelas. Hastes são P5/P95 e quartis interpolados pela distribuição acumulada ponderada, sem pontos individuais; não são hastes de Tukey. O resumo geral de renda permanece separado das comparações anteriores à saída.
- O trancamento 16,87%/2,37% usa V0 pareado e histórico anterior para os dois grupos. Os 642 alunos com trancamento anterior na revisão inicial descreviam todos os alunos com saída, outra população. Não são numeradores intercambiáveis.
- Finanças e renda passam a ter tabelas e gráficos completos na sequência original, com o mesmo recorte temporal das revisões. Mensalidade média informada padronizada continua igual nos grupos (R$ 1.807,94). Rendas médias mãe/aluno/pai são R$ 2.445,19/909,38/2.493,37 nos casos e R$ 2.859,35/917,41/3.077,32 nas referências; cobertura e temporalidade impedem explicações causais.
- Percentuais de patrimônio/escolaridade agora incluem ausentes no denominador e referências padronizadas. Diferem do original, que retirava nulos e usava referências de outros períodos. Todas as categorias observadas são mantidas.
- A tabela de bolsa mostra 1.093 casos sem informação, 369 utilizados e 2 informados sem referência informada compatível. Renda tem 1.065 casos sem informação, 395 utilizados e 4 fora do suporte. Nas referências, informação ausente e informação fora do suporte dos casos são contadas separadamente. A soma das referências usadas com as ausentes, sozinha, não recompõe a amostra.

## Pendências com instituição e orientador

Definir evasão do curso ou da instituição, cancelamento/transferência, duração sem retorno, episódios e censura. Confirmar ordenação intrassemestre, temporalidade de flags/status, unidade de ocorrências e tratamento de vínculos. Validar SQL das contagens, escala formal do CRE, frequências fora do domínio, nulos financeiros e data de atualização das informações familiares. Discutir estratos, elegibilidade equivalente e confirmação em t sem transformar sensibilidades em definição silenciosa.

A extração termina em 2026/1 e pode começar depois do ingresso. Seleção por histórico, permanência confirmada e estabilidade muda a população; referências repetidas não são independentes. A análise de sexo é exploratória e não ajusta diferenças de seguimento. Nenhum resultado estabelece causa.

## Execução, conferência visual e preservação

O notebook final executou **31 células de código, do início ao fim em kernel limpo, sem erros**, com **23 gráficos incorporados**. Todos foram inspecionados visualmente; foram ajustados legendas, rótulos monetários e contagens pequenas. As tabelas principais foram confrontadas com as saídas dos notebooks anteriores. Uma leitura independente com `csv.DictReader` e estruturas Python reconciliou semestres distintos, trancamento anterior, finanças, rendas e qui-quadrado. Asserções verificam temporalidade, unicidade dos retratos, soma dos pesos, painéis completos e integridade das fontes.

Leitura configurável pelas variáveis `TCC_CSV_PATH`, `TCC_LEGENDA_PATH` e `TCC_NOTEBOOK_ORIGINAL_PATH`, ou pela célula de configuração. O CSV não foi copiado; dados individuais ficaram em memória. Saídas salvas contêm tabelas agregadas e gráficos sem pontos individuais.

Os três originais e os quatro artefatos anteriores tiveram integridade conferida por SHA-256, sem mudanças. Hashes dos arquivos de origem nesta execução:

| Fonte do OneDrive | SHA-256 |
|---|---|
| dados_alunos.csv | `ad2138cee12e97ab27f149228e22a9298dc15ac5ac3f40a4d4cf2fcd714c0f19` |
| Legenda.md | `65e7e8128b667d5499d08a49dddf1502f66f5c340b74f338c426d424ecfbea33` |
| pre_defesa_analise_exploratoria.ipynb | `99f507491340c50bcd235367653e88dd728022df518c1552c6f742a6e27ebe37` |

Não houve slides, treinamento de modelos, commit ou push.

## Acabamento visual — 01/10/2026

| Ajuste | Aplicação |
|---|---|
| Cores dos grupos | Casos em laranja (`#ff7f00`) e referências em azul (`#377eb8`) em todos os gráficos que comparam esses grupos, incluindo caixas e barras. |
| Frequência nas sensibilidades | Eixo limitado a 0–100%; legendas posicionadas abaixo dos painéis, sem cobrir barras. |
| Leitura dos gráficos de caixas | Nota junto às figuras identifica quartis P25–P75, linha da mediana e hastes P5–P95, e explica a ponderação das referências por semestre, curso e período para reproduzir a distribuição dos casos informados. Rótulos de N distinguem alunos dos casos de unidades aluno/semestre das referências. |

As versões antes e depois do acabamento executaram novamente em kernels limpos, com 31 células de código cada e sem erros. As **46 tabelas agregadas ficaram idênticas**, comparadas com precisão de 15 casas decimais, e todas as saídas não gráficas permaneceram iguais à entrega anterior. Os **dez gráficos comparativos afetados** foram conferidos visualmente. Cálculos, critérios, amostras, ordem e quantidade de células, demais textos e referências foram preservados. Os originais do OneDrive e as versões anteriores permaneceram intactos por conferência de hash; somente saídas agregadas foram salvas. Sem commit ou push.


## Preparação para publicação

Esta v2 é uma cópia da última versão executada de `pre_defesa_analise_consolidada.ipynb`, com nomes e configuração adequados à publicação. Os arquivos de apoio e originais do OneDrive continuam preservados localmente. Os caminhos padrão deixaram de depender de pasta pessoal: CSV via `TCC_CSV_PATH` (padrão `dados_alunos.csv`), legenda via `TCC_LEGENDA_PATH` (padrão junto ao CSV) e original via `TCC_NOTEBOOK_ORIGINAL_PATH` (padrão `pre_defesa_analise_exploratoria.ipynb` no diretório de execução).

| Arquivo | Ajuste ou remoção |
|---|---|
| Original publicado | Import de `os` e CSV configurável por `os.environ.get("TCC_CSV_PATH", "dados_alunos.csv")`. É ajuste de configuração; cálculos históricos permanecem. Quatro saídas de figuras com pontos de observações individuais (outliers), nas células 33, 36, 38 e 46 (índices a partir de zero), foram removidas da cópia pública. Tabelas e demais gráficos agregados permanecem. |
| v2 publicada | Removidos dois logs de instalação que continham caminhos pessoais. Nenhuma tabela ou gráfico da v2 foi removido. Retirado o caminho pessoal padrão e ajustado o nome do relatório. |
| Ambos os notebooks | Retirados metadados de sessão/execução e do Colab; preservados kernel, linguagem e contadores das execuções armazenadas. Não foram encontradas credenciais nem tabelas com linhas identificadas de alunos. |
| Relatório | Links locais convertidos em relativos; referências aos arquivos intermediários permanecem como referências locais não publicadas. |

**Validação desta etapa:** todos os demais blocos de código da v2 ficaram textualmente idênticos; o bloco após a configuração também é idêntico por comparação de AST. Todas as tabelas agregadas e os 23 gráficos incorporados da última execução foram preservados exatamente. Não houve nova execução dos notebooks nesta preparação: a validação é de equivalência de código e saídas armazenadas. Os registros de execução das seções anteriores referem-se às verificações anteriores à publicação, não a uma execução nova.

O CSV e a legenda ficam fora do GitHub. A main conserva o original preparado como referência histórica; a revisão é proposta em branch separada, sem merge ou merge automático. Não houve treinamento de modelos nesta etapa.
