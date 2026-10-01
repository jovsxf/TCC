# TCC — análise exploratória de evasão no Inatel

## Arquivos

- `pre_defesa_analise_exploratoria.ipynb`: notebook original como referência histórica. Seus cálculos e resultados anteriores à revisão foram preservados; o caminho fixo do CSV foi substituído por configuração.
- `.gitignore`: exclui dados brutos, ambientes, checkpoints, documentos e versões intermediárias.

Eventos de desistência, abandono, cancelamento e desligamento são **eventos de saída observados**; não equivalem necessariamente a evasão definitiva. O original é referência histórica e contém limitações examinadas na revisão.

## Dependências e execução

Python 3, pandas, NumPy, Matplotlib, SciPy, IPython e JupyterLab:

```powershell
python -m pip install pandas numpy matplotlib scipy ipython jupyterlab
```

Execute a partir da pasta do repositório. Configure o CSV externo (exemplo genérico):

```powershell
$env:TCC_CSV_PATH = "D:\dados_privados\dados_alunos.csv"
python -m jupyterlab
```

Abra o notebook e execute as células em ordem, em kernel limpo. Sem `TCC_CSV_PATH`, o original procura `dados_alunos.csv` no diretório de execução.

## Dados e saídas da publicação

O CSV fica fora do GitHub. Não inclua dados de alunos, credenciais ou documentos do OneDrive em commits. As cópias públicas preservam tabelas e gráficos agregados; quatro figuras do original com pontos individuais de outliers foram omitidas. Metadados de sessão foram removidos. O original local anterior à configuração e os arquivos do OneDrive foram preservados.

As saídas incorporadas vêm de execuções anteriores. A preparação desta publicação não executou novamente o notebook nem corrigiu seus cálculos históricos. Ao reexecutar o original, os pontos individuais dessas figuras podem reaparecer; retire essas saídas antes de publicar.
