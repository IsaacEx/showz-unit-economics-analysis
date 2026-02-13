import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------------------------------------------------------
# FUNCIONES PARA GRAFICAR LAS MÉTRICAS
# -----------------------------------------------------------------------------


# Funcion para graficar la matriz de retención y LTV por cohortes mensuales
def plot_cohort_heatmap(
    data, title, xlabel, ylabel, fmt=".1f", vmax=None, figsize=(14, 7)
):
    """
    Heatmap monocromático para matrices de cohortes (retención, LTV, etc.).
    Parameters
    ----------
    data : pd.DataFrame
        Matriz pivotada (índice = cohorte, columnas = lifetime).
    title, xlabel, ylabel : str
        Textos del gráfico.
    fmt : str
        Formato de anotación (ej. '.1f' para %, '.2f' para moneda).
    figsize : tuple
        Tamaño de la figura.
    """
    fig, ax = plt.subplots(figsize=figsize)

    # PyArrow NA → np.nan para compatibilidad con seaborn
    data = data.astype("float64")

    sns.heatmap(
        data,
        annot=True,
        fmt=fmt,
        cmap="Blues",
        vmax=vmax,
        linewidths=0.5,
        linecolor="white",
        cbar_kws={"shrink": 0.8, "label": ""},
        ax=ax,
    )

    ax.set_title(title, fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel(xlabel, fontsize=11, labelpad=10)
    ax.set_ylabel(ylabel, fontsize=11, labelpad=10)
    ax.tick_params(axis="both", labelsize=9)

    plt.tight_layout()
    plt.show()


# Funcion para graficar series temporales (AOV mensual, conversiones, etc.)
def plot_time_series(
    data, title, xlabel, ylabel, color="teal", marker="o", linewidth=2, figsize=(12, 5)
):
    """
    Line plot para series temporales (AOV mensual, conversiones, etc.).

    Parameters
    ----------
    data : pd.Series
        Serie con índice temporal (str o Period) y valores numéricos.
    title, xlabel, ylabel : str
        Textos del gráfico.
    color : str
        Color de la línea.
    marker : str
        Marcador de puntos.
    linewidth : float
        Grosor de la línea.
    figsize : tuple
        Tamaño de la figura.
    """
    fig, ax = plt.subplots(figsize=figsize)

    data.plot(kind="line", marker=marker, color=color, linewidth=linewidth, ax=ax)

    ax.set_title(title, fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel(xlabel, fontsize=11, labelpad=10)
    ax.set_ylabel(ylabel, fontsize=11, labelpad=10)
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.tick_params(axis="both", labelsize=9)
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()


# Funcion para graficar barras (gasto por fuente, CAC, etc.)
def plot_bar(
    data, title, xlabel, ylabel, color="teal", annotate=False, figsize=(12, 6)
):
    """
    Bar plot para comparaciones categóricas.

    Parameters
    ----------
    data : pd.Series
        Serie con índice categórico y valores numéricos.
    title, xlabel, ylabel : str
        Textos del gráfico.
    color : str
        Color de las barras.
    figsize : tuple
        Tamaño de la figura.
    """
    fig, ax = plt.subplots(figsize=figsize)

    data.plot(kind="bar", color=color, ax=ax)

    ax.set_title(title, fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel(xlabel, fontsize=11, labelpad=10)
    ax.set_ylabel(ylabel, fontsize=11, labelpad=10)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.tick_params(axis="both", labelsize=9)
    if annotate:
        for container in ax.containers:
            ax.bar_label(container, fmt="%.2f", fontsize=9, padding=3)
    plt.xticks(rotation=0)

    plt.tight_layout()
    plt.show()


# Funcion para graficar múltiples líneas (gasto por fuente en el tiempo, etc.)
def plot_multi_lines(data, title, xlabel, ylabel, figsize=(13, 6)):
    """
    Line plot con múltiples series (una línea por columna del DataFrame).

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame donde cada columna es una serie y el índice es el eje X.
    title, xlabel, ylabel : str
        Textos del gráfico.
    figsize : tuple
        Tamaño de la figura.
    """
    fig, ax = plt.subplots(figsize=figsize)

    data.plot(kind="line", marker="o", linewidth=1.5, ax=ax)

    ax.set_title(title, fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel(xlabel, fontsize=11, labelpad=10)
    ax.set_ylabel(ylabel, fontsize=11, labelpad=10)
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.tick_params(axis="both", labelsize=9)
    ax.legend(title="Source", fontsize=9, title_fontsize=10)
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()
