# AUDITORÍA ESTRATÉGICA DE ROI Y UNIT ECONOMICS: SHOWZ

Este repositorio contiene un diagnóstico integral sobre la rentabilidad y el comportamiento del usuario en Showz, una plataforma de comercialización de boletos (entradas) para eventos. Mediante un enfoque de Data-Driven Business, identifiqué ineficiencias críticas en la economía unitaria y diseñé una hoja de ruta estratégica para revertir el modelo de crecimiento deficitario de la organización.

---

## 🛠️ Stack Tecnológico y Arquitectura 

| Categoría        | Tecnología / Enfoque |
|------------------|----------------------|
| **Lenguaje**     | Python 3.12 |
| **Datos y procesamiento** | Pandas ≥ 3.0, PyArrow ≥ 14 (tipos y I/O optimizados) |
| **Visualización** | Matplotlib ≥ 3.9, Seaborn ≥ 0.13 |
| **Notebooks**     | Jupyter, ipykernel (entorno Conda) |
| **Metodología**  | Análisis de cohortes (retención y monetización temporal) |
| **Métricas de negocio** | LTV, CAC, ROMI, AOV; engagement (DAU/WAU/MAU, Sticky), tiempo a conversión |
| **Arquitectura** | Código modular en `src/`, pipelines y reportes en `notebooks/` |

El entorno se define en `environment.yml` (Conda). Creación: `conda env create -f environment.yml` y `conda activate showz_env`.

---

## 📂 Organización del Proyecto

```
showz_marketing_roi/
├── .cursorrules
├── .gitignore
├── .vscode/
│   └── settings.json
├── data/
│   ├── raw/                 # Datos originales (CSV)
│   │   ├── visits_log.csv
│   │   ├── orders_log.csv
│   │   └── costs.csv
│   └── processed/           # Parquets generados al ejecutar `data_cleaning.ipynb`
│       ├── visits.parquet
│       ├── orders.parquet
│       └── costs.parquet
├── notebooks/
│   ├── data_cleaning.ipynb                # Notebook demostrativo de limpieza
│   └── marketing_report_showz.ipynb       # Informe estratégico
├── src/                     # Carga y estandarización de datos, métricas y gráficos reutilizables.
│   ├── __init__.py
│   ├── data_loader.py
│   ├── metrics.py
│   └── plotting.py
├── environment.yml
├── LICENCE
└── README.md
```

---

## ⚙️ Replicabilidad

Este proyecto utiliza **Pandas 3.0** y **PyArrow** para optimizar el rendimiento. Se recomienda el uso de Conda para la gestión de dependencias.

1. **Clonar el repositorio:**
    ```bash
    git clone https://github.com/IsaacEx/showz-unit-economics-analysis.git
    ```

2.  **Instalar dependencias:**
* Utilizando **Conda**
   `conda env create -f environment.yml` → `conda activate showz_env`.
* Utilizando **pip**
    ```bash
    pip install -r requirements.txt
    ```

3. Ejecutar en orden: **`data_cleaning.ipynb`** (genera `data/processed/`) y luego **`marketing_report_showz.ipynb`**.

---
---

## 1. Resumen Ejecutivo

Tras realizar una auditoría exhaustiva del ciclo de vida del cliente y la eficiencia del gasto publicitario durante el periodo 2017–2018, se ha identificado una **crisis estructural de economía unitaria**. El costo promedio de adquisición ($CAC$) de **$7.96 USD** supera sistemáticamente el ingreso generado por la primera compra ($AOV$ de **$5.00 USD**). 

Aunque la plataforma demuestra una notable capacidad para capturar demanda con rapidez (conversión en "Día 0"), presenta una falla crítica en la retención de usuarios, perdiendo aproximadamente al **95%** de la base tras el primer mes. La sostenibilidad del modelo de negocio de **Showz** depende de una reasignación agresiva del presupuesto hacia canales de alta eficiencia y una evolución del producto que fomente la recurrencia.

