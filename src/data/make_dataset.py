from pathlib import Path

import pandas as pd


RUTA_RAW = Path("data/raw")
RUTA_PROCESSED = Path("data/processed")


def main():
    procesos = pd.read_csv(RUTA_RAW / "main.csv")
    adjudicaciones = pd.read_csv(RUTA_RAW / "awards.csv")

    # Cantidad de renglones por proceso
    filas_por_proceso = procesos["tender_id"].value_counts()

    # Validación de estados
    estados_distintos = procesos[
        ["tender_id", "tender_status"]
    ].drop_duplicates()

    cantidad_estados = estados_distintos[
        "tender_id"
    ].value_counts()

    procesos_inconsistentes = (
        cantidad_estados > 1
    ).sum()

    if procesos_inconsistentes > 0:
        raise ValueError(
            "Existen procesos con más de un estado."
        )

    estados_por_proceso = estados_distintos.copy()

    # Vinculación entre adjudicaciones y procesos
    adjudicaciones_con_id = adjudicaciones[
        ["_link_main"]
    ].merge(
        procesos[
            ["_link", "tender_id"]
        ].drop_duplicates(subset="_link"),
        left_on="_link_main",
        right_on="_link",
        how="left"
    )

    sin_vincular = (
        adjudicaciones_con_id["tender_id"]
        .isna()
        .sum()
    )

    print("Adjudicaciones sin vincular:", sin_vincular)

    ids_adjudicados = adjudicaciones_con_id[
        ["tender_id"]
    ].dropna().drop_duplicates()

    ids_adjudicados["adjudicada"] = 1

    datos_procesos = estados_por_proceso.merge(
        ids_adjudicados,
        on="tender_id",
        how="left"
    )

    datos_procesos["adjudicada"] = (
        datos_procesos["adjudicada"]
        .fillna(0)
        .astype(int)
    )

    # Predictores disponibles al publicar la compra
    columnas_modelo = [
        "tender_id",
        "date",
        "tender_procurementMethodDetails",
        "tender_competitive",
        "tender_tenderPeriod_durationInDays",
        "tender_enquiryPeriod_durationInDays",
        "tender_procuringEntity_name",
        "tender_techniques_hasFrameworkAgreement"
    ]

    datos_modelo = procesos[
        columnas_modelo
    ].drop_duplicates()

    datos_modelo["cantidad_renglones"] = (
        datos_modelo["tender_id"]
        .map(filas_por_proceso)
    )

    datos_modelo = datos_modelo.merge(
        datos_procesos,
        on="tender_id",
        how="left"
    )

    # Solo procesos finalizados
    datos_finales = datos_modelo[
        (datos_modelo["tender_status"] == "complete") |
        (datos_modelo["tender_status"] == "cancelled") |
        (datos_modelo["tender_status"] == "unsuccessful")
    ].copy()

    datos_finales["sin_adjudicacion"] = (
        datos_finales["adjudicada"] == 0
    ).astype(int)

    datos_finales["tender_procuringEntity_name"] = (
        datos_finales["tender_procuringEntity_name"]
        .fillna("No informado")
    )

    columnas_exportar = [
        "tender_id",
        "date",
        "tender_procurementMethodDetails",
        "tender_competitive",
        "tender_tenderPeriod_durationInDays",
        "tender_enquiryPeriod_durationInDays",
        "tender_procuringEntity_name",
        "tender_techniques_hasFrameworkAgreement",
        "cantidad_renglones",
        "sin_adjudicacion"
    ]

    dataset_modelo = datos_finales[
        columnas_exportar
    ].copy()

    RUTA_PROCESSED.mkdir(
        parents=True,
        exist_ok=True
    )

    dataset_modelo.to_csv(
        RUTA_PROCESSED / "dataset_modelo.csv",
        index=False
    )

    print("Dataset generado correctamente.")
    print("Dimensiones:", dataset_modelo.shape)


if __name__ == "__main__":
    main()