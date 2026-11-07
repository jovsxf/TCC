"""Confere se os espaços de hiperparâmetros propostos na #30 rodam nas
bibliotecas atuais. Usa dados sintéticos com valores faltantes, grupos por
aluno e validação agrupada, como prevê a #28. Não mede desempenho."""
import warnings, sys
import numpy as np, optuna, sklearn, xgboost
from sklearn.datasets import make_classification
from sklearn.base import clone
from sklearn.metrics import average_precision_score
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

warnings.simplefilter("error", FutureWarning)  # acusa parâmetro obsoleto
optuna.logging.set_verbosity(optuna.logging.WARNING)
rng = np.random.default_rng(0)
X, y = make_classification(2000, 12, n_informative=6, weights=[0.96], random_state=0)
X[rng.random(X.shape) < 0.1] = np.nan          # faltantes, como frequência e financeiro
grupos = rng.integers(0, 600, len(y))          # vários registros por "aluno"
cv = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)

def lr(t):
    l1 = t.suggest_float("l1_ratio", 0.0, 1.0)
    return make_pipeline(SimpleImputer(strategy="median", add_indicator=True), StandardScaler(),
        LogisticRegression(C=t.suggest_float("C", 1e-3, 1e2, log=True), l1_ratio=l1,
                           solver="saga", max_iter=5000,
                           class_weight=t.suggest_categorical("class_weight", [None, "balanced"])))

def dt(t):
    return DecisionTreeClassifier(random_state=42,
        criterion=t.suggest_categorical("criterion", ["gini", "entropy"]),
        max_depth=t.suggest_int("max_depth", 2, 10),
        min_samples_leaf=t.suggest_int("min_samples_leaf", 10, 200, log=True),
        min_samples_split=t.suggest_int("min_samples_split", 20, 400, log=True),
        ccp_alpha=t.suggest_float("ccp_alpha", 0.0, 0.01),
        class_weight=t.suggest_categorical("class_weight", [None, "balanced"]))

def rf(t):
    md = t.suggest_categorical("max_depth", [None, 4, 6, 8, 12, 16, 20])
    return RandomForestClassifier(random_state=42, n_jobs=-1, bootstrap=True,
        n_estimators=t.suggest_int("n_estimators", 200, 1000, step=100),
        max_depth=md,
        min_samples_leaf=t.suggest_int("min_samples_leaf", 1, 50, log=True),
        max_features=t.suggest_categorical("max_features", ["sqrt", "log2", 0.3, 0.5]),
        max_samples=t.suggest_float("max_samples", 0.5, 1.0),
        class_weight=t.suggest_categorical("class_weight", [None, "balanced", "balanced_subsample"]))

def xgb(t):
    return XGBClassifier(random_state=42, tree_method="hist", eval_metric="logloss", n_jobs=-1,
        n_estimators=t.suggest_int("n_estimators", 100, 1000, step=50),
        learning_rate=t.suggest_float("learning_rate", 0.01, 0.3, log=True),
        max_depth=t.suggest_int("max_depth", 2, 8),
        min_child_weight=t.suggest_float("min_child_weight", 1, 20, log=True),
        subsample=t.suggest_float("subsample", 0.6, 1.0),
        colsample_bytree=t.suggest_float("colsample_bytree", 0.5, 1.0),
        gamma=t.suggest_float("gamma", 0.0, 5.0),
        reg_lambda=t.suggest_float("reg_lambda", 1e-3, 10, log=True),
        reg_alpha=t.suggest_float("reg_alpha", 1e-3, 10, log=True),
        # "treino": negativos ÷ positivos, calculado na partição de treino de cada rodada
        scale_pos_weight=t.suggest_categorical("scale_pos_weight", ["neutro", "treino"]))

def validar(modelo):
    """Validação agrupada com PR-AUC; o peso da classe do XGBoost sai só do treino de cada rodada."""
    aucs = []
    for treino, teste in cv.split(X, y, grupos):
        m = clone(modelo)
        if isinstance(m, XGBClassifier):
            escolha = m.get_params()["scale_pos_weight"]
            razao = (y[treino] == 0).sum() / (y[treino] == 1).sum()
            m.set_params(scale_pos_weight=1.0 if escolha == "neutro" else float(razao))
        m.fit(X[treino], y[treino])
        aucs.append(average_precision_score(y[teste], m.predict_proba(X[teste])[:, 1]))
    return float(np.mean(aucs))


print("versões:", "sklearn", sklearn.__version__, "| xgboost", xgboost.__version__, "| optuna", optuna.__version__)
for nome, f in [("LR", lr), ("DT", dt), ("RF", rf), ("XGB", xgb)]:
    est = optuna.create_study(direction="maximize", sampler=optuna.samplers.TPESampler(seed=42))
    est.optimize(lambda t: validar(f(t)), n_trials=6, catch=())
    print(f"{nome}: {len(est.trials)} tentativas sem erro; parâmetros testados: {sorted(est.best_params)}")
