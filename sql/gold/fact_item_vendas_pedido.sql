CREATE OR REPLACE TABLE `projeto-olist-elt.olist_gold.fato_itens_venda` AS
SELECT 
    t1.order_id, 
    t2.order_item_id,
    t1.customer_id, 
    t2.product_id, 
    t2.seller_id, 
    t2.price AS preco, 
    t2.freight_value AS valor_frete,
    t1.order_purchase_timestamp AS data_pedido,
    t1.order_approved_at AS data_aprovado,
    t1.order_delivered_customer_date AS data_entrega
FROM `projeto-olist-elt.olist_silver.orders_silver` AS t1
INNER JOIN `projeto-olist-elt.olist_silver.order_items_silver` AS t2
ON t1.order_id = t2.order_id;