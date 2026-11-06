#!/usr/bin/env python3
"""Aggregate target-label counts without exporting student identifiers.

Set TCC_CSV_PATH to the private Base_academica_v4.csv, then run:
    python scripts/analysis/rotular_variavel_alvo.py
"""
from __future__ import annotations

import hashlib
import json
import os
import csv
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

CSV = Path(os.environ["TCC_CSV_PATH"])
EXIT_FLAGS = [
    "TEVEDESISTENCIA",
    "TEVEABANDONO",
    "TEVECANCELAMENTO",
    "TEVEDESLIGAMENTO",
    "TEVETRANSAFASTAMENTO",
]
FLAGS = [
    "TEVEDESISTENCIA",
    "TEVEABANDONO",
    "TEVETRANCAMENTO",
    "TEVECANCELAMENTO",
    "TEVEDESLIGAMENTO",
    "TEVETRANSAFASTAMENTO",
    "TEVEDIPLOMACAO",
    "TEVECONCLUSAOPROGRAMA",
    "TEVEREINGRESSO",
    "TEVEMUDANCACURSO",
    "TEVEMIGRACAOCURRICULO",
    "TEVEREMATRICULA",
    "TEVEFALECIMENTO",
    "TEVEPRAZOESGOTADO",
    "TEVEAFASTAMENTOSEMOCORRENCIA",
]
REQUIRED = {
    "ANOSEMESTRE",
    "HANDLEALUNO",
    "SIGLACURSO",
    "ORIGEMREGISTRO",
    *FLAGS,
}


def sem_number(value: str) -> int:
    year, term = value.split("/")
    return int(year) * 2 + int(term) - 1


def load_data() -> tuple[pd.DataFrame, dict[str, object]]:
    sha256 = hashlib.sha256()
    with CSV.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            sha256.update(block)

    with CSV.open("r", encoding="utf-8", newline="") as source:
        source_columns = len(next(csv.reader(source, delimiter=";")))

    df = pd.read_csv(
        CSV,
        sep=";",
        encoding="utf-8",
        dtype="string",
        usecols=lambda col: col not in {"MATRICULA", "DATANASCIMENTO"},
    )
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"Base sem colunas necessárias: {', '.join(sorted(missing))}")
    if df["HANDLEALUNO"].isna().any() or df["ANOSEMESTRE"].isna().any():
        raise ValueError("Há linhas sem identificador interno ou semestre; revisar a extração.")

    parsed = df["ANOSEMESTRE"].str.extract(r"^(\d{4})/([12])$")
    if parsed.isna().any(axis=None):
        raise ValueError("ANOSEMESTRE contém valores fora do padrão AAAA/1 ou AAAA/2.")
    df["SEM"] = (parsed[0].astype("int32") * 2 + parsed[1].astype("int32") - 1)

    for col in FLAGS:
        numeric = pd.to_numeric(df[col], errors="coerce")
        invalid = numeric.notna() & ~numeric.isin([0, 1])
        if invalid.any():
            raise ValueError(f"{col} contém valor diferente de 0/1.")
        df[col] = numeric.fillna(0).astype("int8")
    df["TEVE_SAIDA_FORMAL"] = df[EXIT_FLAGS].eq(1).any(axis=1)
    for col in ["DATAPRAZOESGOTADO", "DATADIPLOMACAO"]:
        df[f"{col}_PARSED"] = pd.to_datetime(
            df[col], errors="coerce", dayfirst=True, format="mixed"
        )

    source_info = {
        "arquivo": CSV.name,
        "sha256": sha256.hexdigest().upper(),
        "linhas_csv": int(len(df)),
        "colunas_fonte": source_columns,
        "colunas_carregadas_sem_matricula_ou_data_nascimento": source_columns - 2,
        "colunas_derivadas": int(len(df.columns) - (source_columns - 2)),
        "semestre_final": int(df["SEM"].max()),
        "semestre_final_label": f"{int(df['SEM'].max()) // 2}/{int(df['SEM'].max()) % 2 + 1}",
        "linhas_por_origem": {
            str(origin): int(count)
            for origin, count in df["ORIGEMREGISTRO"].value_counts(dropna=False).items()
        },
    }
    return df, source_info


