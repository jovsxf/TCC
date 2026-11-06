# Evidências de inconsistências e duplicidades na base v4

Auditoria direta executada em 06/11/2026 para a [issue #17](https://github.com/jovsxf/TCC/issues/17). Responsável: Vinícius. Revisão prevista: Giovana. Entrega proposta para revisão; a issue permanece aberta até a conferência da Giovana.

## Fonte e escopo

Base_academica_v4.csv, SHA-256 A37D9F2F12CB0A19DF1011BE6BA61D64E644A4C01717714DCD0B62C782DE3646. A fonte tem 59.059 linhas, 81 colunas e 7.615 alunos. Foram lidas 79 colunas, excluindo MATRICULA e DATANASCIMENTO. Identificadores internos foram usados somente em memória para agrupamento.

A legenda consultada é Legenda_base_v3.md, cujo título interno identifica a versão 2 de 24/10/2026. O nome do arquivo não confirma sozinho sua versão ou compatibilidade com a v4. A correção da frequência e a interpretação de transferência devem ser lidas com as atualizações posteriores do grupo.

O CSV foi lido diretamente do OneDrive. O hash foi conferido antes e depois, sem alteração. Nenhum dado individual ou base derivada foi salvo no repositório.

## Critérios da auditoria

Os [resultados agregados por verificação](auditoria_base_v4_resultados.json) acompanham este relatório. A execução foi de uma auditoria direta do CSV; não foi uma nova execução dos notebooks nem treinamento de modelos. As verificações estruturais abrangem toda a extração, sem excluir GAE, falecidos ou alunos com saída.

- A chave examinada foi HANDLEALUNO + ANOSEMESTRE + HANDLEALUNOCURRICULO. Repetições por aluno/semestre foram contadas antes de qualquer escolha de retrato, separando origem acadêmica e ocorrência.
- O recorte histórico usa desistência, abandono, cancelamento e desligamento. O recorte com cinco flags acrescenta transferência/afastamento. Trancamento e prazo esgotado não são gatilhos nessas contagens.
- O primeiro evento é o menor semestre com pelo menos um dos flags selecionados, considerando todos os vínculos. Para o retrato anterior, procura-se o último semestre com registro acadêmico estritamente anterior; múltiplas linhas nesse semestre são classificadas como ambíguas, sem desempate arbitrário. Retrato com lacuna é separado do semestre imediatamente anterior.
- A situação final considera todas as linhas no último semestre observado. Qualquer ausência ou categoria Desconhecido resulta em indefinido; sem essas ausências, várias categorias conhecidas resultam em conflito e uma única categoria em situação unívoca. A presença de situação acadêmica conhecida entre os indefinidos é examinada separadamente.
- Validade de domínio, flag/data e situação final são verificações da extração completa. Não demonstram que a informação já estava disponível em um momento anterior à saída; a disponibilidade temporal continua sendo tratada no relatório de temporalidade e na preparação da #20.

## Estrutura, preenchimento e domínio

| Verificação | Resultado | Tratamento |
| --- | --- | --- |
| Chave aluno/semestre/vínculo curricular | Zero ausências e zero duplicatas. | Preservar os registros. |
| Duplicatas integrais nas 79 colunas carregadas | Zero. | Nenhuma exclusão por duplicação integral. |
| Repetições aluno/semestre | 48.200 pares; 8.825 têm vários vínculos curriculares, 1.104 vários vínculos semestrais e 972 vários cursos. | Não confundir múltiplos vínculos com duplicatas nem contar cada linha como episódio independente. |
| Múltiplas linhas acadêmicas | 47 pares aluno/semestre. | Não escolher retrato por posição ou identificador. A consolidação dos indicadores precisa de regra explícita na [#20](https://github.com/jovsxf/TCC/issues/20). |
| Origem | 44.417 acadêmicas e 14.642 ocorrências. | Separar origens e seus denominadores. |
| Flags | 18 completos e binários: 15 TEVE* e IA09, IA12, IA13. | Não converter ausência ou valor inválido em zero em futuras versões; validade do domínio não comprova disponibilidade histórica. |
| Conversão numérica | Zero falhas em 20 variáveis verificadas; zero negativos e zero contagens fracionárias no conjunto de contagens auditado. | Preservar zeros explícitos e ausências. A escala formal do CRE continua dependendo de confirmação institucional. |
| Frequência | Dois valores acima de 100%; máximo 100,56. Uma frequência explicitamente zero. | Preservar a fonte. Manter os dois valores inválidos ausentes apenas na variável analítica, como na revisão; preservar o zero real. |
| Frequência ausente | 16.778 linhas: 14.642 ocorrências e 2.136 acadêmicas. | A ausência nas ocorrências é esperada. Na v4, a frequência também fica ausente sem turma ativa; não substituir por zero. |
| Aprovadas/reprovadas acima de matriculadas | Zero em 44.417 linhas acadêmicas avaliáveis para cada comparação. Ocorrências: zero linhas avaliáveis, pois os indicadores estão ausentes. | As antigas incompatibilidades foram corrigidas na extração v3 e permanecem corrigidas na v4. Não afirmar validação numérica de contagens nas ocorrências. |
| Datas | 26.615 datas preenchidas nas 18 colunas; zero falhas com formato explícito dia/mês/ano de dois dígitos e nenhuma hora. | Eventos no mesmo dia não têm ordem intradiária identificável. Datas administrativas não são o dia comprovado da interrupção. |
| Flag/data | Zero ocorrências de flag positivo sem data ou flag negativo com data nos 15 pares examinados. | Preservar os pares de origem. |
| Código/descrição da situação | Zero incompatibilidades após comparação normalizada de grafia. | Não alterar as categorias originais por suposição. |
| GAE | 27 linhas, 26 alunos. | Recorte fora da graduação regular, conforme alinhamento do grupo; não apagar da fonte. |
| Falecimento | 15 linhas correspondem a 14 alunos. | Não apresentar 15 linhas como 15 pessoas. Aplicação da exclusão pertence à regra de população da #18. |
| Período/mensalidade | 33 períodos zero; 14.479 períodos ausentes; 1.623 mensalidades ausentes. | Não interpretar ausência como zero. Não corrigir período zero sem definição institucional. |

As 20 variáveis numéricas examinadas foram CRENOSEMESTRE, CREATESEMESTRE, MEDIANAATESEMESTRE, VALORMENSALIDADE, IA04_01, IA04_02, IA10_01, IA12_01, IA75_01 a IA75_05, IA34_03, IA65_03, IA70_01, IA70_03, IA70_05, PERIODO e APROVEIT. Limites de 0–100 foram examinados nas variáveis percentuais e nos indicadores acadêmicos anteriormente tratados nessa escala; a ausência de extremos não estabelece a escala institucional do CRE.

## Os 15 conflitos citados na issue

O indicador histórico não detecta necessariamente conflito entre status e flags. Ele combina as situações de todos os vínculos e origens do último semestre de alunos sem evento de saída.

Os mesmos 15 alunos continuam marcados quando se usam os quatro flags históricos ou os cinco flags incluindo transferência. Nas 30 linhas finais desses alunos:

- há uma linha acadêmica e uma ocorrência por aluno;
- as 15 acadêmicas estão Ativo;
- as ocorrências estão Matrícula Pendente em 14 casos e Inativo em um;
- as situações distintas pertencem a vínculos curriculares diferentes.

Portanto, essas 15 marcações não demonstram 15 erros acadêmicos. O tratamento proposto é preservar as linhas e registrar a situação por origem, vínculo e período, sem exclusão global nem reclassificação automática como evasão. A validação anterior também não encontrou dois registros acadêmicos conflitantes dentro desse conjunto.

Separadamente, existe uma linha acadêmica e uma ocorrência com Ativo e evento de saída na própria linha. Elas requerem interpretação temporal; não foram corrigidas automaticamente.

## Atualização do recorte de eventos

A inclusão de transferência como saída muda a seleção, mesmo sem mudar o CSV. As duas versões abaixo são contagens de eventos observados e de disponibilidade do retrato, não quantidades de evadidos.

| Verificação | Quatro flags históricos | Cinco flags, incluindo transferência |
| --- | ---: | ---: |
| Alunos com evento observado | 3.507 | 3.798 |
| Sem registro acadêmico estritamente anterior ao primeiro evento | 1.627 | 1.631 |
| Último semestre acadêmico anterior ambíguo | 1 | 2 |
| Retrato único no semestre imediatamente anterior | 1.489 | 1.762 |
| Retrato único anterior com lacuna | 390 | 403 |
| Total reconciliado | 3.507 | 3.798 |

O último semestre estritamente anterior deve ser identificado antes de verificar unicidade. Não recuar para outro semestre quando o último é ambíguo. Para rotulagem por aluno, a presença de matrícula pode ser reunida entre vínculos; isso não define automaticamente como combinar CRE ou outros atributos.

## Situações indefinidas

| Último semestre dos alunos sem evento observado | Quatro flags | Cinco flags |
| --- | ---: | ---: |
| Indefinido/desconhecido ao combinar todas as linhas | 946 | 891 |
| Com linha acadêmica e situação conhecida | 876 | 870 |
| Acadêmicas Ativo | 857 | 856 |
| Acadêmicas Inativo | 17 | 12 |
| Acadêmicas Matrícula Pendente | 2 | 2 |
| Sem linha acadêmica com situação conhecida | 70 | 21 |

As situações indefinidas globais não equivalem a ausência de situação acadêmica em todos esses alunos. A mudança de 946 para 891 decorre do novo conjunto de eventos; não é correção de dados nem reclassificação automática.

## Pendências e revisão

1. Confirmar institucionalmente os dois valores de frequência acima de 100% e as interpretações ainda abertas na legenda, incluindo atividades complementares.
2. Definir a consolidação de indicadores entre currículos na [#20](https://github.com/jovsxf/TCC/issues/20), preservando os eventos e a distinção entre linhas acadêmicas e ocorrências.
3. Validar a rotulagem temporal na [#18](https://github.com/jovsxf/TCC/issues/18). As pendências já apontadas no [#68](https://github.com/jovsxf/TCC/pull/68) sobre diplomação anterior e continuidade em outro vínculo permanecem separadas desta auditoria estrutural.
4. Solicitar conferência da Giovana antes de encerrar a #17.

Esta entrega não altera os notebooks nem resolve as pendências de rotulagem do #68. A fonte não foi corrigida nem foram excluídos alunos nesta auditoria. Os tratamentos descritos são propostas analíticas e encaminhamentos, registrados separadamente dos valores originais.
