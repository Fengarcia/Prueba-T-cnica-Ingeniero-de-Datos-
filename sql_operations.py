"""
Operaciones SQL requeridas:

1. INSERT
2. UPDATE
3. SELECT JOIN
"""

import sqlite3

DB_NAME = "manufacturing.db"

conn = sqlite3.connect(DB_NAME)

cursor = conn.cursor()

print("INSERT")

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

print("UPDATE")

cursor.execute("""
UPDATE downtime_events
SET type='planned'
WHERE reason_code='CAL-01'
""")

print("SELECT")

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

results = cursor.fetchall()

print("\nProducción por tipo de máquina\n")

for row in results:

    print(row)

conn.commit()
conn.close()