def build_indexes(df: pd.DataFrame) -> dict[str, object]:
    academic_source = df.loc[
        df["ORIGEMREGISTRO"].eq("ACADEMICA"), ["HANDLEALUNO", "SEM"]
    ].drop_duplicates()
    raw_terms_by_student = {
        student: np.sort(group["SEM"].unique().astype(int))
        for student, group in academic_source.groupby("HANDLEALUNO", sort=False)
    }
    trancamento_source = df.loc[
        df["TEVETRANCAMENTO"].eq(1) & df["ORIGEMREGISTRO"].eq("ACADEMICA"),
        ["HANDLEALUNO", "SEM"],
    ].drop_duplicates()
    trancamento_by_student = {
        student: set(group["SEM"].astype(int))
        for student, group in trancamento_source.groupby("HANDLEALUNO", sort=False)
    }
    trancamento_pairs = set(
        map(tuple, trancamento_source[["HANDLEALUNO", "SEM"]].itertuples(index=False, name=None))
    )
    academic = academic_source.loc[
        ~academic_source[["HANDLEALUNO", "SEM"]]
        .apply(tuple, axis=1)
        .isin(trancamento_pairs)
    ].copy()
    terms_by_student = {
        student: np.sort(group["SEM"].unique().astype(int))
        for student, group in academic.groupby("HANDLEALUNO", sort=False)
    }
    academic_students_before_trancamento = int(academic_source["HANDLEALUNO"].nunique())

    exits = df.loc[df[EXIT_FLAGS].eq(1).any(axis=1), ["HANDLEALUNO", "SEM"]]
    exits_by_student = {
        student: np.sort(group["SEM"].unique().astype(int))
        for student, group in exits.groupby("HANDLEALUNO", sort=False)
    }
    historical_exits = df.loc[df[EXIT_FLAGS[:-1]].eq(1).any(axis=1), ["HANDLEALUNO", "SEM"]]
    historical_exits_by_student = {
        student: np.sort(group["SEM"].unique().astype(int))
        for student, group in historical_exits.groupby("HANDLEALUNO", sort=False)
    }

    return {
        "terms": terms_by_student,
        "terms_before_trancamento": raw_terms_by_student,
        "trancamento": trancamento_by_student,
        "exits": exits_by_student,
        "historical_exits": historical_exits_by_student,
        "deceased": set(df.loc[df["TEVEFALECIMENTO"].eq(1), "HANDLEALUNO"]),
        "graduates": set(df.loc[df["TEVEDIPLOMACAO"].eq(1), "HANDLEALUNO"]),
        "gae": set(df.loc[df["SIGLACURSO"].eq("GAE"), "HANDLEALUNO"]),
        "deadline": set(df.loc[df["TEVEPRAZOESGOTADO"].eq(1), "HANDLEALUNO"]),
        "deadline_sem_by_student": {
            student: int(group["SEM"].min())
            for student, group in df.loc[df["TEVEPRAZOESGOTADO"].eq(1)]
            .groupby("HANDLEALUNO", sort=False)
        },
        "deadline_date_by_student": {
            student: group["DATAPRAZOESGOTADO_PARSED"].min()
            for student, group in df.loc[df["TEVEPRAZOESGOTADO"].eq(1)]
            .groupby("HANDLEALUNO", sort=False)
        },
        "graduate_date_by_student": {
            student: group["DATADIPLOMACAO_PARSED"].min()
            for student, group in df.loc[df["TEVEDIPLOMACAO"].eq(1)]
            .groupby("HANDLEALUNO", sort=False)
        },
        "graduate_sem_by_student": {
            student: np.sort(group["SEM"].unique().astype(int))
            for student, group in df.loc[df["TEVEDIPLOMACAO"].eq(1)]
            .groupby("HANDLEALUNO", sort=False)
        },
        "formal_exit_sem_by_student": {
            student: np.sort(group["SEM"].unique().astype(int))
            for student, group in df.loc[df["TEVE_SAIDA_FORMAL"]]
            .groupby("HANDLEALUNO", sort=False)
        },
        "academic_rows": int(len(academic)),
        "academic_rows_before_trancamento": int(len(academic_source)),
        "academic_semesters_flagged_trancamento": int(len(trancamento_source)),
        "academic_students_before_trancamento": academic_students_before_trancamento,
        "academic_source_rows": int(df["ORIGEMREGISTRO"].eq("ACADEMICA").sum()),
        "multiple_curriculum_student_semesters": int(
            df.loc[df["ORIGEMREGISTRO"].eq("ACADEMICA")]
            .groupby(["HANDLEALUNO", "SEM"])["HANDLEALUNOCURRICULO"]
            .nunique()
            .gt(1)
            .sum()
        ) if "HANDLEALUNOCURRICULO" in df.columns else None,
    }


