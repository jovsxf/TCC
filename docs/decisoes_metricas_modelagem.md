# Decisões de métricas para a etapa de modelagem

**Status:** decisões metodológicas registradas; proporção de positivos calculada com a definição provisória da #18; métricas de desempenho dependem do treinamento dos modelos e da revisão da definição do alvo.  
**Escopo:** comparação de modelos como instrumentos de análise. As métricas não validam um sistema de alerta para indivíduos.

## Métricas e justificativas

A classe positiva segue a regra provisória em `docs/definicao_variavel_alvo.md`: evasão da instituição sem retorno, com unidade aluno-semestre. Na base v4 (SHA-256 `A37D9F2F12CB0A19DF1011BE6BA61D64E644A4C01717714DCD0B62C782DE3646`), N = 2 produziu 1.840 linhas positivas e 38.664 negativas: **4,54% de positivos entre 40.504 linhas classificadas**. Esse resultado exclui falecidos e exclui provisoriamente GAE, mas mantém os estudantes com prazo esgotado; confirmar o recorte de GAE com o grupo/orientadora antes de tratá-lo como final. A sensibilidade N = 3 produziu 1.773 positivas, 38.919 negativas e 4,36% de positivos.

| Métrica | Uso e justificativa |
|---|---|
| **Recall (sensibilidade) — principal** | Mede a fração dos casos positivos identificados. O projeto considera especialmente custoso deixar casos de saída sem identificação; por isso, o Recall orientará a seleção de hiperparâmetros e a comparação principal entre modelos. A leitura deve sempre vir acompanhada de Precision e da matriz de confusão, pois maior Recall pode aumentar falsos positivos. |
| **Precision** | Entre as previsões positivas, mede a fração que é positiva. Complementa o Recall e torna visível o custo de produzir muitos falsos positivos, mesmo quando a prioridade é não perder casos. |
| **F1** | Média harmônica de Precision e Recall. Resume o equilíbrio entre as duas métricas, penalizando valores baixos em qualquer uma. Será métrica complementar, não critério principal, pois atribui peso equilibrado aos erros e não representa por si só a prioridade do projeto de reduzir falsos negativos. |
| **ROC-AUC** | Mede a capacidade de ordenar positivos acima de negativos ao longo dos limiares, sem fixar um limiar. Serve como comparação complementar de discriminação. Como a classe pode ser desbalanceada, ROC-AUC não substitui Recall, Precision nem a matriz de confusão no limiar adotado. |

Não se acrescenta outra métrica nesta decisão. Se o grupo incluir uma (por exemplo, PR-AUC), deverá registrar sua justificativa e interpretação antes da comparação final.

## Regra de seleção e cálculo

- **Critério primário de hiperparâmetros:** maximizar a média do Recall da classe positiva na validação cruzada, usando as mesmas partições e a mesma regra de alvo para todos os modelos. Os dados de teste final não participam da seleção.
- **Desempate:** comparar F1 médio e depois Precision média; mostrar também ROC-AUC. Registrar o método de validação, as partições/semente e a variabilidade entre folds para que a comparação seja reproduzível.
- **Limiar:** usar **0,5** para converter a probabilidade estimada em classe nas métricas Precision, Recall e F1 e nas matrizes de confusão (`probabilidade da classe positiva >= 0,5` implica previsão positiva). Este limiar fixo evita escolher um corte diferente para favorecer cada modelo. Qualquer análise posterior de outro limiar deve ser identificada como sensibilidade, sem substituir silenciosamente a comparação principal.
- **ROC-AUC:** calcular a partir dos escores/probabilidades contínuos da classe positiva, sem aplicar o limiar de 0,5.
- **Matrizes de confusão:** registrar para cada modelo avaliado, no conjunto de teste final e no limiar de 0,5, com linhas = classe observada e colunas = classe prevista; apresentar `TN`, `FP`, `FN` e `TP`, além das contagens por classe. Se houver uma matriz agregada de validação cruzada, explicar como foi agregada; não misturá-la com a matriz do teste final.

## Tabela de resultados a preencher após #18 e treinamento

| Modelo | Recall CV (média ± dispersão) | Precision teste | Recall teste | F1 teste | ROC-AUC teste | TN | FP | FN | TP |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A preencher | — | — | — | — | — | — | — | — | — |

Registrar junto à tabela: regra/horizonte adotados na #18; número de unidades e proporção positiva (N = 2: 40.504 unidades classificadas, 4,54% positivos, sob recorte provisório); estratégia de divisão/validação; semente; limiar 0,5; e diferenças de população entre treino, validação e teste.

## Limites de interpretação

Essas métricas comparam modelos agregadamente e apoiam a análise acadêmica. Não autorizam inferências individuais nem demonstram que um modelo esteja apto a emitir alertas ou orientar intervenções para estudantes.

## Pendências e revisão

1. Revisar com o grupo/orientadora a definição provisória e a exclusão de GAE; prazo esgotado permanece na amostra e não conta como saída.
2. Após aprovação, atualizar as issues #18, #29 e #54 com os resultados agregados. Se o recorte mudar, recalcular a proporção.
3. Treinar/avaliar os modelos e preencher a tabela e as matrizes de confusão.
4. Solicitar revisão do grupo/revisor e registrar a conferência desta decisão.


