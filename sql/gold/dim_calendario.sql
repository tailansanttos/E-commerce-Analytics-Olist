CREATE OR REPLACE TABLE `projeto-olist-elt.olist_gold.dim_calendario` AS
WITH gerador_de_datas AS (
    -- Gera uma lista de todas as datas de 1º de Janeiro de 2016 a 31 de Dezembro de 2019
    SELECT data_calendario
    FROM UNNEST(GENERATE_DATE_ARRAY('2016-01-01', '2019-12-31', INTERVAL 1 DAY)) AS data_calendario
)
SELECT 
    data_calendario AS data_completa,
    EXTRACT(YEAR FROM data_calendario) AS ano,
    EXTRACT(MONTH FROM data_calendario) AS mes,
    EXTRACT(DAY FROM data_calendario) AS dia,
    EXTRACT(QUARTER FROM data_calendario) AS trimestre,
    
    -- O BigQuery retorna 1 para Domingo e 7 para Sábado
    EXTRACT(DAYOFWEEK FROM data_calendario) AS numero_dia_semana,
    
    -- Cria um texto formatado, ex: 2018-01 (Ótimo para eixos de gráficos)
    FORMAT_DATE('%Y-%m', data_calendario) AS ano_mes,
    
    -- Cria uma regra condicional simples para saber se é final de semana
    CASE 
        WHEN EXTRACT(DAYOFWEEK FROM data_calendario) IN (1, 7) THEN True 
        ELSE False 
    END AS flag_fim_de_semana

FROM gerador_de_datas;