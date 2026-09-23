"""
Carga de archivos CSV a SQLite.

Este script realiza el proceso de ingesta de datos desde múltiples
archivos CSV hacia una base de datos SQLite.

Procesos ejecutados:
1. Configura el sistema de logging.
2. Verifica la existencia de la carpeta de logs.
3. Establece conexión con SQLite.
4. Carga los archivos CSV en DataFrames de Pandas.
5. Inserta los datos en tablas SQLite.
6. Verifica que las tablas hayan sido creadas correctamente.
7. Registra el resultado de la ejecución en un archivo de log.

Tablas creadas:
- machines
- shifts
- production_orders
- downtime_events

Base de datos destino:
- manufacturing.db
"""

import sqlite3
import pandas as pd
import logging
import os

# ------------------------------------------------------------------
# Configuración de directorios
# ------------------------------------------------------------------

# Crea el directorio 'logs' si no existe.
# La opción exist_ok=True evita generar una excepción cuando
# la carpeta ya está creada.
os.makedirs("logs", exist_ok=True)

# ------------------------------------------------------------------
# Configuración del sistema de logging
# ------------------------------------------------------------------

# Configura el archivo donde se almacenarán los eventos del proceso.
# Se registra fecha, nivel del mensaje y descripción del evento.
logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Nombre de la base de datos SQLite.
DB_NAME = "manufacturing.db"

try:

    # --------------------------------------------------------------
    # Conexión a la base de datos
    # --------------------------------------------------------------

    print("Conectando a SQLite...")

    # Crea o abre la base de datos especificada.
    conn = sqlite3.connect(DB_NAME)

    # --------------------------------------------------------------
    # Lectura de archivos CSV
    # --------------------------------------------------------------

    # Carga la información de máquinas.
    machines = pd.read_csv("machines.csv")

    # Carga la información de turnos de trabajo.
    shifts = pd.read_csv("shifts.csv")

    # Carga las órdenes de producción.
    orders = pd.read_csv("production_orders.csv")

    # Carga los eventos de parada o indisponibilidad.
    downtime = pd.read_csv("downtime_events.csv")

    print("Archivos CSV encontrados")

    # --------------------------------------------------------------
    # Carga de información hacia SQLite
    # --------------------------------------------------------------

    # Inserta los datos de máquinas en la tabla 'machines'.
    # Si la tabla existe, se reemplaza completamente.
    machines.to_sql(
        "machines",
        conn,
        if_exists="replace",
        index=False
    )

    # Inserta los datos de turnos.
    shifts.to_sql(
        "shifts",
        conn,
        if_exists="replace",
        index=False
    )

    # Inserta las órdenes de producción.
    orders.to_sql(
        "production_orders",
        conn,
        if_exists="replace",
        index=False
    )

    # Inserta los eventos de parada.
    downtime.to_sql(
        "downtime_events",
        conn,
        if_exists="replace",
        index=False
    )

    # Confirma la transacción en la base de datos.
    conn.commit()

    # --------------------------------------------------------------
    # Verificación de tablas creadas
    # --------------------------------------------------------------

    cursor = conn.cursor()

    # Consulta las tablas registradas en SQLite.
    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table';
    """)

    print("\nTABLAS CREADAS:")

    # Recorre y muestra cada tabla disponible.
    for table in cursor.fetchall():
        print(table[0])

    # Cierra la conexión con la base de datos.
    conn.close()

    # Registra la ejecución exitosa.
    logging.info("Carga de datos completada correctamente")

    print("\nBase de datos creada correctamente.")

except Exception as e:

    # --------------------------------------------------------------
    # Manejo de errores
    # --------------------------------------------------------------

    # Registra el error ocurrido durante la ejecución.
    logging.error(e)

    # Muestra el error por consola.
    print(f"ERROR: {e}")