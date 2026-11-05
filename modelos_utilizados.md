# Modelos de aprendizado de máquina: justificativa, papel e configuração dos experimentos (#30)

## 1. Introdução

Este trabalho propõe a comparação de quatro modelos de classificação para investigar padrões associados à evasão acadêmica: Regressão Logística, Árvore de Decisão (*Decision Tree*), Random Forest e XGBoost.

A escolha desses modelos atende a duas necessidades da pesquisa. A primeira é avaliar a capacidade de cada abordagem de distinguir os registros associados à evasão daqueles em que esse evento não foi observado. A segunda é compreender quais variáveis e combinações de características aparecem relacionadas às classificações feitas pelos modelos.

Por esse motivo, a comparação não se baseia apenas no desempenho. A possibilidade de interpretar os resultados também é considerada. Um modelo com desempenho ligeiramente inferior, mas que permita uma leitura mais clara das relações identificadas, pode contribuir de forma importante para a discussão.

Os modelos não serão utilizados para afirmar que determinada característica causa a evasão. Os resultados serão interpretados como associações e padrões identificados nos dados disponíveis. A pesquisa busca compreender melhor o fenômeno nos cursos de engenharia do INATEL, e não desenvolver um sistema de decisão individual sobre os estudantes.

A comparação entre os quatro modelos também permite observar como diferentes abordagens representam os dados: desde relações mais simples entre as variáveis até combinações não lineares e interações mais complexas.

## 2. Características dos dados e implicações para a modelagem

A base utilizada no projeto tem estrutura longitudinal, com registros de um mesmo estudante em diferentes semestres. Essa característica exige atenção especial na preparação dos dados e na validação dos modelos, pois os registros de um mesmo aluno não são observações independentes.

A definição da variável-alvo está em consolidação na issue #18 (PR #68, em revisão). Pela proposta atual, o evento positivo é a evasão da instituição sem retorno. Ela ocorre quando o estudante tem um evento formal de saída (desistência, abandono, cancelamento, desligamento ou transferência para outra instituição) e não volta a ter matrícula efetivada em nenhum curso do INATEL nos semestres seguintes. A unidade de análise é o registro do estudante por semestre cursado. O evento positivo é associado ao último semestre efetivamente cursado antes da saída. Semestres trancados não são considerados semestres cursados.

A janela usada para confirmar a ausência de retorno também está em avaliação. A proposta é usar quatro semestres, contados a partir do semestre da saída, com uma janela de dois semestres como análise de sensibilidade.

Na versão atual da proposta, aplicada à base v4, a janela de quatro semestres resulta em 1.878 registros positivos e 38.520 negativos, ou 4,65% de positivos. Com a janela de dois semestres, são 2.014 registros positivos e 38.304 negativos (5,00%). Esses números são provisórios. Eles ainda podem mudar com os ajustes em discussão na PR #68 e com a validação da definição pela orientação.

Essas proporções indicam um desbalanceamento entre as classes: os registros associados à evasão são uma parcela pequena do conjunto. Isso será considerado ao longo da modelagem, principalmente na escolha das métricas e no tratamento do desbalanceamento.

Outro aspecto importante são os valores ausentes. Nem todo campo vazio representa falta de informação no sentido tradicional. Em algumas situações, o valor não existe porque a condição não se aplica ao registro. A frequência, por exemplo, fica vazia quando o estudante não tem turma ativa no semestre. Também há campos financeiros e socioeconômicos sem preenchimento, porque essas informações vêm do processo de solicitação de bolsa.

Na base v4, 2.136 registros acadêmicos não têm informação de frequência. As variáveis socioeconômicas estão ausentes em 29.227 dos 44.417 registros acadêmicos. Esses valores precisam ser interpretados conforme o significado de cada variável, sem substituir automaticamente todos os campos vazios por zero.

Essas características influenciam a escolha dos modelos e o tratamento feito antes do treinamento:

| Característica da base | Implicação para a modelagem |
|---|---|
| Registros longitudinais por estudante | A validação precisa respeitar a separação por aluno e, se for o caso, a ordem temporal, conforme o protocolo da issue #28 |
| Classes desbalanceadas | Serão avaliadas estratégias de ponderação das classes e métricas adequadas à identificação dos casos positivos |
| Variáveis acadêmicas, financeiras e socioeconômicas, de tipos variados | Modelos lineares e baseados em árvores são adequados para dados tabulares desse tamanho, após o tratamento das variáveis |
| Valores ausentes com diferentes significados | O tratamento dos nulos deve considerar a natureza de cada variável e ser feito dentro das partições de treinamento |

