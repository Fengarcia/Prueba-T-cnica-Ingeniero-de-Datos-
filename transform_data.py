"""
Transformaciones y generación de tabla derivada.

Este script extrae información desde la base de datos SQLite,
aplica procesos de limpieza y transformación de datos, genera
métricas calculadas y crea una tabla analítica consolidada
llamada 'machine_performance'.

Procesos realizados:
1. Lectura de tablas desde SQLite.
2. Conversión de campos de fecha y hora.
3. Eliminación de registros duplicados.
4. Cálculo de la tasa de defectos (defect_rate).
5. Integración de datos mediante JOINs.
6. Creación de una tabla derivada para análisis.

Tablas origen:
- production_orders
- machines
- shifts

Tabla destino:
- machine_performance
"""

import sqlite3
import pandas as pd
import logging

# ------------------------------------------------------------------
# Configuración del sistema de logging
# ------------------------------------------------------------------

# Registra eventos informativos y errores en el archivo pipeline.log.
logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO
)

# Nombre de la base de datos SQLite.
DB_NAME = "manufacturing.db"

try:

    # --------------------------------------------------------------
    # Conexión a la base de datos
    # --------------------------------------------------------------

    # Abre la conexión con SQLite.
    conn = sqlite3.connect(DB_NAME)

    # --------------------------------------------------------------
    # Extracción de datos
    # --------------------------------------------------------------

    # Carga las órdenes de producción.
    orders = pd.read_sql(
        "SELECT * FROM production_orders",
        conn
    )

    # Carga el catálogo de máquinas.
    machines = pd.read_sql(
        "SELECT * FROM machines",
        conn
    )

    # Carga la información de turnos.
    shifts = pd.read_sql(
        "SELECT * FROM shifts",
        conn
    )

    print("Calculando defect_rate...")

    # --------------------------------------------------------------
    # Transformación de fechas
    # --------------------------------------------------------------

    # Convierte el campo start_time al tipo datetime.
    # Esto permite realizar análisis temporales posteriores.
    orders["start_time"] = pd.to_datetime(
        orders["start_time"]
    )

    # Convierte el campo end_time al tipo datetime.
    orders["end_time"] = pd.to_datetime(
        orders["end_time"]
    )

    # --------------------------------------------------------------
    # Limpieza de datos
    # --------------------------------------------------------------

    # Elimina registros duplicados del DataFrame.
    # El parámetro inplace=True aplica los cambios
    # directamente sobre el DataFrame original.
    orders.drop_duplicates(
        inplace=True
    )

    # --------------------------------------------------------------
    # Cálculo de métricas derivadas
    # --------------------------------------------------------------

    # Calcula la tasa de defectos por orden de producción.
    #
    # Fórmula:
    # defect_rate = unidades defectuosas / unidades producidas
    #
    # Ejemplo:
    # 10 defectuosas / 100 producidas = 0.10 (10%)
    orders["defect_rate"] = (
        orders["units_defective"]
        / orders["units_produced"]
    )

    # --------------------------------------------------------------
    # Integración de datos (JOIN)
    # --------------------------------------------------------------

    # Realiza un JOIN entre:
    # - production_orders
    # - machines
    # - shifts
    #
    # Resultado:
    # Tabla consolidada con información operacional,
    # productiva y de calendario de trabajo.
    performance = (
        orders
        .merge(
            machines,
            on="machine_id"
        )
        .merge(
            shifts,
            on="shift_id"
        )
    )

    performance.to_sql(
        "machine_performance",
        conn,
        if_exists="replace",
        index=False
    )

except Exception:
    logging.exception("Error durante la transformación")
    raise
finally:
    conn.close()