def summarize_n(
    indexes: dict[str, object],
    last_semester: int,
    n: int,
    *,
    exclude_special: bool,
    window_start: str = "ultimo_semestre_cursado",
) -> dict[str, object]:
    if window_start not in {"ultimo_semestre_cursado", "semestre_evento"}:
        raise ValueError("window_start deve ser 'ultimo_semestre_cursado' ou 'semestre_evento'.")
    terms_by_student = indexes["terms"]
    exits_by_student = indexes["exits"]
    deceased = indexes["deceased"]
    graduates = indexes["graduates"]
    gae = indexes["gae"]
    trancamento = indexes["trancamento"]

    counts: Counter[str] = Counter()
    positive_students: set[str] = set()
    evaded_students: set[str] = set()
    no_prior_usable_students: set[str] = set()
    gap_distribution: Counter[int] = Counter()

    all_students = set(terms_by_student) | set(trancamento)
    for student in all_students:
        terms = terms_by_student.get(student, np.array([], dtype=int))
        # Death and GAE cases are provisionally excluded at student level.
        # TEVEPRAZOESGOTADO is descriptive status, not an exit or exclusion.
        if student in deceased:
            counts["excluidas_falecimento"] += len(terms) + len(trancamento.get(student, set()))
            continue
        if exclude_special and student in gae:
            counts["excluidas_GAE"] += len(terms) + len(trancamento.get(student, set()))
            continue
        counts["excluidas_trancamento"] += len(trancamento.get(student, set()))
        student_exit_sems = set(map(int, exits_by_student.get(student, [])))
        # Always remove a semester containing a formal exit, including episodes
        # followed by a return; the exit semester may contain incomplete data.
        decision: dict[str, int | str] | None = None
        for exit_sem in exits_by_student.get(student, []):
            before_or_same = terms[terms <= exit_sem]
            if not len(before_or_same):
                continue
            last_course_sem = int(before_or_same[-1])
            anchor = last_course_sem if window_start == "ultimo_semestre_cursado" else int(exit_sem)
            returned = bool(((terms > anchor) & (terms <= anchor + n)).any())
            if returned:
                continue

            usable_before_exit = terms[(terms < exit_sem) & ~np.isin(terms, list(student_exit_sems))]
            positive_sem = int(usable_before_exit[-1]) if len(usable_before_exit) else None
            if anchor + n <= last_semester:
                decision = {
                    "kind": "confirmed",
                    "exit_sem": int(exit_sem),
                    "last_course_sem": last_course_sem,
                    "positive_sem": positive_sem,
                }
            else:
                decision = {
                    "kind": "incomplete",
                    "exit_sem": int(exit_sem),
                    "last_course_sem": last_course_sem,
                    "positive_sem": positive_sem,
                }
            break

        considered_exit_sems = (
            [exit_sem for exit_sem in student_exit_sems if exit_sem < int(decision["exit_sem"])]
            if decision
            else list(student_exit_sems)
        )
        returned_exit_sems = {
            exit_sem
            for exit_sem in considered_exit_sems
            if bool(((terms > exit_sem) & (terms <= exit_sem + n)).any())
            and bool((terms == exit_sem).any())
        }
        counts["semestres_saida_com_retorno"] += len(returned_exit_sems)

        if decision and decision["kind"] in {"confirmed", "incomplete"}:
            exit_sem = int(decision["exit_sem"])
            positive_sem = decision["positive_sem"]
            confirmed = decision["kind"] == "confirmed"
            if confirmed:
                evaded_students.add(student)
                if positive_sem is None:
                    no_prior_usable_students.add(student)

            for term in terms:
                term = int(term)
                if term > exit_sem:
                    counts["excluidas_apos_primeiro_episodio"] += int((terms > exit_sem).sum())
                    break
                if term in student_exit_sems:
                    counts["excluidas_semestre_da_saida"] += 1
                    continue
                elif positive_sem is not None and term == positive_sem:
                    if confirmed:
                        counts["positivas"] += 1
                        positive_students.add(student)
                        gap_distribution[exit_sem - term] += 1
                    else:
                        counts["excluidas_saida_sem_janela_completa"] += 1
                else:
                    counts["negativas"] += 1
            continue

        # Without a qualifying formal exit, prior semesters are known negatives.
        # The last one is negative after diplomation, otherwise unresolved or
        # excluded for lack of a formal exit according to the current rule.
        for index, term in enumerate(terms):
            term = int(term)
            if term in student_exit_sems:
                counts["excluidas_semestre_da_saida"] += 1
            elif index < len(terms) - 1 or student in graduates:
                counts["negativas"] += 1
            elif term + n > last_semester:
                counts["excluidas_ainda_sem_desfecho"] += 1
            else:
                counts["excluidas_sem_evento_formal"] += 1

    positives = int(counts["positivas"])
    negatives = int(counts["negativas"])
    total = positives + negatives
    excluded = int(sum(v for k, v in counts.items() if k.startswith("excluidas_")))
    return {
        "N": n,
        "inicio_da_janela": window_start,
        "unidades_aluno_semestre_classificadas_ou_excluidas": total + excluded,
        "linhas_positivas": positives,
        "linhas_negativas": negatives,
        "linhas_excluidas": excluded,
        "proporcao_positiva_pct": round(100 * positives / total, 4) if total else None,
        "alunos_com_linha_positiva": len(positive_students),
        "alunos_evadidos_confirmados": len(evaded_students),
        "evadidos_sem_semestre_anterior_utilizavel": len(no_prior_usable_students),
        "semestres_de_saida_com_retorno_excluidos": int(
            counts.get("semestres_saida_com_retorno", 0)
        ),
        "distancia_semestre_positivo_ate_saida_formal": {
            str(gap): int(value) for gap, value in sorted(gap_distribution.items())
        },
        "exclusoes_por_motivo": {
            key.removeprefix("excluidas_"): int(value)
            for key, value in sorted(counts.items())
            if key.startswith("excluidas_")
        },
    }


