"""
Extracción de datos desde API pública.
"""

import sqlite3
import pandas as pd
import requests
import logging
import time

logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO
)

DB_NAME = "manufacturing.db"

try:

    print("Consumiento API...")

    time.sleep(1)

    response = requests.get(
        "https://jsonplaceholder.typicode.com/users",
        timeout=10
    )

    response.raise_for_status()

    users = pd.DataFrame(
        response.json()
    )

    conn = sqlite3.connect(DB_NAME)

    users.to_sql(
        "api_users",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

    print(
        f"{len(users)} registros cargados desde API"
    )

    logging.info(
        "Datos API cargados correctamente"
    )

except Exception as e:

    logging.error(e)

    print(e)