# Prueba-T-cnica-Ingeniero-de-Datos-
Prueba Técnica – Ingeniero de Datos Junior Descripción General Este proyecto implementa un mini pipeline de datos en Python que cubre las etapas de extracción, carga, transformación y consulta de información, utilizando múltiples fuentes de datos y una base de datos relacional SQLite.

Este proyecto implementa un pipeline de datos en Python compuesto por las etapas de extracción, carga, transformación y consulta SQL.

> [!NOTE]
> PARTE N° 1

## PARTE 1 ENTREGABLES

Las fuentes de datos utilizadas son:

1. API pública REST (JSONPlaceholder).
2. Archivos CSV generados a partir del dataset sintético.
3. Dataset relacional almacenado en SQLite.

# Diagrama de flujo de abstraccion de datos 

<img width="538" height="604" alt="diagrama abstraccion de datos" src="https://github.com/user-attachments/assets/fbda5be5-62d8-4410-9527-13588e0f0aa6" />

# 1. Generar datos (script con generacion de los 10.000 registros a partir de la semilla CC)
python Scrip_Generacion.py

> [!TIP]
> Se ejecutan los script en la siguiente secuencia como se denota a continuación. 
 
# 2. Crear base y cargar CSV
python load_to_sqlite.py

# 3. Consumir API
python extract_api.py
 
# 4. Transformar datos
python transform_data.py
 
# 5. Ejecutar SQL
python sql_operations.py

-------------------------------------------------------------------------------------

# Justificación de las Transformaciones Aplicadas
Objetivo de las transformaciones

* La etapa de transformación tuvo como objetivo garantizar la calidad, consistencia y disponibilidad de los datos para su posterior análisis, permitiendo identificar patrones de producción, defectos y eventos de parada dentro del proceso de manufactura

# 1. Conversión de campos de fecha y hora

Los datos generados por los archivos CSV se encuentran inicialmente como cadenas de texto. La conversión a formato fecha permite:

* Realizar cálculos temporales.
* Analizar duración de órdenes de producción.
* Calcular tiempos de parada.
* Facilitar futuras métricas relacionadas con productividad y disponibilidad.

Esta transformación mejora la capacidad analítica del modelo de datos.

# 2. Eliminación de registros duplicados

drop_duplicates()

Su objetivo:

* Evitar el conteo múltiple de eventos.
* Garantizar la consistencia de indicadores
* Prevenir resultados incorrectos en consultas agregadas.

# 3. Creación de la métrica Defect Rate

Creacion de la columna "defect_rate" mediante "units_defective / units_produced"

La cantidad absoluta de unidades defectuosas no permite comparar correctamente el desempeño entre máquinas o líneas de producción con diferentes volúmenes de fabricación.

La tasa de defectos normaliza esta información y permite:

* Comparar máquinas de distintos tamaños.
* Identificar procesos con problemas de calidad.
* Priorizar acciones de mejora.
* Construir rankings de desempeño.

> [!NOTE] 
> Esta métrica fue utilizada como uno de los principales indicadores del análisis de negocio.

# 4. Integración de tablas mediante JOIN

integración entre

* production_orders
* machines
* shifts

La información de producción se encontraba distribuida en diferentes tablas relacionadas.

La utilización de JOIN permitió:

* Asociar órdenes de producción con sus máquinas.
* Incorporar información del turno responsable.
* Centralizar la información necesaria para el análisis.
* Reducir la complejidad de futuras consultas.

Esta integración facilitó la construcción de una estructura analítica más cercana a las necesidades de negocio.

# 5. Creación de la tabla derivada machine_performance

se genera la tabla "machine_performance" a partir del Join de las tablas operativas

El objetivo fue disponer de una tabla analítica preparada para responder preguntas de negocio sin necesidad de realizar múltiples uniones en cada consulta.

> [!NOTE]
> PARTE N° 2 entregables y ejecución de las dependencias y clon de el repositorio.

## PARTE 2 ENTREGABLES

Clonar repositorio 