def legacy_reference_n2(indexes: dict[str, object], last_semester: int) -> dict[str, object]:
    """Reproduce guide's old event-semester window for source cross-check only."""
    terms_by_student = indexes["terms_before_trancamento"]
    exits_by_student = indexes["historical_exits"]
    deceased = indexes["deceased"]
    graduates = indexes["graduates"]
    counts: Counter[str] = Counter()
    positive_students: set[str] = set()
    no_prior_usable_students: set[str] = set()

    for student, terms in terms_by_student.items():
        if student in deceased:
            continue
        outcome: tuple[str, int] | None = None
        for exit_sem in exits_by_student.get(student, []):
            returned = bool(((terms > exit_sem) & (terms <= exit_sem + 2)).any())
            if not returned:
                outcome = (
                    "confirmed" if exit_sem + 2 <= last_semester else "incomplete",
                    int(exit_sem),
                )
                break

        kind, end_sem = outcome if outcome else ("none", -1)
        prior = terms[terms < end_sem] if kind != "none" else terms
        if kind == "confirmed" and not len(prior):
            no_prior_usable_students.add(student)

        for term in terms:
            term = int(term)
            if kind != "none" and term >= end_sem:
                if term == end_sem:
                    counts["excluidas_semestre_da_saida"] += 1
                break
            last_before = len(prior) > 0 and term == int(prior[-1])
            if kind == "confirmed" and last_before:
                counts["positivas"] += 1
                positive_students.add(student)
            elif kind == "incomplete" and last_before:
                counts["excluidas_saida_sem_janela_completa"] += 1
            elif (terms > term).any() or student in graduates:
                counts["negativas"] += 1
            elif term + 2 > last_semester:
                counts["excluidas_ainda_sem_desfecho"] += 1
            else:
                counts["excluidas_sem_evento_formal"] += 1

    positives = int(counts["positivas"])
    negatives = int(counts["negativas"])
    excluded = int(sum(counts.values()) - positives - negatives)
    return {
        "N": 2,
        "inicio_da_janela": "semestre_evento (referencia antiga)",
        "linhas_positivas": positives,
        "linhas_negativas": negatives,
        "linhas_excluidas": excluded,
        "proporcao_positiva_pct": round(100 * positives / (positives + negatives), 4),
        "alunos_com_linha_positiva": len(positive_students),
        "evadidos_sem_semestre_anterior_utilizavel": len(no_prior_usable_students),
        "exclusoes_por_motivo": dict(sorted(counts.items())),
    }


