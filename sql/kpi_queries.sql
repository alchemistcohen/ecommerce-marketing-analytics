-- =============================================================================
-- CONSULTA 1: Rendimiento y Eficiencia por Canal Publicitario
-- Muestra el gasto total, ingresos, ROAS y CAC global ordenados por rentabilidad.
-- =============================================================================
SELECT 
    canal,
    SUM(gasto_eur) AS gasto_total_eur,
    SUM(ingresos_eur) AS ingresos_totales_eur,
    SUM(clientes_unicos) AS total_clientes_adquiridos,
    ROUND(SUM(ingresos_eur) / NULLIF(SUM(gasto_eur), 0), 2) AS roas_global,
    ROUND(SUM(gasto_eur) / NULLIF(SUM(clientes_unicos), 0), 2) AS cac_promedio_eur
FROM rendimiento_marketing
GROUP BY canal
ORDER BY roas_global DESC;


-- =============================================================================
-- CONSULTA 2: Segmentación de Clientes por Categoría RFM
-- Clasiﬁca a los clientes según su puntuación combinada en VIP, Leales, En Riesgo o Perdidos.
-- =============================================================================
WITH matriz_rfm AS (
    SELECT 
        id_cliente,
        recencia_dias,
        frecuencia,
        monto_total,
        (r_score + f_score + m_score) AS rfm_total_score,
        CASE 
            WHEN r_score >= 3 AND f_score >= 3 AND m_score >= 3 THEN 'Cliente VIP'
            WHEN f_score >= 3 THEN 'Cliente Leal'
            WHEN r_score <= 2 AND f_score >= 3 THEN 'En Riesgo de Fuga'
            ELSE 'Necesita Atencion'
        END AS segmento_cliente
    FROM segmentacion_rfm
)
SELECT 
    segmento_cliente,
    COUNT(id_cliente) AS total_clientes,
    ROUND(AVG(monto_total), 2) AS ticket_medio_acumulado,
    ROUND(SUM(monto_total), 2) AS ingresos_totales_segmento,
    ROUND(COUNT(id_cliente) * 100.0 / SUM(COUNT(id_cliente)) OVER (), 2) AS porcentaje_clientes
FROM matriz_rfm
GROUP BY segmento_cliente
ORDER BY ingresos_totales_segmento DESC;


-- =============================================================================
-- CONSULTA 3: Evolución Mensual de Margen Bruto y Adquisición
-- Muestra el crecimiento mes a mes de ingresos frente al presupuesto publicitario.
-- =============================================================================
SELECT 
    TO_CHAR(fecha, 'YYYY-MM') AS mes,
    SUM(gasto_eur) AS gasto_mensual_eur,
    SUM(ingresos_eur) AS ingresos_mensuales_eur,
    ROUND(SUM(ingresos_eur) - SUM(gasto_eur), 2) AS beneficio_bruto_marketing,
    ROUND(SUM(ingresos_eur) / NULLIF(SUM(gasto_eur), 0), 2) AS roas_mensual
FROM rendimiento_marketing
GROUP BY TO_CHAR(fecha, 'YYYY-MM')
ORDER BY mes ASC;