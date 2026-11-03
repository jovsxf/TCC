# TCC — análise exploratória de evasão no Inatel

## Arquivos

- `pre_defesa_analise_exploratoria.ipynb`: notebook original como referência histórica. Seus cálculos e resultados anteriores à revisão foram preservados; o caminho fixo do CSV foi substituído por configuração.
- `pre_defesa_analise_exploratoria_v2.ipynb`: revisão proposta da análise, com saída validada anteriormente, critérios explícitos e sensibilidades.
- `relatorio_alteracoes_v2.md`: auditoria por seção, resultados reconciliados, limitações e ajustes de publicação.
- `pre_defesa_analise_exploratoria_v2_base_v2_novas_colunas.ipynb`: v2 executada sobre a nova extração da base (com datas das ocorrências, correções e indicadores novos), com três células de análise a mais (59–61).
- `relatorio_alteracoes_base_v2.md`: o que mudou na base e no notebook, por que, o que foi analisado, os números que mudaram em relação à pré-defesa e as decisões pendentes.
- `pre_defesa_analise_exploratoria_v2_base_v3_legenda_v2.ipynb`: v2 executada sobre a base v3 (`Base_academica_v3.csv`), com os indicadores de disciplinas corrigidos e a legenda v2.
- `relatorio_correcoes_indicadores_disciplinas.md`: correções nos indicadores de disciplinas (aprovadas, matriculadas, reprovadas, grade e progresso), como chegamos nelas, a legenda v2 e o resultado na base v3.
- `.gitignore`: exclui dados brutos, ambientes, checkpoints, documentos e versões intermediárias.

Eventos de desistência, abandono, cancelamento e desligamento são **eventos de saída observados**; não equivalem necessariamente a evasão definitiva. O original é referência histórica e contém limitações examinadas na revisão.

## Dependências e execução

Python 3, pandas, NumPy, Matplotlib, SciPy, IPython e JupyterLab:

```powershell
python -m pip install pandas numpy matplotlib scipy ipython jupyterlab
```

Execute a partir da pasta do repositório. Configure o CSV externo (exemplo genérico):

```powershell
$env:TCC_CSV_PATH = "D:\dados_privados\Base_academica_v3.csv"
python -m jupyterlab
```

Abra o notebook e execute as células em ordem, em kernel limpo. Sem `TCC_CSV_PATH`, ambos procuram `dados_alunos.csv` no diretório de execução. As versões da base ficam na pasta compartilhada do grupo como `Base_academica_v2.csv`, `Base_academica_v3.csv` etc.; a v1 é o antigo `dados_alunos.csv`. O notebook v2 também lê a legenda e o original para verificar a integridade das fontes:

```powershell
$env:TCC_LEGENDA_PATH = "D:\dados_privados\Legenda.md"
$env:TCC_NOTEBOOK_ORIGINAL_PATH = Join-Path (Get-Location) "pre_defesa_analise_exploratoria.ipynb"
```

Por padrão, a legenda é `Legenda.md` junto ao CSV e o original é o arquivo publicado na pasta de execução. A legenda também fica fora do GitHub.

## Dados e saídas da publicação

O CSV fica fora do GitHub. Não inclua dados de alunos, credenciais ou documentos do OneDrive em commits. As cópias públicas preservam tabelas e gráficos agregados; quatro figuras do original com pontos individuais de outliers foram omitidas. Metadados de sessão foram removidos. O original local anterior à configuração e os arquivos do OneDrive foram preservados.

As saídas incorporadas vêm de execuções anteriores. A preparação desta publicação não executou novamente o notebook nem corrigiu seus cálculos históricos. Ao reexecutar o original, os pontos individuais dessas figuras podem reaparecer; retire essas saídas antes de publicar.

## Revisão proposta

A branch `revisao/analise-exploratoria-v2` propõe a v2 e seu relatório para revisão antes de merge na main. Corrige seleção temporal, comparabilidade, unidades e ausências, e acrescenta sensibilidades e verificações de retorno, conclusão e estabilidade. A cópia preserva o código analítico, tabelas agregadas e 23 gráficos da última versão consolidada executada. Dois logs de instalação com caminhos pessoais foram removidos. As saídas preservadas não representam uma nova execução nesta etapa de publicação.