def return_curve(
    indexes: dict[str, object], last_semester: int, *, window_start: str = "semestre_evento"
) -> list[dict[str, object]]:
    """Return curve measured from either the formal exit or last course semester."""
    terms_by_student = indexes["terms"]
    exits_by_student = indexes["exits"]
    excluded = indexes["deceased"] | indexes["gae"]
    cohort: list[tuple[int, int | None]] = []

    for student, exits in exits_by_student.items():
        if student in excluded:
            continue
        terms = terms_by_student.get(student)
        if terms is None:
            continue
        prior = terms[terms <= int(exits[0])]
        if not len(prior):
            continue
        last_course = int(prior[-1])
        anchor = int(exits[0]) if window_start == "semestre_evento" else last_course
        later = terms[terms > anchor]
        delay = int(later[0] - anchor) if len(later) else None
        cohort.append((last_semester - anchor, delay))

    curve: list[dict[str, object]] = []
    for k in range(1, 11):
        observed = [(delay, coverage) for coverage, delay in cohort if coverage >= k]
        returned = sum(delay is not None and delay <= k for delay, _ in observed)
        exact = sum(delay == k for delay, _ in observed)
        curve.append(
            {
                "k": k,
                "alunos_observaveis": len(observed),
                "voltaram_ate_k_pct": round(100 * returned / len(observed), 2)
                if observed
                else None,
                "voltaram_exatamente_em_k_pct": round(100 * exact / len(observed), 2)
                if observed
                else None,
            }
        )
    return curve