---

## 2. Hallazgos Clave

### A. Fragilidad del Modelo de Producto
* **Visitantes Oportunistas:** Un *Sticky MAU* de **3.91%** confirma que el usuario no percibe a Showz como un destino habitual, sino como una herramienta transaccional de un solo uso.
* **Eficiencia vs. Emoción:** Con una mediana de sesión ($ASL$) de **5 minutos** y una moda de **1 minuto**, la plataforma se posiciona como funcionalmente eficiente para búsquedas rápidas, pero incapaz de fomentar el descubrimiento o la fidelización.

### B. Desbalance Financiero ($LTV$ vs. $CAC$)
* **Techo de Ingresos:** El valor de vida del cliente ($LTV$) en las cohortes de 2018 se mantiene estancado en un rango de **$4.40 – $5.00 USD**, lo que deja un margen de maniobra nulo para absorber costos operativos.
* **Toxicidad de la Fuente 3:** Este canal concentra el **42.5%** de la inversión total, pero presenta un $CAC$ de **$13.49 USD**. Esta cifra supera incluso el $LTV$ máximo histórico registrado en la plataforma (**$13.44 USD**), lo que significa que la empresa destruye valor neto con cada cliente adquirido por esta vía.

### C. Ventanas de Oportunidad
* **Alta Intención de Compra:** El **73%** de las conversiones se concreta en menos de 24 horas, validando una intención de compra inmediata en la primera visita.
* **Canales de Alta Eficiencia:** Las fuentes **10, 9 y 4** presentan un $CAC$ inferior a **$6 USD**, posicionándose como los únicos motores capaces de alcanzar el punto de equilibrio (*breakeven*) en el corto plazo.

---

## 3. Recomendaciones Estratégicas

**I. Reingeniería del Presupuesto de Marketing (Inmediato)**
* **Desinversión Deficitaria:** Reducir drásticamente la inversión en las **Fuentes 3 y 2**, dado que su $CAC$ es inviable frente al $LTV$ real proyectado.
* **Escalabilidad Eficiente:** Redistribuir el **50% del presupuesto** liberado hacia las **Fuentes 1, 4, 5, 9 y 10**, priorizando el crecimiento en canales con retorno de inversión comprobado.

**II. Optimización de la Conversión y Ticket Promedio**
* **Estrategia de Upselling "Día 0":** Implementar sugerencias de eventos relacionados o servicios premium durante el proceso de pago para elevar el $AOV$ por encima del umbral crítico de los **$5.00 USD**.
* **Fricción Cero:** La estabilidad y velocidad de la pasarela de pagos debe ser la prioridad técnica máxima para capitalizar la alta velocidad de conversión detectada.

**III. Pivotaje hacia la Retención (Mediano Plazo)**
* **Programas de Reactivación:** Ejecutar campañas de *retargeting* personalizadas basadas en el historial de navegación para elevar la tasa de sesiones por usuario (**1.58**) hacia niveles competitivos de la industria.

---

## 4. Próximos Pasos

1. **Dashboard de Control:** Configurar un monitor de $CAC$ vs. $LTV$ por canal con alertas automáticas ante desviaciones del $ROMI$ proyectado por debajo de **1.0**.
2. **Análisis de Atribución:** Investigar si la **Fuente 3** actúa como canal de asistencia o "primer contacto" antes de proceder a su eliminación total.
3. **Encuestas de Voice of Customer (VoC):** Identificar las razones cualitativas de la baja recurrencia para ajustar la propuesta de valor del catálogo.

> **VERDICTO FINAL:** El éxito de **Showz** depende de transitar de una estrategia de marketing basada en volumen a una centrada en la **eficiencia unitaria**, asegurando que cada dólar invertido genere un valor de vida superior a su costo de adquisición.

---
---

## ⚖️ Licencia y Autor

**Autor:** Isaac Esteban Martínez Ortega

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---