## 3. Justificativa para a escolha dos modelos

Foram selecionados quatro modelos com características distintas, que permitem comparar diferentes formas de representar os dados.

A Regressão Logística foi incluída por oferecer uma referência mais simples e interpretável. A Árvore de Decisão representa as classificações por meio de regras. A Random Forest amplia essa abordagem combinando diversas árvores, enquanto o XGBoost constrói árvores em sequência, buscando melhorar o desempenho do conjunto.

A comparação entre essas abordagens permite avaliar se os modelos mais complexos oferecem ganhos relevantes em relação aos mais simples. Essa avaliação será feita a partir dos resultados experimentais, sem assumir de antemão que algum modelo terá desempenho superior.

| Modelo | Característica principal | Forma de interpretação |
|---|---|---|
| Regressão Logística | Modelo linear no logaritmo das chances do evento | Coeficientes e razões de chance |
| Árvore de Decisão | Classificação por regras e condições | Estrutura da própria árvore |
| Random Forest | Combinação de várias árvores independentes | Importância por permutação e SHAP |
| XGBoost | Construção sequencial de árvores, com correção dos erros anteriores | Importância por permutação e SHAP |

Outros modelos que aparecem nos trabalhos relacionados, como SVM, k-NN, Naive Bayes, redes neurais, LightGBM e CatBoost, não foram incluídos. Eles não acrescentam uma forma de interpretação diferente das oferecidas pelos quatro modelos escolhidos, e o escopo definido com a orientação prioriza a análise dos fatores associados, e não a busca do maior desempenho possível. LightGBM e CatBoost, além disso, pertencem à mesma família do XGBoost.

### 3.1 Regressão Logística

A Regressão Logística será usada como modelo de referência, principalmente pela possibilidade de interpretar a relação entre as variáveis explicativas e as chances de ocorrência do evento.

O modelo estima a probabilidade de uma observação pertencer a determinada classe por meio de uma função logística. Seus coeficientes representam a direção e a intensidade da associação entre cada variável e o logaritmo das chances de evasão, considerando as demais variáveis constantes.

Quando os coeficientes são exponenciados, obtêm-se as razões de chance (*odds ratios*), que auxiliam na interpretação. Para as variáveis numéricas padronizadas, essa leitura considera a variação de um desvio padrão. As variáveis categóricas codificadas em indicadores são interpretadas em relação à categoria de referência.

A escolha também encontra respaldo no estudo de Chagas, Gomide e Santana (2025), realizado com cursos de Engenharia da UFRJ-Macaé. Nesse trabalho, a Regressão Logística apresentou AUC de 0,805 no conjunto de teste, resultado praticamente igual ao do XGBoost (0,803). Isso reforça a importância de manter um modelo mais simples na comparação, mesmo diante de abordagens mais flexíveis.

Um cuidado necessário é a possível multicolinearidade. Variáveis muito correlacionadas podem tornar os coeficientes instáveis e dificultar sua interpretação individual. A regularização pode reduzir esse problema, mas não dispensa a análise das correlações entre as variáveis, prevista nas issues #23 e #26. Villar e Andrade (2024), por exemplo, excluíram a Regressão Logística de sua comparação por causa da multicolinearidade da base.

Outro ponto é o tratamento dos valores ausentes. Como a implementação da Regressão Logística não aceita esses valores diretamente, será usada uma etapa de imputação dentro do pipeline de treinamento, acompanhada de indicadores de ausência. Assim, o tratamento não usa informações das partições de validação ou teste, e o padrão dos valores ausentes não fica escondido.

### 3.2 Árvore de Decisão (*Decision Tree*)

A Árvore de Decisão foi selecionada pela capacidade de representar a classificação por meio de regras explícitas. O modelo divide os registros em grupos a partir de condições aplicadas às variáveis, o que permite visualizar quais combinações de características foram usadas nas decisões.

Neste trabalho, essa abordagem pode ajudar a mostrar combinações entre desempenho acadêmico, reprovações e outras características da trajetória do estudante. Os limites encontrados, porém, são determinados pelo treinamento e não devem ser interpretados como regras institucionais nem como relações causais.

