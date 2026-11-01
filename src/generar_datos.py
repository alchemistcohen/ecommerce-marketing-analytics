import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

# Configuración de parámetros
num_dias = 90
fecha_inicio = datetime(2026, 1, 1)
fechas = [fecha_inicio + timedelta(days=i) for i in range(num_dias)]
canales = ['Google Ads', 'Meta Ads', 'TikTok Ads', 'Email Marketing', 'Búsqueda Orgánica']

# 1. Generación de Gastos de Marketing
registros_marketing = []
for fecha in fechas:
    for canal in canales:
        if canal == 'Búsqueda Orgánica':
            gasto = 0
            clics = np.random.randint(100, 500)
            impresiones = clics * np.random.randint(10, 20)
        else:
            gasto = round(float(np.random.uniform(50, 500)), 2)
            impresiones = int(gasto * np.random.uniform(20, 50))
            clics = int(impresiones * np.random.uniform(0.01, 0.05))
            
        registros_marketing.append({
            'fecha': fecha.strftime('%Y-%m-%d'),
            'canal': canal,
            'gasto_eur': gasto,
            'impresiones': impresiones,
            'clics': clics
        })

df_marketing = pd.DataFrame(registros_marketing)
df_marketing.to_csv('data/raw/gastos_marketing.csv', index=False)

# 2. Generación de Transacciones de Ventas
num_clientes = 500
clientes_ids = [f"CLI-{1000 + i}" for i in range(num_clientes)]
registros_ventas = []

for _ in range(2500):
    fecha = np.random.choice(fechas)
    cliente = np.random.choice(clientes_ids)
    canal = np.random.choice(canales, p=[0.3, 0.3, 0.15, 0.1, 0.15])
    monto = round(float(np.random.exponential(scale=45) + 15), 2)
    num_items = np.random.randint(1, 6)
    
    registros_ventas.append({
        'id_transaccion': f"TRX-{np.random.randint(100000, 999999)}",
        'fecha': fecha.strftime('%Y-%m-%d'),
        'id_cliente': cliente,
        'canal_origen': canal,
        'monto_total_eur': monto,
        'num_articulos': num_items
    })

df_ventas = pd.DataFrame(registros_ventas)
df_ventas.to_csv('data/raw/ventas_transacciones.csv', index=False)

print("✅ Datos sintéticos generados con éxito en la carpeta 'data/raw/'")