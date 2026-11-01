-- Creación de tabla para el rendimiento diario de campañas y ventas
DROP TABLE IF EXISTS rendimiento_marketing;

CREATE TABLE rendimiento_marketing (
    fecha DATE NOT NULL,
    canal VARCHAR(50) NOT NULL,
    gasto_eur NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    impresiones INT NOT NULL DEFAULT 0,
    clics INT NOT NULL DEFAULT 0,
    ingresos_eur NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    total_pedidos INT NOT NULL DEFAULT 0,
    clientes_unicos INT NOT NULL DEFAULT 0,
    articulos_vendidos INT NOT NULL DEFAULT 0,
    roas NUMERIC(8, 2) GENERATED ALWAYS AS (
        CASE WHEN gasto_eur > 0 THEN ingresos_eur / gasto_eur ELSE 0 END
    ) STORED,
    cac NUMERIC(8, 2) GENERATED ALWAYS AS (
        CASE WHEN clientes_unicos > 0 THEN gasto_eur / clientes_unicos ELSE 0 END
    ) STORED,
    PRIMARY KEY (fecha, canal)
);

-- Creación de tabla para la segmentación RFM de clientes
DROP TABLE IF EXISTS segmentacion_rfm;

CREATE TABLE segmentacion_rfm (
    id_cliente VARCHAR(20) PRIMARY KEY,
    recencia_dias INT NOT NULL,
    frecuencia INT NOT NULL,
    monto_total NUMERIC(10, 2) NOT NULL,
    r_score INT NOT NULL,
    f_score INT NOT NULL,
    m_score INT NOT NULL
);