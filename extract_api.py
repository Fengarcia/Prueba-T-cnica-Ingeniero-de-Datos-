"""
Módulo de extracción de datos desde una API pública.

Este script consume información de usuarios desde la API pública
JSONPlaceholder, transforma la respuesta en un DataFrame de Pandas
y almacena los datos en una base de datos SQLite.

Funcionalidades:
- Consume un endpoint REST mediante requests.
- Convierte la respuesta JSON en un DataFrame.
- Guarda los datos en una tabla SQLite.
- Registra eventos y errores en un archivo de log.

Autor: [Tu nombre]
Fecha: [Fecha]
"""

import sqlite3
import pandas as pd
import requests
import logging
import time
import os

# Configuración del sistema de logging.
# Todos los eventos de información y errores se almacenarán
# en el archivo logs/pipeline.log.
# Crea la carpeta 'logs' si no existe.
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO
)

# Nombre de la base de datos SQLite donde se almacenarán los datos.
DB_NAME = "manufacturing.db"

try:
    # Mensaje informativo para indicar el inicio del consumo de la API.
    print("Consumiendo API...")

    # Simula una pequeña espera antes de realizar la petición.
    time.sleep(1)

    # Realiza una petición GET al endpoint de usuarios.
    # Se define un timeout de 10 segundos para evitar bloqueos.
    response = requests.get(
        "https://jsonplaceholder.typicode.com/users",
        timeout=10
    )

    # Lanza una excepción si el código de respuesta HTTP indica error.
    response.raise_for_status()

    # Convierte la respuesta JSON en un DataFrame de Pandas.
    users = pd.DataFrame(
        response.json()
    )

    # Establece la conexión con la base de datos SQLite.
    conn = sqlite3.connect(DB_NAME)

    # Guarda el DataFrame en la tabla 'api_users'.
    # Si la tabla ya existe, será reemplazada.
    users.to_sql(
        "api_users",
        conn,
        if_exists="replace",
        index=False
    )

    # Cierra la conexión para liberar recursos.
    conn.close()

    # Muestra por consola la cantidad de registros cargados.
    print(
        f"{len(users)} registros cargados desde API"
    )

    # Registra en el log que la carga se realizó correctamente.
    logging.info(
        "Datos API cargados correctamente"
    )

except Exception as e:
    """
    Captura cualquier excepción ocurrida durante:
    - La conexión a la API.
    - La transformación de los datos.
    - La escritura en la base de datos.

    El error se registra en el log y se muestra por pantalla.
    """

    logging.error(e)

    print(e)