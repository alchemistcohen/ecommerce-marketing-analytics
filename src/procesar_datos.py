import pandas as pd
import numpy as np

# 1. Carga de datos generados
df_marketing = pd.read_csv('data/raw/gastos_marketing.csv')
df_ventas = pd.read_csv('data/raw/ventas_transacciones.csv')

# Conversión de tipos de fecha
df_marketing['fecha'] = pd.to_datetime(df_marketing['fecha'])
df_ventas['fecha'] = pd.to_datetime(df_ventas['fecha'])

# 2. Agregación diaria por canal de venta
ventas_por_canal = df_ventas.groupby(['fecha', 'canal_origen']).agg(
    ingresos_eur=('monto_total_eur', 'sum'),
    total_pedidos=('id_transaccion', 'count'),
    clientes_unicos=('id_cliente', 'nunique'),
    articulos_vendidos=('num_articulos', 'sum')
).reset_index().rename(columns={'canal_origen': 'canal'})

# 3. Consolidador de Marketing + Ventas
df_rendimiento = pd.merge(
    df_marketing,
    ventas_por_canal,
    on=['fecha', 'canal'],
    how='left'
).fillna(0)

# Cálculo de KPIs clave por canal y fecha
df_rendimiento['roas'] = np.where(
    df_rendimiento['gasto_eur'] > 0,
    df_rendimiento['ingresos_eur'] / df_rendimiento['gasto_eur'],
    0
)
df_rendimiento['cac'] = np.where(
    df_rendimiento['clientes_unicos'] > 0,
    df_rendimiento['gasto_eur'] / df_rendimiento['clientes_unicos'],
    0
)
df_rendimiento['aov'] = np.where(
    df_rendimiento['total_pedidos'] > 0,
    df_rendimiento['ingresos_eur'] / df_rendimiento['total_pedidos'],
    0
)

# 4. Segmentación RFM de Clientes
fecha_ref = df_ventas['fecha'].max() + pd.Timedelta(days=1)

df_rfm = df_ventas.groupby('id_cliente').agg(
    recencia_dias=('fecha', lambda x: (fecha_ref - x.max()).days),
    frecuencia=('id_transaccion', 'count'),
    monto_total=('monto_total_eur', 'sum')
).reset_index()

# Puntuaciones RFM (Cuartiles 1 a 4)
df_rfm['R_score'] = pd.qcut(df_rfm['recencia_dias'], q=4, labels=[4, 3, 2, 1])
df_rfm['F_score'] = pd.qcut(df_rfm['frecuencia'].rank(method='first'), q=4, labels=[1, 2, 3, 4])
df_rfm['M_score'] = pd.qcut(df_rfm['monto_total'], q=4, labels=[1, 2, 3, 4])

# 5. Guardar datasets procesados
df_rendimiento.to_csv('data/processed/rendimiento_marketing_diario.csv', index=False)
df_rfm.to_csv('data/processed/segmentacion_rfm_clientes.csv', index=False)

print("✅ Datasets procesados y guardados en 'data/processed/'")