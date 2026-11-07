# Variáveis categóricas — proposta da #19

Preparação local em 06/11/2026. Responsável: Vinícius. Revisão prevista: Giovana. A implementação está disponível para revisão; a #19 não foi encerrada.

## Escopo

O código codifica somente os campos solicitados pelo chamador. O inventário abaixo não aprova todos esses campos como preditores: a seleção pertence à #26, a consolidação por aluno/semestre à #20 e a disponibilidade temporal à #51. A #15, dependência formal da #19, permanece aberta.

Não foram alterados os notebooks, os cálculos da EDA, os critérios de evasão ou os arquivos do OneDrive. Não há treinamento de modelos nem dataset final nesta entrega.

## Inventário confirmado na v4

Fonte: Base_academica_v4.csv, SHA-256 A37D9F2F12CB0A19DF1011BE6BA61D64E644A4C01717714DCD0B62C782DE3646. Os números foram conferidos diretamente no CSV e coincidem com a inspeção anterior da mesma fonte. São contagens de linhas, não de alunos.

| Campo | Categorias não vazias | Ausentes nas 59.059 linhas | Ausentes nas 44.417 acadêmicas |
| --- | ---: | ---: | ---: |
| SIGLACURSO | 12 | 0 | 0 |
| TURNO | 2 | 0 | 0 |
| SEXO | 2 | 20 | 13 |
| IA70_02 — escolaridade da mãe | 9 | 43.869 | 29.227 |
| IA70_04 — faixa de patrimônio | 6 | 43.869 | 29.227 |
| IA70_06 — escolaridade do pai | 9 | 43.869 | 29.227 |
| IA09_02 — motivo da desclassificação da bolsa | 28 | 55.812 | 41.170 |

IA09, IA12 e IA13 já são binários e não passam por esta transformação. STATUSALUNO, CODIGOSTATUSALUNO, datas, HANDLEs e demais campos fora do inventário são rejeitados como entradas deste codificador. INGRESSO é semestre de ingresso; não informa a forma de admissão.

## Tratamento implementado para revisão

- Indicadores por categoria, sem ordem numérica arbitrária para curso, escolaridade ou patrimônio. Não se agrupam categorias raras automaticamente.
- Remoção somente de espaços nas extremidades; não se alteram acentos, caixa ou categorias explícitas. Vazio, nulo e texto só com espaços recebem o marcador de ausência. Não Informado, Desconhecido, zero e não continuam categorias distintas se estiverem presentes.
- O vocabulário é aprendido em `fit`. Valores não vistos nesse ajuste recebem um marcador de categoria nova em `transform`, sem ampliar o vocabulário. Há marcadores distintos para ausência e categoria nova, mesmo quando não ocorrem no ajuste.
- São mantidos todos os indicadores (`drop=None`). A categoria de referência, regularização e uso nos modelos continuam sujeitos ao protocolo. Indicadores sem exemplos no ajuste não fornecem estimativas de efeito para categorias novas.
- Não há preenchimento entre semestres ou currículos. A transformação não verifica sozinha se um atributo estava disponível antes da saída; a #20 precisa fornecer observações elegíveis.

A classe é compatível com `Pipeline` e pode ser clonada para cada partição. O ajuste deve ocorrer dentro do treino de cada partição; este é o procedimento descrito na [documentação do scikit-learn sobre vazamento](https://scikit-learn.org/1.6/common_pitfalls.html#data-leakage). O [OneHotEncoder](https://scikit-learn.org/1.6/modules/generated/sklearn.preprocessing.OneHotEncoder.html) faz a expansão dos indicadores; os dois marcadores são regras explícitas desta proposta.

## Verificação executada

Os [resultados agregados](verificacao_categoricas_v4.json) vêm de execução real do verificador em 06/11/2026. Foram usadas as 59.059 linhas, inclusive ocorrências e GAE, exclusivamente para verificar o código. Nenhum rótulo de evasão foi carregado.

A separação técnica agrupa todas as linhas de cada aluno usando uma regra fixa de hash, independente dos atributos e de qualquer desfecho. Ela não escolhe nem substitui a divisão experimental da #27.

| Verificação | Resultado |
| --- | ---: |
| Conjunto de ajuste técnico | 46.896 linhas; 6.071 alunos |
| Conjunto de verificação técnica | 12.163 linhas; 1.544 alunos |
| Alunos nos dois conjuntos | 0 |
| Indicadores produzidos para os sete campos | 80 |
| Categorias novas na verificação | 2 linhas em IA09_02; zero nos outros campos |
| Vocabulário alterado por `transform` | Não |
| Valor não finito na matriz | Nenhum |

Os 80 indicadores dependem desse vocabulário técnico e não são o número definitivo de preditores. As matrizes ficaram apenas em memória. Não foram exportados valores individuais, identificadores, textos de motivos ou o codificador ajustado.

Sete testes com dados sintéticos passaram: distinção entre ausência/Não Informado/categoria nova, vocabulário limitado ao ajuste, coluna inteiramente ausente, integração com pipeline e clonagem, preservação das entradas, preservação de zero/não e rejeição de campos indevidos ou marcadores reservados.

## Arquivos e reprodução

- [Codificador](../scripts/preprocessing/categoricas.py).
- [Verificador com leitura externa e saída agregada](../scripts/analysis/verificar_categoricas.py).
- [Testes sintéticos](../tests/test_categoricas.py).

Ambiente verificado: Python 3.12.5, pandas 2.2.3, NumPy 2.2.6, SciPy 1.15.2 e scikit-learn 1.6.1. Nenhuma dependência foi instalada nesta etapa.

Executar da raiz da cópia de trabalho, usando um Python com essas dependências:

```powershell
python -B -m unittest discover -s tests -p "test_categoricas.py" -v
$env:TCC_CSV_PATH = "D:\dados_privados\Base_academica_v4.csv"
python -B -m scripts.analysis.verificar_categoricas --output verificacao_categoricas_local.json
```

O caminho do CSV vem de TCC_CSV_PATH ou `--csv`; não há pasta pessoal como padrão. O verificador exige um nome de saída ainda inexistente e salva somente JSON agregado. O CSV permanece fora do repositório. Não salvar matrizes individuais ou o objeto ajustado no Git.

## Pendências para concluir a #19

1. Conferir a #15 e aprovar os campos na #26. A presença no inventário não equivale a inclusão no modelo.
2. Fechar as regras de ausências e os significados financeiros nas #16 e #52. A codificação preserva a distinção, mas não resolve o significado institucional.
3. Integrar ao gerador da #20 e às partições das #27 e #28. Ainda não existe demonstração no dataset final, cuja população e rotulagem continuam pendentes.
4. Aprovação de Vinícius antes da publicação e revisão da Giovana no PR antes de encerrar a issue. Esta preparação não altera ou encerra outras issues.
