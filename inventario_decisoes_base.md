# Inventário e decisões da base acadêmica

**Data do registro:** 03/11/2026  
**Base de referência:** `Base_academica_v3.csv`, extração de 24/10/2026, identificada no relatório de correções pelo SHA-256 `9CCE803735488354B820F9B1976612AB9D1DE5950EDB91BE57F85C415D6A2343`.  
**Notebook de trabalho:** `pre_defesa_analise_exploratoria_v2_inventario_base.ipynb`, cópia de `pre_defesa_analise_exploratoria_v2.ipynb` feita em 03/11/2026. O notebook original e a alteração local pré-existente foram preservados.

## Escopo e limite da conferência

A cópia do CSV e da legenda v2 não está neste repositório; ambos permanecem na pasta compartilhada do grupo. Portanto, este inventário consolida os metadados e resultados documentados nas versões anteriores, mas **não afirma ter reaberto o CSV para uma inspeção direta de tipos, codificação de bytes ou unidades**. A verificação direta fica registrada como pendência antes de qualquer nova extração ou mudança de esquema. Não há evidência suficiente para declarar se o CSV está em UTF-8, Windows-1252 ou outra codificação, nem para enumerar o dtype inferido por biblioteca de cada coluna.

## Estrutura confirmada nos registros existentes

- A versão v3 tem **59.059 linhas e 81 colunas**, conforme relatório `relatorio_correcoes_indicadores_disciplinas.md`.
- A unidade lógica documentada é uma linha por **aluno, semestre e currículo**. Há registros de origem acadêmica e registros originados apenas de ocorrência (`ORIGEMREGISTRO`); campos acadêmicos podem ficar vazios nas linhas só de ocorrência. Vazio não deve ser convertido automaticamente em zero.
- A estrutura tem flags/eventos e datas de ocorrência, campos acadêmicos e indicadores `IA*`, além de variáveis cadastrais. A interpretação detalhada e as unidades declaradas devem ser consultadas na legenda v2, mantida junto à base.
- O relatório registra que não havia duplicidade para a chave lógica aluno-semestre-currículo na conferência da base v2. Essa propriedade não foi revalidada diretamente na v3 neste trabalho.
- O hash acima identifica a extração v3 usada nos resultados prévios; comparar o hash é necessário para confirmar que a fonte local é a mesma.

## Campos para as etapas seguintes

| Grupo | Campos/uso | Tratamento registrado |
|---|---|---|
| Chave lógica | aluno + semestre + currículo | Usar para checagens de unicidade e alinhamento. Não publicar matrícula ou identificadores internos. |
| Origem do registro | `ORIGEMREGISTRO` | Separar linhas acadêmicas e linhas só de ocorrência; não interpretar ausência de dado acadêmico nas últimas como zero. |
| Saída e trajetória | flags `TEVE*` e datas `DATA*` documentadas na legenda | Preservar a distinção entre evento ocorrido e data de inclusão; validar datas e categorias antes de transformar. |
| Acadêmicos | indicadores `IA*`, situação e curso | Usar conforme unidades e definições da legenda v2; tratar vazios, zeros e registros de ocorrência conforme os relatórios prévios. |
| Curso | sigla, incluindo `GAE` | Decisão abaixo: excluir GAE da coorte principal de graduação regular; conservar na fonte e reportar a exclusão. |
| Identificadores e atributo sensível | `MATRICULA`, `DATANASCIMENTO` | Não usar, reproduzir, exibir em saída, tabela, gráfico, texto ou chave publicada. |

Os nomes acima são os campos relevantes comprovados pela documentação disponível, não uma transcrição das 81 colunas. A lista integral, os tipos observados e unidades devem ser extraídos de uma cópia autorizada do CSV e reconciliados com a legenda antes de novo processamento.

## Divergências entre legenda e CSV

1. **Grafia de transferência/afastamento:** a legenda antiga registra `TEVETRASAFASTAMENTO`; o nome usado no CSV e nos relatórios da base v3 é `TEVETRANSAFASTAMENTO`. Adotar o nome efetivamente presente na base para operações, sem renomear silenciosamente a coluna; documentar a equivalência e corrigir a legenda na próxima revisão controlada.
2. **GAE:** ausente da legenda anterior. A legenda v2 passou a descrevê-la como **Curso Aluno Especial**. O relatório anterior identifica 26 alunos em GAE (a contagem de linhas varia por versão/recorte e foi citada como 27 linhas em um relatório antigo), portanto essa contagem deve ser recalculada na extração efetivamente usada.

## Decisão sobre GAE

**Decisão para esta análise:** excluir registros do curso GAE da coorte principal quando o universo for graduação regular, pois Curso Aluno Especial não é curso de graduação regular. Não apagar nem alterar esses registros na base; quantificar e registrar a exclusão e, se a comparação for relevante ao protocolo, apresentar análise de sensibilidade incluindo GAE separadamente. A decisão é de recorte analítico, não uma correção da fonte. Ela deve ser comunicada ao grupo por afetar tamanho da população e resultados de etapas seguintes.

## Campos que não serão usados nem reproduzidos

`MATRICULA` e `DATANASCIMENTO` ficam explicitamente fora do uso analítico e da reprodução em notebooks, saídas, tabelas, gráficos e texto. A legenda v2 também orienta a não divulgar códigos internos. A chave lógica é apenas conceitual no relatório; nenhum valor individual será registrado.

## Pendências para fechar a inspeção física

- Acessar a cópia controlada de `Base_academica_v3.csv` e `Legenda.md` no compartilhamento, conferir os nomes e a ordem de todas as 81 colunas, tipos observados, nulos, codificação e delimitador.
- Conferir unidade e domínio de cada campo na legenda v2, marcando explicitamente quais entram no protocolo e quais exigem parsing ou recodificação (especialmente datas, flags, categorias e campos numéricos com zeros/vazios).
- Revalidar unicidade da chave lógica, contagens por origem e a contagem de GAE na mesma versão/hash que alimentará as próximas etapas.
- Se a fonte ou regra mudar, atualizar este registro e avisar o grupo antes de comparar resultados com os relatórios v2/v3.

## Referências internas

- `relatorio_correcoes_indicadores_disciplinas.md`, seções 7–9: limitações, legenda v2 e validações da base v3.
- `relatorio_alteracoes_v2.md`, seção 21: pendência histórica de dicionário e temporalidade, já resolvida parcialmente pela legenda v2.
- `README.md`: localização externa do CSV e da legenda e configuração do notebook.
