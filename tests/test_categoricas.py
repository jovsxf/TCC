"""Verificações de vazamento e semântica, exclusivamente com dados sintéticos."""

import unittest

import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal
from sklearn.base import clone
from sklearn.exceptions import NotFittedError
from sklearn.pipeline import Pipeline

from scripts.preprocessing.categoricas import AUSENTE, NOVA, CodificadorCategoricas


class TestCategoricas(unittest.TestCase):
    def test_ausencia_nao_informado_e_categoria_nova_sao_distintos(self):
        training = pd.DataFrame({"IA70_02": ["Ensino Médio", "Não Informado"]})
        validation = pd.DataFrame({"IA70_02": [None, "Não Informado", "Novo", " "]})
        encoder = CodificadorCategoricas(("IA70_02",)).fit(training)
        names = encoder.get_feature_names_out().tolist()
        result = encoder.transform(validation).toarray()
        self.assertEqual(result[0, names.index("IA70_02_" + AUSENTE)], 1)
        self.assertEqual(result[1, names.index("IA70_02_Não Informado")], 1)
        self.assertEqual(result[2, names.index("IA70_02_" + NOVA)], 1)
        np.testing.assert_array_equal(result[0], result[3])
        np.testing.assert_array_equal(result.sum(axis=1), np.ones(4))

    def test_transform_nao_aprende_categorias_da_validacao(self):
        training = pd.DataFrame({"TURNO": ["Integral", "Noturno"]})
        validation = pd.DataFrame({"TURNO": ["Exclusivo da validação"]})
        encoder = CodificadorCategoricas(("TURNO",)).fit(training)
        before = encoder.get_feature_names_out().copy()
        encoder.transform(validation)
        np.testing.assert_array_equal(before, encoder.get_feature_names_out())
        self.assertNotIn("Exclusivo da validação", encoder.encoder_.categories_[0])
        self.assertEqual(encoder.resumo_cobertura(validation)["TURNO"]["categorias_novas"], 1)

    def test_coluna_inteira_ausente_no_ajuste(self):
        training = pd.DataFrame({"SEXO": [None, pd.NA]})
        validation = pd.DataFrame({"SEXO": ["M", None]})
        encoder = CodificadorCategoricas(("SEXO",)).fit(training)
        np.testing.assert_array_equal(encoder.transform(validation).toarray(), [[0, 1], [1, 0]])

    def test_pipeline_clone_e_preservacao_das_entradas(self):
        data = pd.DataFrame({"TURNO": [" Integral ", "Noturno"], "SEXO": ["M", None]})
        original = data.copy(deep=True)
        pipeline = Pipeline([("categoricas", CodificadorCategoricas(("TURNO", "SEXO")))])
        result = clone(pipeline).fit_transform(data)
        self.assertEqual(result.shape[0], 2)
        np.testing.assert_array_equal(np.asarray(result.sum(axis=1)).ravel(), [2, 2])
        assert_frame_equal(data, original)

    def test_zero_e_nao_sao_categorias_explicitas(self):
        data = pd.DataFrame({"IA09_02": ["0", "não", None]})
        encoder = CodificadorCategoricas(("IA09_02",)).fit(data)
        result = encoder.transform(data).toarray()
        self.assertFalse(np.array_equal(result[0], result[2]))
        self.assertFalse(np.array_equal(result[1], result[2]))

    def test_identificador_status_e_coluna_extra_sao_rejeitados(self):
        for column in ("HANDLEALUNO", "MATRICULA", "DATANASCIMENTO", "STATUSALUNO"):
            with self.subTest(column=column), self.assertRaises(ValueError):
                CodificadorCategoricas((column,)).fit(pd.DataFrame({column: ["x"]}))
        with self.assertRaises(ValueError):
            CodificadorCategoricas(("SEXO",)).fit(pd.DataFrame({"SEXO": ["M"], "HANDLEALUNO": [1]}))

    def test_sem_ajuste_e_marcador_reservado_sao_rejeitados(self):
        with self.assertRaises(NotFittedError):
            CodificadorCategoricas(("SEXO",)).transform(pd.DataFrame({"SEXO": ["M"]}))
        for marker in (AUSENTE, NOVA):
            with self.subTest(marker=marker), self.assertRaises(ValueError):
                CodificadorCategoricas(("SEXO",)).fit(pd.DataFrame({"SEXO": [marker]}))


if __name__ == "__main__":
    unittest.main()
