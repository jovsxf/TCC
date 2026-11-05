# Inventário e decisões da base acadêmica

**Inspeção direta:** 05/11/2026  
**Fonte usada na tarefa #18:** `Base_academica_v4.csv`, 59.059 linhas, 81 colunas, SHA-256 `A37D9F2F12CB0A19DF1011BE6BA61D64E644A4C01717714DCD0B62C782DE3646`. O CSV permanece fora do repositório.  
**Registros:** 44.417 linhas `ACADEMICA` e 14.642 linhas `OCORRENCIA`; 7.138 alunos com algum semestre acadêmico; 44.370 pares únicos aluno-semestre acadêmico; 47 pares aluno-semestre aparecem em mais de um currículo.

## Formato, tipos e chaves

- O arquivo é texto delimitado por ponto e vírgula, com campos entre aspas duplas. A leitura UTF-8 foi concluída sem erro. O recorte observado vai de `2009/1` a `2026/1`.
- CSV não carrega tipos nativos. Para preservar a forma original, o script de rotulagem lê os 79 campos autorizados como texto e converte explicitamente as flags usadas em 0/1; cria também um índice inteiro de semestre a partir de `ANOSEMESTRE`. `MATRICULA` e `DATANASCIMENTO` não são carregados.
- Não há valor ausente nas colunas da chave lógica verificadas. A chave `(HANDLEALUNO, ANOSEMESTRE, HANDLEALUNOCURRICULO)` não tem duplicatas na v4. A unidade lógica da base é aluno-semestre-currículo; na rotulagem da #18, currículos diferentes são consolidados em uma única unidade aluno-semestre.
- A unidade temporal é semestre letivo (`AAAA/1` ou `AAAA/2`). Campos `DATA*` representam datas de calendário; flags `TEVE*` representam ocorrências; códigos e indicadores acadêmicos precisam ser interpretados conforme domínio da legenda.
- A validação de UTF-8, delimitador, chave, semestre, origem e flags binárias foi feita diretamente na v4. As escalas de cada indicador (por exemplo, CRE, frequência, bolsas, valores financeiros e contagens) dependem da legenda v2. Como a legenda fica fora do repositório e não foi anexada nesta execução, a inspeção das unidades e dos domínios de cada indicador permanece limitada aos relatórios versionados.

## Colunas da v4 por grupo

A separação abaixo registra todos os 81 nomes da fonte. A classificação de tipo é lógica pelo papel/nome e pela documentação; fisicamente os campos são texto no CSV.

| Grupo lógico | Colunas |
|---|---|
| Identificadores internos e período (7) | `HANDLEANOSEMESTRE`, `ANOSEMESTRE`, `HANDLEALUNOANOSEMESTRE`, `HANDLEALUNO`, `HANDLEALUNOCURRICULO`, `HANDLECURRICULO`, `PERIODO` |
| Categorias e situação (8) | `SIGLACURSO`, `TURNO`, `SEXO`, `CODIGOSTATUSALUNO`, `STATUSALUNO`, `INGRESSO`, `APROVEIT`, `ORIGEMREGISTRO` |
| Flags de ocorrência (15) | `TEVEDESISTENCIA`, `TEVEABANDONO`, `TEVETRANCAMENTO`, `TEVECANCELAMENTO`, `TEVEDESLIGAMENTO`, `TEVETRANSAFASTAMENTO`, `TEVEDIPLOMACAO`, `TEVECONCLUSAOPROGRAMA`, `TEVEREINGRESSO`, `TEVEMUDANCACURSO`, `TEVEMIGRACAOCURRICULO`, `TEVEREMATRICULA`, `TEVEFALECIMENTO`, `TEVEPRAZOESGOTADO`, `TEVEAFASTAMENTOSEMOCORRENCIA` |
| Datas de eventos (18) | `DATADESISTENCIA`, `DATAABANDONO`, `DATATRANCAMENTO`, `DATACANCELAMENTO`, `DATADESLIGAMENTO`, `DATATRANSAFASTAMENTO`, `DATADIPLOMACAO`, `DATACONCLUSAOPROGRAMA`, `DATAREINGRESSO`, `DATAMUDANCACURSO`, `DATAMIGRACAOCURRICULO`, `DATAPRIMEIRASAIDA`, `DATAULTIMASAIDA`, `DATAINCLUSAOSAIDA`, `DATAREMATRICULA`, `DATAFALECIMENTO`, `DATAPRAZOESGOTADO`, `DATAAFASTAMENTOSEMOCORRENCIA` |
| Indicadores acadêmicos, financeiros e contagens (31) | `CRENOSEMESTRE`, `CREATESEMESTRE`, `MEDIANAATESEMESTRE`, `VALORMENSALIDADE`, `MATRICULAEFETIVADA`, `QUANTIDADEOCORRENCIAS`, `QTDOCORRENCIASSEMDATA`, `IA04_01`, `IA04_02`, `IA75_01`, `IA75_02`, `IA75_03`, `IA75_04`, `IA75_05`, `IA34_03`, `IA65_03`, `ATIVCOMPL_MATRICULADAS`, `ATIVCOMPL_APROVADAS`, `ATIVCOMPL_REPROVADAS`, `IA70_01`, `IA70_02`, `IA70_03`, `IA70_04`, `IA70_05`, `IA70_06`, `IA09`, `IA09_02`, `IA10_01`, `IA12`, `IA12_01`, `IA13` |
| Campos sensíveis fora do uso/reprodução (2) | `MATRICULA`, `DATANASCIMENTO` |