A facilidade de visualização é uma das principais vantagens desse modelo. Oliveira e Medeiros (2024) usaram árvores de decisão em seu estudo sobre evasão, destacando a possibilidade de representar os resultados de forma compreensível. Barbosa et al. (2023) também incluíram esse modelo na comparação.

Uma limitação importante é a sensibilidade da árvore a variações nos dados. Pequenas alterações na amostra podem modificar suas divisões, e árvores muito profundas tendem a se ajustar demais aos dados de treinamento. No estudo da UFRJ-Macaé, a árvore foi o modelo com pior desempenho e o mais instável. Para reduzir esse risco, serão avaliados limites de profundidade, de quantidade mínima de registros por folha e de poda.

Na apresentação dos resultados, será preciso distinguir a árvore usada na avaliação de desempenho de uma eventual versão simplificada para facilitar a visualização no artigo. Caso seja usada uma versão podada apenas para ilustração, isso deverá ser explicitado.

### 3.3 Random Forest

A Random Forest combina várias árvores de decisão treinadas com diferentes amostras dos registros de treinamento. Na configuração tradicional, cada árvore usa uma amostra obtida com reposição (*bootstrap*) e considera apenas um subconjunto das variáveis em cada divisão.

A combinação das árvores tende a reduzir a variabilidade de uma árvore individual e permite representar relações não lineares e interações entre variáveis. Por isso, o modelo foi incluído para verificar se a combinação de árvores identifica padrões que as abordagens anteriores não representam com a mesma facilidade.

O estudo de Oliveira e Medeiros (2024) apresentou resultados favoráveis para a Random Forest, especialmente com SMOTE. Barbosa et al. (2023) também apontaram resultados relevantes para esse modelo, embora o artigo apresente divergências entre suas seções quanto ao modelo com melhor resultado.

Apesar da capacidade de classificação, a Random Forest não oferece a mesma facilidade de interpretação de uma árvore única. A importância das variáveis será analisada por permutação, calculada sobre os dados de validação, e complementada por SHAP.

A importância padrão, baseada na redução de impureza, não será usada isoladamente, pois tende a favorecer variáveis contínuas ou com muitas categorias. Além disso, quando duas variáveis têm correlação elevada, a importância pode se dividir entre elas, o que exige cuidado na interpretação.

### 3.4 XGBoost

O XGBoost usa uma estratégia de *boosting*, na qual as árvores são construídas em sequência. Cada nova árvore procura corrigir os erros do conjunto formado pelas anteriores. Essa estratégia permite representar relações não lineares e combinações entre variáveis, além de oferecer mecanismos de regularização para controlar a complexidade do modelo.

O XGBoost foi incluído por apresentar resultados competitivos em estudos sobre evasão acadêmica. Bettahi, Belouadha e Harroud (2025) obtiveram resultados expressivos com esse modelo e usaram SHAP para auxiliar na interpretação. No estudo de Chagas, Gomide e Santana (2025), o resultado do XGBoost ficou próximo ao da Regressão Logística.

Uma vantagem prática do XGBoost é o tratamento nativo de valores ausentes. Os valores faltantes podem ser mantidos durante o treinamento, sem a etapa de imputação usada na Regressão Logística.

Por outro lado, o modelo tem diversos hiperparâmetros que controlam a construção das árvores, a taxa de aprendizado e a regularização. Se não forem ajustados adequadamente, há risco de sobreajuste. Por isso, serão definidos limites para a busca, e a avaliação respeitará a separação entre treinamento, validação e teste.

A interpretação será complementada por SHAP, que permite analisar como as variáveis contribuem para as saídas do modelo. Essa análise servirá para compreender os padrões aprendidos, sem atribuir às variáveis um papel causal na evasão.

## 4. Relação com os trabalhos relacionados

A escolha dos modelos também considerou estudos que investigaram a evasão e o desempenho acadêmico com técnicas de aprendizado de máquina. A comparação desses trabalhos permite identificar as abordagens já usadas, os modelos mais frequentes e a forma como os resultados foram avaliados.

