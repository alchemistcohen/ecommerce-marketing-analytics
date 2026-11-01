import os
import pytest
import pandas as pd

PATH_RENDIMIENTO = 'data/processed/rendimiento_marketing_diario.csv'
PATH_RFM = 'data/processed/segmentacion_rfm_clientes.csv'

@pytest.fixture
def df_rendimiento():
    """Fixture para cargar el dataset procesado de rendimiento de marketing."""
    return pd.read_csv(PATH_RENDIMIENTO)

@pytest.fixture
def df_rfm():
    """Fixture para cargar el dataset procesado de segmentación RFM."""
    return pd.read_csv(PATH_RFM)

# -----------------------------------------------------------------------------
# 1. PRUEBAS DE EXISTENCIA Y ESTRUCTURA DE ARCHIVOS
# -----------------------------------------------------------------------------
def test_existencia_archivos_csv():
    assert os.path.exists(PATH_RENDIMIENTO), f"El archivo {PATH_RENDIMIENTO} no existe."
    assert os.path.exists(PATH_RFM), f"El archivo {PATH_RFM} no existe."

# -----------------------------------------------------------------------------
# 2. PRUEBAS DE CALIDAD: RENDIMIENTO DE MARKETING
# -----------------------------------------------------------------------------
def test_rendimiento_columnas_y_nulos(df_rendimiento):
    columnas_esperadas = ['fecha', 'canal', 'gasto_eur', 'ingresos_eur', 'roas', 'cac', 'aov']
    for col in columnas_esperadas:
        assert col in df_rendimiento.columns, f"Falta la columna requerida: {col}"

    assert df_rendimiento['fecha'].notnull().all(), "Existen registros con fecha nula."
    assert df_rendimiento['canal'].notnull().all(), "Existen registros con canal nulo."

def test_rendimiento_consistencia_financiera(df_rendimiento):
    # Los valores monetarios y métricas no pueden ser negativos
    assert (df_rendimiento['gasto_eur'] >= 0).all(), "Existen gastos negativos."
    assert (df_rendimiento['ingresos_eur'] >= 0).all(), "Existen ingresos negativos."
    assert (df_rendimiento['roas'] >= 0).all(), "Existen valores de ROAS negativos."
    assert (df_rendimiento['cac'] >= 0).all(), "Existen valores de CAC negativos."

# -----------------------------------------------------------------------------
# 3. PRUEBAS DE CALIDAD: SEGMENTACIÓN RFM
# -----------------------------------------------------------------------------
def test_rfm_unicidad_y_rangos(df_rfm):
    # Cada cliente debe ser único
    assert df_rfm['id_cliente'].is_unique, "Se encontraron IDs de clientes duplicados en el análisis RFM."

    # Los puntajes RFM deben estar estrictamente en el rango 1 a 4
    for score_col in ['R_score', 'F_score', 'M_score']:
        assert df_rfm[score_col].isin([1, 2, 3, 4]).all(), f"Valores fuera de rango (1-4) en {score_col}."

def test_rfm_coherencia_metricas(df_rfm):
    assert (df_rfm['monto_total'] >= 0).all(), "Hay montos totales acumulados negativos."
    assert (df_rfm['frecuencia'] > 0).all(), "Existen clientes con frecuencia de compra menor o igual a cero."