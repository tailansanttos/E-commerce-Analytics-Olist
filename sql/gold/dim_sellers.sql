CREATE OR REPLACE TABLE `projeto-olist-elt.olist_gold.dim_sellers` AS
SELECT t1.seller_id, 
t1.seller_zip_code_prefix AS cep,
INITCAP(t2.geolocation_city) AS cidade,
t1.seller_state AS estado
FROM `projeto-olist-elt.olist_silver.sellers_silver` AS t1
LEFT JOIN `projeto-olist-elt.olist_silver.geolocation_silver` AS t2
ON t1.seller_zip_code_prefix = t2.geolocation_zip_code_prefix

