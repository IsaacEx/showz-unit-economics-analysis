# -----------------------------------------------------------------------------
# FUNCIONES PARA CALCULAR LAS MÉTRICAS DE NEGOCIO
# -----------------------------------------------------------------------------


# DAU, WAU, MAU y Sticky Factors
def get_product_metrics(visits):
    """
    Calcula KPIs de producto: DAU, WAU, MAU y Sticky Factors.
    """
    # Extraer componentes temporales (Optimizado para PyArrow)
    visits["date"] = visits["start_ts"].dt.date
    visits["week"] = visits["start_ts"].dt.isocalendar().week
    visits["month"] = visits["start_ts"].dt.month
    visits["year"] = visits["start_ts"].dt.year

    # Cálculos de Usuarios Únicos
    dau = visits.groupby("date").agg({"uid": "nunique"}).mean().iloc[0]
    wau = visits.groupby(["year", "week"]).agg({"uid": "nunique"}).mean().iloc[0]
    mau = visits.groupby(["year", "month"]).agg({"uid": "nunique"}).mean().iloc[0]

    # Factores de Adherencia (Sticky Factor)
    sticky_wau = (dau / wau) * 100
    sticky_mau = (dau / mau) * 100

    return {
        "dau": int(dau),
        "wau": int(wau),
        "mau": int(mau),
        "sticky_wau": round(float(sticky_wau), 2),
        "sticky_mau": round(float(sticky_mau), 2),
    }


# ASL, Mediana de ASL, Moda de ASL y Frecuencia de sesiones por usuario
def get_session_metrics(visits):
    """
    Calcula la duración promedio de sesión (ASL) y frecuencia de sesiones por usuario.
    """
    # Calcular duración en segundos
    visits["duration_sec"] = (visits["end_ts"] - visits["start_ts"]).dt.total_seconds()

    # ASL (Average Session Length)
    asl_mean = visits["duration_sec"].mean()
    asl_median = visits["duration_sec"].median()
    asl_mode = visits["duration_sec"].mode()[0]

    # Frecuencia: Sesiones por usuario único
    total_sessions = len(visits)
    total_users = visits["uid"].nunique()
    sessions_per_user = total_sessions / total_users

    return {
        "asl_mean": round(float(asl_mean), 2),
        "asl_median": round(float(asl_median), 2),
        "asl_mode": int(asl_mode),
        "sessions_per_user": round(float(sessions_per_user), 2),
    }


#
def get_retention_matrix(visits):
    """
    Calcula la matriz de retención por cohortes mensuales.
    """
    # Determinar el mes de la primera visita para cada usuario
    first_visits = visits.groupby("uid")["start_ts"].min().reset_index()
    first_visits.columns = ["uid", "first_visit_month"]
    first_visits["first_visit_month"] = (
        first_visits["first_visit_month"].astype("datetime64[ns]").dt.to_period("M")
    )

    # Unir con el dataframe original
    visits_cohorts = visits.merge(first_visits, on="uid")
    visits_cohorts["visit_month"] = (
        visits_cohorts["start_ts"].astype("datetime64[ns]").dt.to_period("M")
    )

    # Calcular la "edad" de la cohorte (cohort_lifetime)
    # En Pandas 3.0, la resta de periodos devuelve un objeto que convertimos a entero
    visits_cohorts["cohort_lifetime"] = (
        visits_cohorts["visit_month"] - visits_cohorts["first_visit_month"]
    ).apply(lambda x: x.n)

    # Tabla pivote de usuarios únicos
    cohort_report = visits_cohorts.pivot_table(
        index="first_visit_month",
        columns="cohort_lifetime",
        values="uid",
        aggfunc="nunique",
    )

    # Calcular el porcentaje de retención
    initial_users_count = cohort_report[0]
    retention_matrix = cohort_report.divide(initial_users_count, axis=0) * 100

    return retention_matrix


# Funcion para calcular el tiempo transcurrido entre la primera visita y la primera compra
def get_conversion_time(visits, orders):
    """
    Calcula el tiempo transcurrido entre la primera visita y la primera compra.
    """
    # Encontrar la primera visita de cada usuario
    first_visits = visits.groupby("uid")["start_ts"].min().reset_index()
    first_visits.columns = ["uid", "first_session_ts"]

    # Encontrar la primera compra de cada usuario
    first_orders = orders.groupby("uid")["buy_ts"].min().reset_index()
    first_orders.columns = ["uid", "first_order_ts"]

    # Unir las tablas y calcular la diferencia
    conversion = first_orders.merge(first_visits, on="uid")

    # Diferencia en días (puedes cambiar a 'h' para horas o 'm' para minutos)
    conversion["time_to_conversion"] = (
        conversion["first_order_ts"] - conversion["first_session_ts"]
    ).dt.days

    return conversion["time_to_conversion"]


# Funcion para calcular el Ticket Promedio (AOV) general y su evolución mensual
def get_aov_metrics(orders):
    """
    Calcula el ticket promedio real (solo pedidos con ingreso).
    """
    # Filtramos pedidos monetizados
    paying_orders = orders.query("revenue > 0").copy()

    # Calculamos AOV con el denominador correcto
    aov_paying = paying_orders["revenue"].sum() / len(paying_orders)

    # También calculamos la evolución mensual (clave para ver estacionalidad)
    paying_orders["month"] = (
        paying_orders["buy_ts"].astype("datetime64[ns]").dt.to_period("M")
    )
    monthly_aov = paying_orders.groupby("month")["revenue"].mean()

    return {"aov_paying": round(float(aov_paying), 2), "monthly_aov": monthly_aov}


