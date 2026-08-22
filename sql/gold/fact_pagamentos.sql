CREATE OR REPLACE TABLE  `projeto-olist-elt.olist_gold.fato_pagamentos`  AS
SELECT t1.order_id,  
t2.customer_id,
t1.payment_type AS tipo_pagamento,
t1.payment_sequential AS sequencia_pagamento,
t1.payment_installments AS parcelas,
t1.payment_value AS valor_pagamento,
t2.order_purchase_timestamp AS data_pedido
FROM `projeto-olist-elt.olist_silver.order_payments_silver`  AS t1
LEFT JOIN `projeto-olist-elt.olist_silver.orders_silver` t2
ON t1.order_id = t2.order_id
