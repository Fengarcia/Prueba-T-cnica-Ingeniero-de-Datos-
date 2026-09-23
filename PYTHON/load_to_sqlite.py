"""
Carga de archivos CSV a SQLite.
"""

import sqlite3
import pandas as pd
import logging
import os

# Crear carpeta de logs
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

DB_NAME = "manufacturing.db"

try:

    print("Conectando a SQLite...")

    conn = sqlite3.connect(DB_NAME)

    # Leer CSV
    machines = pd.read_csv("machines.csv")
    shifts = pd.read_csv("shifts.csv")
    orders = pd.read_csv("production_orders.csv")
    downtime = pd.read_csv("downtime_events.csv")

    print("Archivos CSV encontrados")

    # Cargar tablas
    machines.to_sql(
        "machines",
        conn,
        if_exists="replace",
        index=False
    )

    shifts.to_sql(
        "shifts",
        conn,
        if_exists="replace",
        index=False
    )

    orders.to_sql(
        "production_orders",
        conn,
        if_exists="replace",
        index=False
    )

    downtime.to_sql(
        "downtime_events",
        conn,
        if_exists="replace",
        index=False
    )

    conn.commit()

    # Verificar tablas
    cursor = conn.cursor()

    cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type='table';
    """)

    print("\nTABLAS CREADAS:")

    for table in cursor.fetchall():
        print(table[0])

    conn.close()

    logging.info("Carga de datos completada")

    print("\nBase de datos creada correctamente.")

except Exception as e:

    logging.error(e)

    print(f"ERROR: {e}")