"""Codificação nominal proposta na #19; não seleciona população ou preditores."""

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder
from sklearn.utils.validation import check_is_fitted


CAMPOS_CANDIDATOS = (
    "SIGLACURSO", "TURNO", "SEXO", "IA70_02", "IA70_04", "IA70_06", "IA09_02"
)
AUSENTE = "__TCC_AUSENTE__"
NOVA = "__TCC_CATEGORIA_NOVA__"


class CodificadorCategoricas(TransformerMixin, BaseEstimator):
    """One-hot com campos explícitos e vocabulário aprendido somente em fit.

    Vazio, categoria explícita e categoria não vista no ajuste são distintos.
    Não agrupa categorias raras, ordena escolaridades ou completa trajetórias.
    O chamador deve aplicar fit apenas ao treino de cada partição.
    """

    def __init__(self, columns):
        self.columns = columns

    def _normalizar(self, X):
        if isinstance(self.columns, str):
            raise ValueError("Informe uma sequência explícita de campos.")
        columns = tuple(self.columns)
        if not columns or len(set(columns)) != len(columns):
            raise ValueError("Os campos devem ser únicos e não vazios.")
        if any(column not in CAMPOS_CANDIDATOS for column in columns):
            raise ValueError("Há campo fora do inventário de categóricas da #19.")
        if not isinstance(X, pd.DataFrame) or X.columns.has_duplicates:
            raise ValueError("Use um DataFrame com nomes de coluna únicos.")
        if set(X.columns) != set(columns):
            raise ValueError("Forneça somente os campos categóricos selecionados.")

        frame = pd.DataFrame(index=X.index)
        for column in columns:
            values = X[column].astype("string").str.strip()
            if values.isin([AUSENTE, NOVA]).any():
                raise ValueError("Um campo contém marcador reservado da codificação.")
            frame[column] = values.mask(values.eq("")).fillna(AUSENTE)
        return frame

    def fit(self, X, y=None):
        frame = self._normalizar(X)
        if frame.empty:
            raise ValueError("O conjunto de ajuste precisa ter pelo menos uma linha.")

        categories = []
        for column in frame:
            observed = sorted(set(frame[column]) - {AUSENTE})
            categories.append(observed + [AUSENTE, NOVA])

        self.encoder_ = OneHotEncoder(
            categories=categories,
            handle_unknown="error",
            sparse_output=True,
            dtype=np.float64,
            drop=None,
        ).fit(frame)
        self.feature_names_in_ = np.asarray(frame.columns, dtype=object)
        self.n_features_in_ = frame.shape[1]
        self.n_features_out_ = sum(len(values) for values in categories)
        return self

    def transform(self, X):
        check_is_fitted(self, "encoder_")
        frame = self._normalizar(X)
        if list(frame.columns) != list(self.feature_names_in_):
            raise ValueError("Os campos diferem dos usados no ajuste.")
        if frame.empty:
            return csr_matrix((0, self.n_features_out_), dtype=np.float64)
        for column, categories in zip(frame, self.encoder_.categories_):
            frame[column] = frame[column].where(frame[column].isin(categories), NOVA)
        return self.encoder_.transform(frame)

    def get_feature_names_out(self, input_features=None):
        check_is_fitted(self, "encoder_")
        return self.encoder_.get_feature_names_out(input_features)

    def resumo_cobertura(self, X):
        """Retorna somente contagens; não devolve textos ou linhas individuais."""
        check_is_fitted(self, "encoder_")
        frame = self._normalizar(X)
        result = {}
        for column, categories in zip(frame, self.encoder_.categories_):
            missing = frame[column].eq(AUSENTE)
            new = ~missing & ~frame[column].isin(categories)
            result[column] = {
                "linhas": len(frame),
                "ausentes": int(missing.sum()),
                "categorias_novas": int(new.sum()),
                "categorias_conhecidas": int((~missing & ~new).sum()),
            }
        return result
