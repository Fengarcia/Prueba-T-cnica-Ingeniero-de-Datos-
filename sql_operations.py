"""
Operaciones SQL sobre la base de datos Manufacturing.

Este script realiza tres operaciones fundamentales de SQL:

1. INSERT:
   Inserta una nueva orden de producción en la tabla
   production_orders.

2. UPDATE:
   Actualiza los eventos de parada programada en la tabla
   downtime_events.

3. SELECT con JOIN:
   Consulta la producción total agrupada por tipo de máquina
   utilizando una unión entre las tablas production_orders
   y machines.

Base de datos utilizada:
- manufacturing.db
"""

import sqlite3

# Nombre de la base de datos SQLite.
DB_NAME = "manufacturing.db"

# ------------------------------------------------------------------
# Conexión a la base de datos
# ------------------------------------------------------------------

# Abre una conexión con la base de datos SQLite.
conn = sqlite3.connect(DB_NAME)

# Crea un cursor para ejecutar instrucciones SQL.
cursor = conn.cursor()

# ------------------------------------------------------------------
# INSERT
# ------------------------------------------------------------------

print("INSERT")

# Inserta una nueva orden de producción en la tabla
# production_orders.
#
# Datos registrados:
# - order_id: Identificador de la orden.
# - line_id: Línea de producción.
# - machine_id: Máquina utilizada.
# - product_id: Producto fabricado.
# - start_time: Fecha y hora de inicio.
# - end_time: Fecha y hora de finalización.
# - units_produced: Cantidad producida.
# - units_defective: Unidades defectuosas.
# - shift_id: Turno asociado.
cursor.execute("""
INSERT INTO production_orders
(
    order_id,
    line_id,
    machine_id,
    product_id,
    start_time,
    end_time,
    units_produced,
    units_defective,
    shift_id
)
VALUES
(
    999999,
    1,
    10,
    1,
    '2026-01-01 08:00:00',
    '2026-01-01 10:00:00',
    500,
    5,
    1
)
""")

# ------------------------------------------------------------------
# UPDATE
# ------------------------------------------------------------------

print("UPDATE")

# Actualiza los registros de la tabla downtime_events.
#
# Todos los eventos cuyo código de razón sea 'CAL-01'
# serán marcados como paradas planificadas ('planned').
cursor.execute("""
UPDATE downtime_events
SET type = 'planned'
WHERE reason_code = 'CAL-01'
""")

# ------------------------------------------------------------------
# SELECT CON JOIN
# ------------------------------------------------------------------

print("SELECT")

# Consulta la producción total agrupada por tipo de máquina.
#
# La consulta realiza:
# - Un JOIN entre production_orders y machines.
# - Una suma de las unidades producidas.
# - Un agrupamiento por tipo de máquina.
# - Un orden descendente según la producción total.
cursor.execute("""
SELECT
    m.machine_type,
    SUM(
        p.units_produced
    ) AS total_units
FROM production_orders p
INNER JOIN machines m
    ON p.machine_id = m.machine_id
GROUP BY m.machine_type
ORDER BY total_units DESC
""")

# Recupera todos los resultados de la consulta.
results = cursor.fetchall()

# ------------------------------------------------------------------
# Presentación de resultados
# ------------------------------------------------------------------

print("\nProducción por tipo de máquina\n")

# Recorre los resultados obtenidos y los muestra por consola.
#
# Ejemplo:
# ('CNC', 15000)
# ('Robot', 12000)
for row in results:
    print(row)

# ------------------------------------------------------------------
# Confirmación y cierre de conexión
# ------------------------------------------------------------------

# Guarda permanentemente los cambios realizados por las
# operaciones INSERT y UPDATE.
conn.commit()

# Cierra la conexión para liberar recursos.
conn.close()