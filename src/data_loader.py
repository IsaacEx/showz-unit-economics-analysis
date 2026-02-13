# -----------------------------------------------------------------------------
# FUNCIONES PARA OBTENER EL DIAGNÓSTICO DE UN DATAFRAME Y CARGAR LOS DATOS RAW
# -----------------------------------------------------------------------------

import pandas as pd
from IPython.display import display, Markdown


def get_data_diagnostics(df, name="Dataset"):
    """
    Genera un reporte visual compacto sobre el estado de un DataFrame.
    Ideal para auditorías rápidas en notebooks de preprocesamiento.
    """
    n_rows = len(df)
    display(Markdown(f"## Diagnóstico de: `{name}`"))

    # --- Dimensiones y memoria ---
    mem_mb = df.memory_usage(deep=True).sum() / 1_048_576
    display(
        Markdown(
            f"**Dimensiones:** {n_rows:,} filas × {df.shape[1]} columnas &ensp;|&ensp; "
            f"**Memoria:** {mem_mb:.2f} MB"
        )
    )

    # --- Tabla de estructura por columna ---
    nulls = df.isnull().sum()
    pct = (nulls / n_rows * 100).round(2) if n_rows > 0 else nulls * 0

    stats = pd.DataFrame(
        {
            "Column": df.columns,
            "Type": df.dtypes.astype(str),
            "Non-Null": df.count(),
            "Nulls": nulls,
            "% Nulls": pct,
            "Unique": df.nunique(),
        }
    ).reset_index(drop=True)

    display(stats)

    # --- Duplicados ---
    n_dup = df.duplicated().sum()
    display(
        Markdown(
            f"**Filas duplicadas (completas):** {n_dup:,} "
            f"({(n_dup / n_rows * 100):.2f}%)"
            if n_rows > 0
            else "**DataFrame vacío — sin duplicados que evaluar.**"
        )
    )

    # --- Strings vacíos (relevante en pandas 3 con dtype str) ---
    str_cols = df.select_dtypes(include=["string", "object"]).columns
    if len(str_cols) > 0:
        empty_str = {
            col: (df[col].astype(str).str.strip() == "").sum() for col in str_cols
        }
        empty_str = {k: v for k, v in empty_str.items() if v > 0}
        if empty_str:
            display(
                Markdown(
                    "**Strings vacíos o solo espacios:** "
                    + ", ".join(f"`{c}` ({v:,})" for c, v in empty_str.items())
                )
            )

    # --- Resumen numérico (min / max / mean) ---
    num_cols = df.select_dtypes(include="number").columns
    if len(num_cols) > 0:
        display(Markdown("**Resumen numérico:**"))
        display(df[num_cols].describe().round(2))

    # --- Rango de fechas para columnas datetime ---
    dt_cols = df.select_dtypes(include="datetime").columns
    if len(dt_cols) > 0:
        date_ranges = {col: f"{df[col].min()} → {df[col].max()}" for col in dt_cols}
        display(
            Markdown(
                "**Rango de fechas:** "
                + " | ".join(f"`{c}`: {r}" for c, r in date_ranges.items())
            )
        )

    # --- Muestra ---
    display(Markdown("**Muestra (3 filas):**"))
    display(df.head(3))
    print("=" * 100)


def standardize_dataframe(df, dtypes=None):
    """Normaliza columnas a snake_case y aplica tipos PyArrow/category."""
    df = df.rename(columns=lambda c: c.strip().lower().replace(" ", "_"))
    if not dtypes:
        return df
    # Pre-parseo: strings temporales → datetime (necesario antes del cast)
    for c, d in dtypes.items():
        if c in df.columns and "timestamp" in str(d):
            df[c] = pd.to_datetime(df[c])
    # Cast único con diccionario
    return df.astype({c: d for c, d in dtypes.items() if c in df.columns})


def load_raw_data():
    """
    Carga inicial de los archivos CSV.
    Resuelve la ruta desde la raíz del proyecto (src/../data/raw/).
    """
    from pathlib import Path

    project_root = Path(__file__).resolve().parent.parent
    raw = project_root / "data" / "raw"

    visits = pd.read_csv(raw / "visits_log.csv")
    orders = pd.read_csv(raw / "orders_log.csv")
    costs = pd.read_csv(raw / "costs.csv")

    return visits, orders, costs


# ------------------------------------------
# FUNCIONES PARA MOSTRAR UNA PREVIEW DE LOS DATOS
# ------------------------------------------


def quick_preview(datasets):
    """Muestra head(3) y dtypes de cada DataFrame. Recibe dict {nombre: df}."""
    for name, df in datasets.items():
        print(f"\n{'─'*15} {name} {'─'*15}  ({len(df):,} filas × {df.shape[1]} columnas)")
        display(df.head(2))
        print(df.dtypes.to_string())