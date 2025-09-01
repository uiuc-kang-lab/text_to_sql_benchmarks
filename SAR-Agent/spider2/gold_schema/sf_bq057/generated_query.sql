-- Step 1 : Build 2021 transaction base and flag likely CoinJoin txs
--   • Exclude coinbase transactions ("is_coinbase" = FALSE)
--   • Add heuristic CoinJoin flag: ≥10 inputs AND ≥10 outputs
WITH "base_2021" AS (
    SELECT  
        "block_timestamp_month"                                            AS "block_timestamp_month" ,
        EXTRACT(MONTH FROM "block_timestamp_month")                        AS "month_num",          -- numeric month 1-12
        "input_value"                                                      AS "input_value",         -- satoshis in inputs
        "output_value"                                                     AS "output_value",        -- satoshis in outputs
        "input_count"                                                      AS "input_count",         -- #inputs
        "output_count"                                                     AS "output_count",        -- #outputs
        CASE WHEN "input_count" >= 10 AND "output_count" >= 10 
             THEN TRUE 
             ELSE FALSE END                                                AS "is_coinjoin"           -- heuristic flag
    FROM   "CRYPTO"."CRYPTO_BITCOIN"."TRANSACTIONS"
    WHERE  EXTRACT(YEAR FROM "block_timestamp_month") = 2021
      AND  "is_coinbase" = FALSE           -- exclude coinbase txs
)

-- Preview results before aggregation
SELECT *
FROM   "base_2021";