"""
Transformaciones y generación de tabla derivada.
"""

import sqlite3
import pandas as pd
import logging

logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO
)

DB_NAME = "manufacturing.db"

try:

    conn = sqlite3.connect(DB_NAME)

    orders = pd.read_sql(
        "SELECT * FROM production_orders",
        conn
    )

    machines = pd.read_sql(
        "SELECT * FROM machines",
        conn
    )

    shifts = pd.read_sql(
        "SELECT * FROM shifts",
        conn
    )

    print("Calculando defect_rate...")

    # Conversión de fechas
    orders["start_time"] = pd.to_datetime(
        orders["start_time"]
    )

    orders["end_time"] = pd.to_datetime(
        orders["end_time"]
    )

    # Eliminar duplicados
    orders.drop_duplicates(
        inplace=True
    )

    # Métrica derivada
    orders["defect_rate"] = (
        orders["units_defective"]
        / orders["units_produced"]
    )

    # Join requerido
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

    conn.close()

    print(
        "Tabla machine_performance creada"
    )

    logging.info(
        "Transformaciones completadas"
    )

except Exception as e:

    logging.error(e)
    print(e)