| Trabalho | Dados utilizados | Modelos considerados | Ajuste de hiperparâmetros | Tratamento do desbalanceamento | Principais resultados |
|---|---|---|---|---|---|
| Barbosa et al. (2023) | 1.429 registros do sistema acadêmico, cursos técnicos e superiores do IFPE | Árvore de Decisão, Random Forest e XGBoost | Sem busca sistemática; os autores citam essa ausência como limitação | Não descrito | Há divergência entre as seções: a tabela comparativa e a conclusão apontam a Random Forest (F1 de 0,83, sem ajuste), e o resumo e a discussão destacam o XGBoost após ajuste |
| Oliveira e Medeiros (2024) | Dados de autoavaliação de cursos de graduação da UFPB | SVM, Random Forest e Árvore de Decisão | Validação cruzada estratificada com dez partições | Subamostragem, SMOTE e ADASYN | A Random Forest com SMOTE obteve acurácia de 87,97%, precisão de 91,72%, recall de 91,67% e F1 de 91,57% |
| Chagas, Gomide e Santana (2025) | Estudantes de cursos de Engenharia da UFRJ-Macaé, com foco no desempenho do primeiro período | Regressão Logística, Árvore de Decisão e XGBoost | Optuna, validação cruzada com cinco partições e AUC como objetivo | Pesos de classe e ajuste posterior do limiar | No teste, a Regressão Logística obteve AUC de 0,805, a Árvore de Decisão 0,759 e o XGBoost 0,803 |
| Bettahi, Belouadha e Harroud (2025) | 17.883 registros de uma instituição marroquina e experimentos complementares com a base UCI | Nove modelos, entre eles Regressão Logística, Árvore de Decisão, Random Forest e XGBoost | Valores finais fixos, sem descrição do espaço de busca | Pesos de classe e limiar que maximiza o F1 na validação | O XGBoost obteve AUC de 0,993 e F1 de 0,911 no conjunto principal. A diferença em relação à Random Forest não foi estatisticamente significativa (p = 0,428). O estudo usou SHAP |
| Villar e Andrade (2024) | Base UCI "Predict Students' Dropout and Academic Success" (Realinho et al., 2022), com 4.424 estudantes do Instituto Politécnico de Portalegre, criada a partir do estudo de Martins et al. (2021) | Árvore de Decisão, SVM, Random Forest e diferentes modelos de *boosting* | Optuna e validação cruzada | SMOTE e ADASYN | LightGBM e CatBoost com Optuna tiveram os melhores resultados. A Regressão Logística foi excluída por multicolinearidade |

A análise mostra que árvores de decisão, Random Forest e XGBoost aparecem com frequência nos estudos sobre evasão acadêmica. A Regressão Logística também foi considerada em pesquisas que compararam modelos mais simples e interpretáveis com abordagens mais complexas.

Entre os estudos levantados, o de Chagas, Gomide e Santana (2025) é o mais próximo desta pesquisa. Ele usa dados de cursos de Engenharia, aplica uma metodologia estruturada e compara três dos quatro modelos selecionados. Seus procedimentos de ajuste serviram como uma das referências para a definição inicial dos hiperparâmetros.

Os resultados desses trabalhos, no entanto, não serão usados como referência direta para determinar qual modelo deve se sair melhor no INATEL. As bases têm características, populações, variáveis e formas de validação diferentes. Além disso, nenhum desses estudos separa os dados por aluno ou por período, porque suas bases têm um registro por estudante. A base deste TCC tem registros longitudinais ao longo dos semestres, o que exige cuidados específicos na separação dos dados.

Também se observou a ausência de busca sistemática de hiperparâmetros em alguns desses trabalhos. Por isso, este projeto registra previamente os espaços de busca e os critérios de avaliação, para que a comparação entre os modelos siga um procedimento definido.

