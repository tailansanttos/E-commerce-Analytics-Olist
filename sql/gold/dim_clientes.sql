CREATE OR REPLACE TABLE `projeto-olist-elt.olist_gold.dim_clientes` AS
SELECT 
    customer_id,
    customer_unique_id,
    customer_zip_code_prefix AS cep,
    INITCAP(customer_city) AS cidade,
    UPPER(customer_state) AS estado
FROM `projeto-olist-elt.olist_silver.customers_silver`;