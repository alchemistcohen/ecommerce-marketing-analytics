import sqlite3
import pandas as pd

# 1. Conexión a la base de datos SQLite (se crea el archivo si no existe)
conexion = sqlite3.connect('data/ecommerce.db')

# 2. Carga de datasets procesados desde la carpeta data/processed/
df_rendimiento = pd.read_csv('data/processed/rendimiento_marketing_diario.csv')
df_rfm = pd.read_csv('data/processed/segmentacion_rfm_clientes.csv')

# 3. Escribir tablas relacionales en la base de datos
df_rendimiento.to_sql('rendimiento_marketing', conexion, if_exists='replace', index=False)
df_rfm.to_sql('segmentacion_rfm', conexion, if_exists='replace', index=False)

print("✅ Tablas 'rendimiento_marketing' y 'segmentacion_rfm' creadas en 'data/ecommerce.db'")

# 4. Verificación de las consultas SQL ejecutadas directamente en SQLite
cursor = conexion.cursor()

print("\n📊 Resultado Consulta SQL 1: Rendimiento por Canal")
query_1 = """
SELECT 
    canal,
    ROUND(SUM(gasto_eur), 2) AS gasto_total_eur,
    ROUND(SUM(ingresos_eur), 2) AS ingresos_totales_eur,
    COALESCE(ROUND(SUM(ingresos_eur) / NULLIF(SUM(gasto_eur), 0), 2), 0.00) AS roas_global
FROM rendimiento_marketing
GROUP BY canal
ORDER BY roas_global DESC;
"""

cursor.execute(query_1)
columnas = [desc[0] for desc in cursor.description]
df_resultado = pd.DataFrame(cursor.fetchall(), columns=columnas)
print(df_resultado.to_string(index=False))

conexion.close()