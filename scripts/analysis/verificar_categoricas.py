"""Verificação técnica da #19; exporta somente um resumo agregado em JSON."""

import argparse
import hashlib
import importlib.metadata
import json
import os
import platform
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline

from scripts.preprocessing.categoricas import (
    AUSENTE, NOVA, CAMPOS_CANDIDATOS, CodificadorCategoricas
)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verificar(csv_path):
    source_hash = sha256(csv_path)
    columns = ["HANDLEALUNO", "ORIGEMREGISTRO", *CAMPOS_CANDIDATOS]
    data = pd.read_csv(
        csv_path,
        sep=";",
        encoding="utf-8",
        dtype="string",
        keep_default_na=False,
        usecols=columns,
    )
    if data.HANDLEALUNO.str.strip().eq("").any():
        raise ValueError("A verificação exige identificador interno preenchido.")

    # Separação usada apenas no teste do código, sem escolha de split experimental.
    students = data.HANDLEALUNO.unique()
    verification_students = {
        student for student in students
        if int(hashlib.sha256(("issue19-check-v1|" + student).encode()).hexdigest(), 16) % 5 == 0
    }
    is_verification = data.HANDLEALUNO.isin(verification_students)
    fit_data = data.loc[~is_verification, list(CAMPOS_CANDIDATOS)]
    check_data = data.loc[is_verification, list(CAMPOS_CANDIDATOS)]
    if fit_data.empty or check_data.empty:
        raise ValueError("A divisão técnica precisa ter alunos nos dois lados.")
    fit_students = set(data.loc[~is_verification, "HANDLEALUNO"])
    overlap = len(fit_students & verification_students)
    if overlap:
        raise AssertionError("Há alunos nos dois lados da verificação técnica.")

    pipeline = Pipeline([("categoricas", CodificadorCategoricas(CAMPOS_CANDIDATOS))])
    fit_matrix = pipeline.fit_transform(fit_data)
    encoder = pipeline.named_steps["categoricas"]
    before = tuple(tuple(values) for values in encoder.encoder_.categories_)
    check_matrix = pipeline.transform(check_data)
    if before != tuple(tuple(values) for values in encoder.encoder_.categories_):
        raise AssertionError("A transformação modificou o vocabulário aprendido.")
    for column, categories in zip(fit_data, encoder.encoder_.categories_):
        expected = set(fit_data[column].str.strip()) - {""}
        if set(categories) - {AUSENTE, NOVA} != expected:
            raise AssertionError("O vocabulário não corresponde apenas ao ajuste.")
    for matrix in (fit_matrix, check_matrix):
        if not np.isfinite(matrix.data).all():
            raise AssertionError("A matriz transformada contém valores não finitos.")
        if not np.all(np.asarray(matrix.sum(axis=1)).ravel() == len(CAMPOS_CANDIDATOS)):
            raise AssertionError("Uma linha não tem exatamente uma categoria por campo.")

    inventory = {}
    academic = data.ORIGEMREGISTRO.eq("ACADEMICA")
    for column in CAMPOS_CANDIDATOS:
        values = data[column].str.strip()
        missing = values.eq("")
        inventory[column] = {
            "categorias_observadas": int(values.loc[~missing].nunique()),
            "ausentes_total": int(missing.sum()),
            "ausentes_academicas": int((missing & academic).sum()),
        }

    if sha256(csv_path) != source_hash:
        raise AssertionError("A fonte mudou durante a verificação.")
    return {
        "executado_em_utc": datetime.now(timezone.utc).isoformat(),
        "csv_nome": csv_path.name,
        "csv_sha256": source_hash,
        "fonte_preservada": True,
        "escopo": "verificação técnica; não é dataset final nem split experimental",
        "linhas": len(data),
        "alunos": len(students),
        "linhas_academicas": int(academic.sum()),
        "ajuste_tecnico": {"linhas": len(fit_data), "alunos": len(fit_students)},
        "verificacao_tecnica": {
            "linhas": len(check_data),
            "alunos": len(verification_students),
        },
        "alunos_em_ambos": overlap,
        "regra_divisao_tecnica": "SHA-256(issue19-check-v1|HANDLEALUNO) módulo 5 igual a 0 vai à verificação; demais ao ajuste",
        "campos_verificados": list(CAMPOS_CANDIDATOS),
        "inventario": inventory,
        "colunas_transformadas": fit_matrix.shape[1],
        "categorias_por_campo_no_ajuste_sem_marcadores": {
            column: len(categories) - 2
            for column, categories in zip(CAMPOS_CANDIDATOS, encoder.encoder_.categories_)
        },
        "cobertura_verificacao": encoder.resumo_cobertura(check_data),
        "vocabulario_preservado_ao_transformar": True,
        "matrizes_e_vocabulario_exportados": False,
        "modelos_treinados": 0,
        "versoes": {
            "python": platform.python_version(),
            **{
                name: importlib.metadata.version(name)
                for name in ("pandas", "numpy", "scipy", "scikit-learn")
            },
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", default=os.environ.get("TCC_CSV_PATH"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not args.csv:
        parser.error("Configure TCC_CSV_PATH ou informe --csv.")
    csv_path = Path(args.csv).expanduser().resolve()
    output = args.output.resolve()
    if output.suffix.lower() != ".json" or output == csv_path:
        parser.error("A saída deve ser um JSON separado da fonte.")
    if output.exists():
        parser.error("A saída já existe; escolha outro nome para preservar a execução anterior.")
    result = verificar(csv_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    summary = {
        "linhas": result["linhas"],
        "alunos": result["alunos"],
        "colunas_transformadas": result["colunas_transformadas"],
        "alunos_em_ambos": result["alunos_em_ambos"],
        "modelos_treinados": 0,
    }
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