# Funcion para calcular el Lifetime Value (LTV) acumulado por mes de vida de la cohorte
def get_ltv_matrix(orders):
    """
    Calcula el LTV acumulado por cohortes mensuales.
    """
    # Definir el mes de primera compra para cada usuario
    first_orders = (
        orders.groupby("uid")["buy_ts"].min().astype("datetime64[ns]").dt.to_period("M")
    )
    first_orders.name = "first_order_month"

    # Unir con los datos originales
    orders_cohorts = orders.merge(first_orders, on="uid")
    orders_cohorts["order_month"] = (
        orders_cohorts["buy_ts"].astype("datetime64[ns]").dt.to_period("M")
    )

    # Calcular el ciclo de vida (edad de la cohorte)
    orders_cohorts["cohort_lifetime"] = (
        orders_cohorts["order_month"] - orders_cohorts["first_order_month"]
    ).apply(lambda x: x.n)

    # Agrupar ingresos por cohorte y edad
    revenue_cohorts = (
        orders_cohorts.groupby(["first_order_month", "cohort_lifetime"])["revenue"]
        .sum()
        .reset_index()
    )

    # Calcular el tamaño inicial de cada cohorte (compradores únicos por mes)
    cohort_sizes = (
        orders_cohorts.groupby("first_order_month")["uid"].nunique().reset_index()
    )
    cohort_sizes.columns = ["first_order_month", "n_buyers"]

    # Unir ingresos con tamaños y calcular LTV por periodo
    report = revenue_cohorts.merge(cohort_sizes, on="first_order_month")
    report["ltv"] = report["revenue"] / report["n_buyers"]

    # Pivotar y calcular el LTV acumulado
    ltv_pivot = report.pivot_table(
        index="first_order_month",
        columns="cohort_lifetime",
        values="ltv",
        aggfunc="sum",
    ).cumsum(axis=1)

    return ltv_pivot


# Funcion para calcular el gasto total por fuente y a través del tiempo
def get_marketing_spend(costs):
    """
    Calcula la distribución del gasto por canal y a través del tiempo.
    """
    # Gasto total por fuente
    spend_by_source = (
        costs.groupby("source_id")["costs"].sum().sort_values(ascending=False)
    )

    # Gasto mensual por fuente (pivot: index=mes, columns=source_id)
    costs["month"] = costs["dt"].astype("datetime64[ns]").dt.to_period("M")
    spend_over_time = costs.pivot_table(
        index="month", columns="source_id", values="costs", aggfunc="sum"
    )

    return {"spend_by_source": spend_by_source, "spend_over_time": spend_over_time}


# Funcion para calcular el Costo de Adquisición de Clientes (CAC) por fuente
def get_cac_metrics(visits, orders, costs):
    """
    Calcula el CAC por fuente cruzando visits (source_id) con orders (compradores).
    """
    # Fuente de adquisición: source_id de la primera visita cronológica
    first_visit = (
        visits.sort_values("start_ts").groupby("uid")["source_id"].first().reset_index()
    )

    # Primera compra de cada usuario
    first_order = orders.sort_values("buy_ts").groupby("uid").first().reset_index()
    first_order["month"] = (
        first_order["buy_ts"].astype("datetime64[ns]").dt.to_period("M")
    )

    # Cruce: cada comprador con su fuente de adquisición
    buyers = first_order.merge(first_visit, on="uid")

    # Nuevos clientes por (mes, fuente)
    new_customers = (
        buyers.groupby(["month", "source_id"])["uid"].nunique().reset_index()
    )
    new_customers.columns = ["month", "source_id", "n_clients"]

    # Costos por (mes, fuente)
    costs = costs.copy()
    costs["month"] = costs["dt"].astype("datetime64[ns]").dt.to_period("M")
    monthly_costs = costs.groupby(["month", "source_id"])["costs"].sum().reset_index()

    # Unir y calcular CAC
    cac_report = monthly_costs.merge(new_customers, on=["month", "source_id"])
    cac_report["cac"] = cac_report["costs"] / cac_report["n_clients"]

    # CAC total por fuente (gasto total / clientes totales — más robusto que promediar)
    totals = cac_report.groupby("source_id").agg(
        total_cost=("costs", "sum"), total_clients=("n_clients", "sum")
    )
    cac_by_source = totals["total_cost"] / totals["total_clients"]

    return {
        "cac_by_source": cac_by_source,
        "full_report": cac_report,
    }


# Funcion para calcular el Return on Marketing Investment (ROMI) por fuente
def get_romi_matrix(orders, costs):
    """
    Calcula el ROMI acumulado por cohortes: LTV / CAC.
    """
    # LTV acumulado por cohorte (reutiliza la función existente)
    ltv = get_ltv_matrix(orders)

    # Nuevos clientes por mes de primera compra
    first_order_month = (
        orders.groupby("uid")["buy_ts"].min().astype("datetime64[ns]").dt.to_period("M")
    )
    new_clients = first_order_month.value_counts().sort_index()

    # Gasto total de marketing por mes
    costs = costs.copy()
    costs["month"] = costs["dt"].astype("datetime64[ns]").dt.to_period("M")
    monthly_spend = costs.groupby("month")["costs"].sum()

    # CAC por mes de adquisición
    cac = monthly_spend / new_clients

    # ROMI = LTV / CAC (alineado por mes de adquisición)
    return ltv.divide(cac, axis=0)