def main() -> None:
    df, source_info = load_data()
    indexes = build_indexes(df)
    last_semester = int(source_info["semestre_final"])

    results = [
        summarize_n(indexes, last_semester, 4, exclude_special=True, window_start="semestre_evento"),
        summarize_n(indexes, last_semester, 2, exclude_special=True, window_start="semestre_evento"),
    ]
    course_clock_n4 = summarize_n(
        indexes, last_semester, 4, exclude_special=True, window_start="ultimo_semestre_cursado"
    )
    legacy_n2 = legacy_reference_n2(indexes, last_semester)

    special = {
        "alunos_com_semestre_academico_antes_de_remover_trancamentos": indexes[
            "academic_students_before_trancamento"
        ],
        "alunos_com_semestre_academico": len(indexes["terms"]),
        "alunos_falecidos": len(indexes["deceased"]),
        "alunos_GAE": len(indexes["gae"]),
        "alunos_com_prazo_esgotado": len(indexes["deadline"]),
        "alunos_GAE_e_prazo_esgotado": len(indexes["gae"] & indexes["deadline"]),
        "alunos_falecidos_e_GAE": len(indexes["deceased"] & indexes["gae"]),
        "alunos_falecidos_e_prazo_esgotado": len(indexes["deceased"] & indexes["deadline"]),
        "alunos_com_exclusao_provisoria_falecimento_ou_GAE": len(
            indexes["deceased"] | indexes["gae"]
        ),
        "alunos_com_semestre_academico_apos_exclusoes_falecimento_GAE": len(
            set(indexes["terms"])
            - indexes["deceased"]
            - indexes["gae"]
        ),
        "linhas_fonte_academica": indexes["academic_source_rows"],
        "aluno_semestres_academicos_unicos": indexes["academic_rows"],
        "aluno_semestres_academicos_antes_de_remover_trancamentos": indexes[
            "academic_rows_before_trancamento"
        ],
        "aluno_semestres_academicos_com_flag_trancamento": indexes[
            "academic_semesters_flagged_trancamento"
        ],
        "aluno_semestres_academicos_apos_remover_trancamentos": indexes["academic_rows"],
        "aluno_semestres_com_multiplos_curriculos": indexes[
            "multiple_curriculum_student_semesters"
        ],
    }

    deadline_students = indexes["deadline"]
    returned_within_2 = {
        student
        for student in deadline_students
        if any(
            term > indexes["deadline_sem_by_student"][student]
            and term <= indexes["deadline_sem_by_student"][student] + 2
            for term in indexes["terms"].get(student, [])
        )
    }
    graduated_after = {
        student
        for student in deadline_students
        if any(
            term > indexes["deadline_sem_by_student"][student]
            for term in indexes["graduate_sem_by_student"].get(student, [])
        )
    }
    graduated_same_or_after = {
        student
        for student in deadline_students
        if any(
            term >= indexes["deadline_sem_by_student"][student]
            for term in indexes["graduate_sem_by_student"].get(student, [])
        )
    }
    graduation_dates_available = {
        student
        for student in deadline_students
        if pd.notna(indexes["deadline_date_by_student"].get(student))
        and pd.notna(indexes["graduate_date_by_student"].get(student))
    }
    graduated_after_deadline_date = {
        student
        for student in graduation_dates_available
        if indexes["graduate_date_by_student"][student]
        > indexes["deadline_date_by_student"][student]
    }
    graduated_same_deadline_date = {
        student
        for student in graduation_dates_available
        if indexes["graduate_date_by_student"][student]
        == indexes["deadline_date_by_student"][student]
    }
    formal_exit_same_or_after = {
        student
        for student in deadline_students
        if any(
            term >= indexes["deadline_sem_by_student"][student]
            for term in indexes["formal_exit_sem_by_student"].get(student, [])
        )
    }
    deadline_followup = {
        "alunos_com_prazo_esgotado": len(deadline_students),
        "voltaram_a_cursar_em_ate_2_semestres_apos_flag": len(returned_within_2),
        "diplomaram_no_mesmo_semestre_ou_depois_do_flag": len(graduated_same_or_after),
        "diplomaram_em_semestre_posterior_ao_flag": len(graduated_after),
        "diplomaram_com_data_posterior_a_data_do_prazo": len(graduated_after_deadline_date),
        "ambas_as_datas_disponiveis": len(graduation_dates_available),
        "datas_de_diploma_e_prazo_iguais": len(graduated_same_deadline_date),
        "tiveram_saida_formal_no_mesmo_semestre_ou_depois": len(formal_exit_same_or_after),
        "sobreposicao_retorno_e_saida_formal": len(returned_within_2 & formal_exit_same_or_after),
        "sobreposicao_retorno_e_diplomacao": len(returned_within_2 & graduated_after),
        "sobreposicao_diplomacao_e_saida_formal": len(graduated_after & formal_exit_same_or_after),
    }

    print(
        json.dumps(
            {
                "fonte": source_info,
                "populacao": special,
                "seguimento_prazo_esgotado": deadline_followup,
                "resultados_regra_corrigida": results,
                "curva_retorno_ancorada_no_semestre_da_saida": return_curve(
                    indexes, last_semester
                ),
                "sensibilidade_N4_janela_iniciada_no_ultimo_semestre_cursado": course_clock_n4,
                "referencia_guia_N2_codigo_antigo": legacy_n2,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
