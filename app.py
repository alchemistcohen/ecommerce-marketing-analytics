import sqlite3
import pandas as pd
import plotly.express as px
import streamlit as st

# Configuración inicial de la página
st.set_page_config(
    page_title="Dashboard de Analítica Marketing & E-Commerce",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard de Analítica de Marketing & E-Commerce")
st.markdown("Análisis interactivo de rentabilidad publicitaria, atribución por canal y segmentación de clientes (RFM).")

# Conexión a la base de datos SQLite
@st.cache_data
def cargar_datos():
    conexion = sqlite3.connect('data/ecommerce.db')
    df_rendimiento = pd.read_sql_query("SELECT * FROM rendimiento_marketing", conexion)
    df_rfm = pd.read_sql_query("SELECT * FROM segmentacion_rfm", conexion)
    conexion.close()
    
    df_rendimiento['fecha'] = pd.to_datetime(df_rendimiento['fecha'])
    return df_rendimiento, df_rfm

df_rendimiento, df_rfm = cargar_datos()

# Sidebar: Filtros de usuario
st.sidebar.header("🔍 Filtros de Control")

# Filtro por canal
canales_disponibles = list(df_rendimiento['canal'].unique())
canales_seleccionados = st.sidebar.multiselect(
    "Selecciona Canales Publicitarios:",
    options=canales_disponibles,
    default=canales_disponibles
)

# Filtro por rango de fechas
fecha_min = df_rendimiento['fecha'].min().date()
fecha_max = df_rendimiento['fecha'].max().date()
rango_fechas = st.sidebar.date_input(
    "Rango de Fechas:",
    value=[fecha_min, fecha_max],
    min_value=fecha_min,
    max_value=fecha_max
)

# Aplicar filtros
if len(rango_fechas) == 2:
    f_inicio, f_fin = pd.to_datetime(rango_fechas[0]), pd.to_datetime(rango_fechas[1])
    df_filtrado = df_rendimiento[
        (df_rendimiento['canal'].isin(canales_seleccionados)) &
        (df_rendimiento['fecha'] >= f_inicio) &
        (df_rendimiento['fecha'] <= f_fin)
    ]
else:
    df_filtrado = df_rendimiento[df_rendimiento['canal'].isin(canales_seleccionados)]

# --- MÉTRICAS PRINCIPALES (KPIs) ---
st.subheader("📌 Resumen Ejecutivo de Métricas Clave")

gasto_total = df_filtrado['gasto_eur'].sum()
ingresos_totales = df_filtrado['ingresos_eur'].sum()
clientes_totales = df_filtrado['clientes_unicos'].sum()
pedidos_totales = df_filtrado['total_pedidos'].sum()

roas_global = ingresos_totales / gasto_total if gasto_total > 0 else 0
cac_promedio = gasto_total / clientes_totales if clientes_totales > 0 else 0
aov_promedio = ingresos_totales / pedidos_totales if pedidos_totales > 0 else 0

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
kpi1.metric("Ingresos Totales", f"€{ingresos_totales:,.2f}")
kpi2.metric("Gasto Publicitario", f"€{gasto_total:,.2f}")
kpi3.metric("ROAS Global", f"{roas_global:.2f}x")
kpi4.metric("CAC Promedio", f"€{cac_promedio:.2f}")
kpi5.metric("Ticket Medio (AOV)", f"€{aov_promedio:.2f}")

st.markdown("---")

# --- PESTAÑAS DE ANÁLISIS ---
tab1, tab2 = st.tabs(["📈 Rendimiento de Marketing & Canales", "👥 Segmentación RFM de Clientes"])

with tab1:
    st.subheader("Análisis de Eficiencia por Canal")
    
    # Agregación por canal
    df_canal = df_filtrado.groupby('canal').agg(
        gasto_total=('gasto_eur', 'sum'),
        ingresos_totales=('ingresos_eur', 'sum'),
        clientes=('clientes_unicos', 'sum')
    ).reset_index()
    
    df_canal['roas'] = df_canal.apply(lambda r: r['ingresos_totales'] / r['gasto_total'] if r['gasto_total'] > 0 else 0, axis=1)
    df_canal['cac'] = df_canal.apply(lambda r: r['gasto_total'] / r['clientes'] if r['clientes'] > 0 else 0, axis=1)
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        fig_roas = px.bar(
            df_canal, x='canal', y='roas', color='canal',
            title="ROAS por Canal Publicitario",
            labels={'roas': 'ROAS (x)', 'canal': 'Canal'},
            text_auto='.2f'
        )
        st.plotly_chart(fig_roas, use_container_width=True)
        
    with col_chart2:
        fig_cac = px.bar(
            df_canal, x='canal', y='cac', color='canal',
            title="Coste de Adquisición de Cliente (CAC) en €",
            labels={'cac': 'CAC (€)', 'canal': 'Canal'},
            text_auto='.2f'
        )
        st.plotly_chart(fig_cac, use_container_width=True)

    # Tendencia temporal
    st.subheader("Evolución Temporal de Ingresos vs. Gasto")
    df_diario = df_filtrado.groupby('fecha').agg(
        ingresos=('ingresos_eur', 'sum'),
        gasto=('gasto_eur', 'sum')
    ).reset_index()
    
    fig_linea = px.line(
        df_diario, x='fecha', y=['ingresos', 'gasto'],
        title="Tendencia Diaria de Ingresos vs Gasto Publicitario",
        labels={'value': 'Euros (€)', 'fecha': 'Fecha', 'variable': 'Métrica'}
    )
    st.plotly_chart(fig_linea, use_container_width=True)

with tab2:
    st.subheader("Distribución de Clientes por Matriz RFM")
    
    def clasificar_rfm(row):
        r, f, m = row['R_score'], row['F_score'], row['M_score']
        if r >= 3 and f >= 3 and m >= 3:
            return 'Cliente VIP'
        elif f >= 3:
            return 'Cliente Leal'
        elif r <= 2 and f >= 3:
            return 'En Riesgo de Fuga'
        else:
            return 'Necesita Atención'

    df_rfm['segmento'] = df_rfm.apply(clasificar_rfm, axis=1)
    
    rfm_resumen = df_rfm.groupby('segmento').agg(
        total_clientes=('id_cliente', 'count'),
        monto_promedio=('monto_total', 'mean'),
        monto_total=('monto_total', 'sum')
    ).reset_index()
    
    c1, c2 = st.columns(2)
    
    with c1:
        fig_pie = px.pie(
            rfm_resumen, names='segmento', values='total_clientes',
            title="Distribución de Clientes por Segmento RFM",
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with c2:
        fig_monto = px.bar(
            rfm_resumen, x='segmento', y='monto_total', color='segmento',
            title="Ingresos Totales Aportados por Segmento (€)",
            text_auto=',.2f'
        )
        st.plotly_chart(fig_monto, use_container_width=True)