## Divergências entre legenda e CSV

1. A legenda antiga escrevia `TEVETRASAFASTAMENTO`; a v4 contém `TEVETRANSAFASTAMENTO`. Os relatórios da legenda v2 registram a correção. Usar o nome efetivamente presente na v4, sem renomear silenciosamente.
2. `GAE` aparece em `SIGLACURSO` e corresponde a Curso Aluno Especial segundo a legenda v2. A v4 registra 26 alunos nesse curso (24 aluno-semestres acadêmicos). A decisão provisória para a #18 é excluir a trajetória desses estudantes até validação do recorte.

## Decisões e tratamentos

| Campo/grupo | Uso/tratamento |
|---|---|
| Chave lógica (`HANDLEALUNO`, `ANOSEMESTRE`, `HANDLEALUNOCURRICULO`) | Usar somente para checagem e agrupamento interno; não publicar identificadores. Sem valores ausentes ou duplicatas nesta v4. |
| `ORIGEMREGISTRO` | Separar linhas acadêmicas e linhas só de ocorrência. A ausência de campos acadêmicos nas linhas `OCORRENCIA` não significa zero. |
| Eventos formais (`TEVEDESISTENCIA`, `TEVEABANDONO`, `TEVECANCELAMENTO`, `TEVEDESLIGAMENTO`) e datas | Definem a evidência de saída segundo a regra provisória da #18. Transferência/afastamento não entra isoladamente como evasão. |
| Indicadores acadêmicos (`IA*`, `ATIVCOMPL_*`, CRE, frequência) | Usar segundo unidades e domínios da legenda v2 e os relatórios de correção; manter vazios distintos de zero. |
| GAE | Excluir provisoriamente a trajetória completa de estudantes com esse curso até validação do recorte; quantificado em `docs/definicao_variavel_alvo.md`. |
| `TEVEPRAZOESGOTADO` | Não é evento de saída nem motivo de exclusão. O estudante segue a regra comum: exige evento formal e ausência de retorno na janela. |
| `MATRICULA`, `DATANASCIMENTO` | Não carregar, analisar nem reproduzir em notebook, saída, tabela, gráfico ou texto. Códigos internos também não devem ser divulgados. |

A legenda integral e a consulta de extração continuam fora do repositório. Os nomes da v4 foram conferidos diretamente; unidades e domínios campo a campo precisam ser confirmados com a legenda v2 antes de qualquer alteração de interpretação.

## Referências internas

- `docs/relatorio_correcoes_indicadores_disciplinas.md`, seções 7–9: legenda v2, GAE, privacidade e validações da v3.
- `docs/relatorio_temporalidade_campos.md`: disponibilidade temporal e prevenção de vazamento.
- `docs/definicao_variavel_alvo.md`: regra e contagens agregadas da #18 na base v4.
- `README.md`: configuração do CSV privado e execução dos notebooks/scripts.

