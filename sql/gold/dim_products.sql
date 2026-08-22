CREATE OR REPLACE TABLE `projeto-olist-elt.olist_gold.dim_produtos` AS
SELECT 
    product_id,
    COALESCE(product_category_name, 'Sem Categoria') AS categoria_pt,
    COALESCE(product_category_name_english, 'Uncategorized') AS categoria_en,
    COALESCE(product_photos_qty, 0) AS qtd_fotos,
    COALESCE(product_weight_g, 0) AS peso_g,
    COALESCE(product_length_cm, 0) AS comprimento_cm, 
    COALESCE(product_height_cm, 0) AS altura_cm, 
    COALESCE(product_width_cm, 0) AS largura_cm
FROM `projeto-olist-elt.olist_silver.products_silver` 
WHERE product_id IS NOT NULL;