Durante a revisão bibliográfica, foram identificadas duas informações que precisam ser corrigidas na documentação do projeto. O estudo de Oliveira e Medeiros (2024) é de autores vinculados ao IFPB e usa dados de autoavaliação da UFPB. O trabalho de Chagas, Gomide e Santana (2025) é um estudo de caso da UFRJ-Macaé, e não uma revisão sistemática. Essas correções devem ser levadas para a fundamentação teórica (#57) e para a revisão bibliográfica (#48).

## 5. Espaço de hiperparâmetros

A comparação entre os modelos será feita com ajuste de hiperparâmetros, buscando configurações adequadas para cada algoritmo. Os intervalos desta seção representam o espaço inicial de busca, e não resultados já obtidos. Eles ainda podem ser ajustados conforme as decisões finais sobre a variável-alvo, as variáveis explicativas, o protocolo de validação e o tratamento do desbalanceamento.

Uma regra vale para todos os modelos: qualquer transformação que dependa dos dados será ajustada exclusivamente na partição de treinamento de cada rodada. Isso inclui imputação, padronização, cálculo de pesos de classe e eventuais procedimentos de reamostragem. Assim, informações das partições de validação ou teste não são usadas no ajuste.

A busca será feita com Optuna, usando o amostrador TPE. Essa abordagem permite explorar espaços com muitos hiperparâmetros sem testar todas as combinações possíveis, o que seria especialmente custoso no caso do XGBoost.

Os hiperparâmetros `class_weight` e `scale_pos_weight` dependem da estratégia de desbalanceamento definida na issue #54. Se essa issue optar por reamostragem ou apenas pelo ajuste do limiar, esses parâmetros ficam fixos no valor neutro.

### 5.1 Regressão Logística

A implementação usará um pipeline com imputação pela mediana, indicadores de ausência e padronização das variáveis numéricas, seguido do classificador. Todas essas etapas serão ajustadas dentro das partições de treinamento.

| Hiperparâmetro | Intervalo proposto | Escala | Justificativa |
|---|---|---|---|
| `C` | 0,001 a 100 | Logarítmica | Controla a força da regularização. Valores menores aplicam regularização mais intensa |
| `l1_ratio` | 0 a 1 | Linear | Controla a combinação entre as regularizações L2 e L1; valores intermediários correspondem à Elastic Net |
| `class_weight` | `None` ou `"balanced"` | Categórica | Permite avaliar a ponderação das classes, conforme a issue #54 |

Parâmetros fixos:

- `solver="saga"`
- `max_iter=5000`

O solver `saga` foi escolhido por aceitar todas as combinações de regularização previstas. A partir da versão 1.8 do scikit-learn, o parâmetro `penalty` está obsoleto e a regularização é controlada por `l1_ratio`. A UFRJ-Macaé ajustou `penalty` e `C`, o que equivale a esta busca.

Nos testes com dados sintéticos, algumas configurações com valores altos de `C` geraram avisos de convergência após 5.000 iterações. Por isso, a implementação deverá monitorar esses avisos e avaliar o aumento de `max_iter`. Os coeficientes de modelos que não convergirem não deverão ser usados na interpretação.

### 5.2 Árvore de Decisão

| Hiperparâmetro | Intervalo proposto | Escala | Justificativa |
|---|---|---|---|
| `criterion` | `"gini"` ou `"entropy"` | Categórica | Define o critério usado para avaliar as divisões |
| `max_depth` | 2 a 10 | Inteira | Limita a profundidade da árvore e ajuda a controlar sua complexidade |
| `min_samples_leaf` | 10 a 200 | Logarítmica | Define a quantidade mínima de registros por folha, evitando grupos muito pequenos |
| `min_samples_split` | 20 a 400 | Logarítmica | Define a quantidade mínima de registros para dividir um nó |
| `ccp_alpha` | 0 a 0,01 | Linear | Controla a poda por custo-complexidade |
| `class_weight` | `None` ou `"balanced"` | Categórica | Permite avaliar a ponderação das classes, conforme a issue #54 |

Os intervalos de `criterion`, `max_depth`, `min_samples_leaf` e `min_samples_split` foram definidos a partir dos parâmetros usados no estudo da UFRJ-Macaé. O parâmetro `ccp_alpha` foi acrescentado para permitir a poda da árvore, considerando a instabilidade observada naquele estudo.

As implementações de árvores do scikit-learn aceitam valores ausentes diretamente, sem imputação. Esse comportamento vale também para a Random Forest.

O limite inferior de `min_samples_leaf` deverá ser revisto após a definição final da variável-alvo e do tamanho da amostra.

### 5.3 Random Forest

| Hiperparâmetro | Intervalo proposto | Escala | Justificativa |
|---|---|---|---|
| `n_estimators` | 200 a 1.000, de 100 em 100 | Inteira | Define a quantidade de árvores do modelo |
| `max_depth` | `None`, 4, 6, 8, 12, 16 ou 20 | Categórica | Controla a profundidade máxima das árvores |
| `min_samples_leaf` | 1 a 50 | Logarítmica | Controla o tamanho mínimo das folhas e ajuda a suavizar as árvores |
| `max_features` | `"sqrt"`, `"log2"`, 0,3 ou 0,5 | Categórica | Define a quantidade de variáveis consideradas em cada divisão |
| `max_samples` | 0,5 a 1,0 | Linear | Define a fração dos registros de treinamento usada por árvore |
| `class_weight` | `None`, `"balanced"` ou `"balanced_subsample"` | Categórica | Permite avaliar diferentes formas de ponderação das classes |

O parâmetro `bootstrap=True` será mantido fixo, pois é necessário para usar `max_samples`. Com a opção `"balanced_subsample"`, a ponderação das classes é recalculada na amostra de cada árvore.

Os valores usados por Bettahi, Belouadha e Harroud (2025), como 200 árvores e `max_features="sqrt"`, estão contemplados no espaço de busca.

### 5.4 XGBoost

O XGBoost usará `tree_method="hist"` e `eval_metric="logloss"` como configurações fixas. Os valores ausentes serão mantidos, aproveitando o tratamento nativo do algoritmo.

| Hiperparâmetro | Intervalo proposto | Escala | Justificativa |
|---|---|---|---|
| `n_estimators` | 100 a 1.000, de 50 em 50 | Inteira | Define a quantidade de árvores construídas |
| `learning_rate` | 0,01 a 0,3 | Logarítmica | Controla a contribuição de cada árvore adicionada ao conjunto |
| `max_depth` | 2 a 8 | Inteira | Limita a profundidade das árvores |
| `min_child_weight` | 1 a 20 | Logarítmica | Controla o peso mínimo necessário para formar uma nova folha |
| `subsample` | 0,6 a 1,0 | Linear | Define a fração de registros usada por árvore |
| `colsample_bytree` | 0,5 a 1,0 | Linear | Define a fração de variáveis considerada por árvore |
| `gamma` | 0 a 5 | Linear | Define o ganho mínimo necessário para fazer uma divisão |
| `reg_lambda` | 0,001 a 10 | Logarítmica | Controla a regularização L2 |
| `reg_alpha` | 0,001 a 10 | Logarítmica | Controla a regularização L1 |
| `scale_pos_weight` | 1 ou razão entre negativos e positivos na partição de treinamento | Categórica | Permite ajustar o peso da classe positiva, conforme a issue #54 |

A configuração segue de perto os parâmetros do estudo da UFRJ-Macaé. Alguns parâmetros presentes naquele trabalho, como `max_delta_step` e `grow_policy`, não foram incluídos inicialmente, para manter o espaço de busca mais controlado.

Os valores finais usados por Bettahi, Belouadha e Harroud (2025) estão contemplados nos intervalos definidos: 200 árvores, taxa de aprendizado de 0,05, profundidade 8, `subsample` e `colsample_bytree` de 0,8 e regularizações iguais a 2.

## 6. Estratégia de busca e avaliação

A busca dos hiperparâmetros será feita com Optuna e amostragem TPE. O orçamento inicial proposto para cada modelo é:

| Modelo | Número de tentativas proposto |
|---|---:|
| Regressão Logística | 50 |
| Árvore de Decisão | 50 |
| Random Forest | 100 |
| XGBoost | 150 |

Será usada uma semente fixa no amostrador e nos modelos, para facilitar a reprodução dos experimentos.

Cada tentativa será avaliada conforme o protocolo de validação da issue #28. Como a base tem vários registros por estudante, a proposta é que a separação dos dados seja agrupada por aluno, de modo que um mesmo estudante não apareça ao mesmo tempo nas partições de treinamento e de validação. Caso seja usada uma divisão temporal, registros de períodos futuros não poderão participar do treinamento de modelos avaliados em períodos anteriores.

A imputação, a padronização, o cálculo dos pesos de classe e qualquer procedimento de reamostragem serão executados dentro de cada partição de treinamento. Essa organização evita que informações da validação ou do teste influenciem o ajuste.

### 6.1 Métricas de avaliação

A métrica principal da busca é a área sob a curva Precisão-Revocação (PR-AUC), calculada como precisão média (*Average Precision*) na média das partições de validação. A ROC-AUC também será registrada como métrica complementar.

A escolha da PR-AUC considera o desbalanceamento da variável-alvo. Como os registros positivos representam 4,65% da amostra na definição provisória, a avaliação precisa dar atenção especial à identificação dessa classe. Nessa situação, a ROC-AUC tende a parecer mais favorável do que o resultado prático, porque os falsos positivos se diluem entre os muitos registros negativos.

A PR-AUC mostra a relação entre precisão e revocação ao longo dos diferentes limiares de classificação. Em termos práticos, ajuda a avaliar quantos dos registros classificados com maior risco correspondem de fato a casos positivos e quantos dos casos positivos existentes foram identificados pelo modelo. Assim como a ROC-AUC, ela não depende de um limiar fixo.

A ROC-AUC será apresentada como complemento, mostrando a capacidade de ordenação dos registros positivos e negativos em diferentes limiares. Ela também permite situar os resultados em relação a trabalhos que usaram essa métrica, como o da UFRJ-Macaé.

As métricas serão interpretadas em conjunto, considerando a proporção de positivos na base e as características do protocolo de validação. Os resultados dos trabalhos relacionados servirão como referência bibliográfica, mas não como comparação direta de desempenho, pois as bases e os procedimentos experimentais são diferentes.

### 6.2 Definição do limiar de classificação

Após a seleção dos hiperparâmetros, será definido um limiar de classificação para cada modelo, usando as probabilidades obtidas por validação cruzada *out-of-fold* no conjunto de treinamento.

O limiar será escolhido pela maximização do F2, métrica que atribui peso maior à revocação do que à precisão. Essa escolha considera que, no contexto da pesquisa, é relevante identificar uma parcela maior dos registros associados à evasão, sem desconsiderar a quantidade de falsos positivos.

A mesma regra será aplicada aos quatro modelos. Isso é necessário porque cada modelo, com ou sem ponderação de classes, produz probabilidades em escalas diferentes. Um limiar fixo para todos compararia essas escalas, e não a qualidade dos modelos.

O limiar selecionado será mantido fixo na avaliação do conjunto de teste. O limiar convencional de 0,5 também será apresentado como análise de sensibilidade.

O conjunto de teste, definido na issue #27, será usado somente após a definição dos hiperparâmetros e do limiar, evitando que seus resultados influenciem as decisões tomadas durante o treinamento.

## 7. Interpretação dos resultados

Além das métricas de desempenho, a interpretação dos modelos é uma parte central da análise.

Na Regressão Logística, serão examinados os coeficientes e as razões de chance, considerando a padronização das variáveis numéricas e as categorias de referência das variáveis categóricas.

Na Árvore de Decisão, serão observadas as regras e condições usadas nas divisões. Essa representação poderá ajudar a mostrar combinações de características encontradas pelo modelo.

Na Random Forest e no XGBoost, a importância das variáveis por permutação (issue #39) e o SHAP (issue #40) serão usados para investigar quais características mais contribuíram para as classificações.

O SHAP permite observar a contribuição de cada variável para a saída do modelo, tanto de forma geral quanto em registros específicos. Essa contribuição, porém, representa o comportamento aprendido pelo modelo e não deve ser interpretada como explicação causal da evasão.

A interpretação também deverá considerar a correlação entre as variáveis. Quando diferentes indicadores representam aspectos semelhantes da trajetória acadêmica, sua importância pode ser compartilhada ou dividida entre eles. Por isso, os resultados serão discutidos em conjunto com a análise exploratória e com a fundamentação teórica do trabalho.

## 8. Verificação técnica dos espaços de busca

Antes da implementação definitiva dos experimentos, os espaços de hiperparâmetros foram executados com dados sintéticos, incluindo valores ausentes, poucos registros positivos e múltiplos registros do mesmo aluno.

O teste usou a validação agrupada por aluno prevista no projeto, calculou os pesos de classe exclusivamente na partição de treinamento e usou a PR-AUC como métrica.

As configurações foram executadas sem erros e sem avisos de parâmetros obsoletos nas versões das bibliotecas registradas na seção seguinte. Na Regressão Logística, algumas tentativas geraram avisos de convergência, que deverão ser acompanhados na implementação definitiva.

O código dessa verificação está no arquivo `verifica_espacos_hiperparametros.py`.

Essa etapa teve como objetivo verificar se os espaços definidos podem ser executados tecnicamente. Ela não representa uma avaliação de desempenho, pois usou dados sintéticos e não a base do INATEL.

## 9. Ambiente e versões das bibliotecas

As versões usadas na verificação técnica dos espaços de busca foram:

| Biblioteca | Versão |
|---|---|
| scikit-learn | 1.9.1 |
| XGBoost | 3.4.1 |
| Optuna | 5.0.0 |

Essas versões correspondem ao ambiente em que o teste técnico foi executado. As implementações definitivas dos modelos (issues #32 a #35) deverão registrar as versões efetivamente usadas, para permitir a reprodução dos experimentos. Caso sejam usadas versões diferentes, recomenda-se executar novamente o script de verificação.

## 10. Situação das decisões

A definição dos modelos e dos espaços iniciais de busca permite avançar para a implementação, mas parte das decisões ainda depende de outras etapas do projeto. Para deixar claro o estágio de cada uma, elas estão separadas em três grupos.

**Já definido**

- Os quatro modelos comparados: Regressão Logística, Árvore de Decisão, Random Forest e XGBoost.
- A PR-AUC como métrica principal da busca e da comparação, com a ROC-AUC como complemento (issue #29).
- A escolha do limiar pela maximização do F2 nas probabilidades *out-of-fold* do treinamento, com o limiar de 0,5 como sensibilidade (issue #29).
- O ajuste de qualquer transformação dependente dos dados apenas na partição de treinamento.
- A interpretação dos resultados como associação, e não como causa.

**Proposto neste documento**

- Os espaços de busca de cada modelo (seção 5).
- O uso do Optuna com amostrador TPE e o orçamento de tentativas (seção 6).
- O tratamento dos valores ausentes: imputação com indicador de ausência na Regressão Logística e tratamento nativo nos modelos de árvores.
- A importância por permutação e o SHAP como formas principais de interpretação da Random Forest e do XGBoost.

**Depende de outras issues**

- **#18 (variável-alvo):** a definição final e a janela sem retorno, que alteram a quantidade de positivos e negativos, a proporção entre as classes e o limite inferior de `min_samples_leaf`.
- **#26 (variáveis explicativas):** a seleção e o tratamento das variáveis, especialmente das correlacionadas, que afetam a leitura dos coeficientes da Regressão Logística.
- **#27 e #28 (separação e validação):** o conjunto de teste e o protocolo que respeita a estrutura longitudinal.
- **#54 (desbalanceamento):** se `class_weight` e `scale_pos_weight` serão ajustados na busca ou mantidos em valores neutros.
- **#31 (protocolo experimental):** o orçamento final da busca e a forma de apresentar a Árvore de Decisão no artigo.
- **#48 e #57 (revisão bibliográfica e fundamentação):** a correção das referências ao IFPB e à UFRJ-Macaé.

Após essas definições, os modelos poderão ser treinados e comparados com o mesmo protocolo experimental. Os resultados serão analisados considerando tanto as métricas de classificação quanto a possibilidade de interpretar os padrões identificados na base do INATEL.

## Referências

BARBOSA, D.; CABRAL, L.; DWAN, F.; FREITAS, E.; MELLO, R. F. Previsão da Evasão Escolar através da Análise de Dados e Aprendizagem de Máquina: um estudo de caso. In: Workshop de Aplicações Práticas de Learning Analytics em Instituições de Ensino no Brasil (WAPLA), 2023. Porto Alegre: SBC.

BETTAHI, A.; BELOUADHA, F.-Z.; HARROUD, H. A Modular and Explainable Machine Learning Pipeline for Student Dropout Prediction in Higher Education. *Algorithms*, v. 18, n. 10, 662, 2025. DOI: 10.3390/a18100662.

CHAGAS, P. A.; GOMIDE, J. S.; SANTANA, L. E. A. S. Previsão do risco de evasão universitária utilizando aprendizado de máquina: características e dinâmica da evasão nos cursos de Engenharia da UFRJ-Macaé. *Revista Brasileira de Informática na Educação*, v. 33, p. 1226-1247, 2025. DOI: 10.5753/rbie.2025.5196.

MARTINS, M. V.; TOLLEDO, D.; MACHADO, J.; BAPTISTA, L. M. T.; REALINHO, V. Early prediction of student's performance in higher education: a case study. In: *Trends and Applications in Information Systems and Technologies*, 2021.

OLIVEIRA, R. S.; MEDEIROS, F. P. A. Modelo de Predição de Evasão Escolar com Base em Dados de Autoavaliação de Cursos de Graduação. *Revista Brasileira de Informática na Educação*, v. 32, p. 1-21, 2024. DOI: 10.5753/rbie.2024.3542.

REALINHO, V.; MACHADO, J.; BAPTISTA, L.; MARTINS, M. V. Predicting Student Dropout and Academic Success. *Data*, v. 7, n. 11, 146, 2022. Base no UCI Machine Learning Repository: "Predict Students' Dropout and Academic Success". DOI: 10.24432/C5MC89.

VILLAR, A.; ANDRADE, C. R. V. Supervised machine learning algorithms for predicting student dropout and academic success: a comparative study. *Discover Artificial Intelligence*, v. 4, 2, 2024. DOI: 10.1007/s44163-023-00079-z.
