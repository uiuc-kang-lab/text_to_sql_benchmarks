-- Final query: yearly comparison of average output values, granular vs consolidated
WITH "outputs_by_year" AS (
    SELECT 
        -- Convert micro-second epoch to TIMESTAMP and extract calendar year
        DATE_PART('year', TO_TIMESTAMP_LTZ("block_timestamp" / 1000000)) AS "year",
        -- Average value (satoshis) of every individual output in the year
        AVG("value") AS "avg_output_value_outputs"
    FROM CRYPTO.CRYPTO_BITCOIN.OUTPUTS
    GROUP BY 1
),

"txn_by_year" AS (
    SELECT
        DATE_PART('year', TO_TIMESTAMP_LTZ("block_timestamp" / 1000000)) AS "year",
        SUM("output_value")                                  AS "sum_output_value",
        SUM("output_count")                                  AS "sum_output_count",
        SUM("output_value") / NULLIF(SUM("output_count"),0) AS "avg_output_value_txn"
    FROM CRYPTO.CRYPTO_BITCOIN.TRANSACTIONS
    GROUP BY 1
),

"diff_by_year" AS (
    SELECT  
        ob."year"                                 AS "year",
        ob."avg_output_value_outputs"             AS "avg_output_value_outputs",
        t."avg_output_value_txn"                  AS "avg_output_value_txn",
        ob."avg_output_value_outputs" -
        t."avg_output_value_txn"                  AS "avg_output_value_difference"
    FROM "outputs_by_year" ob
    INNER JOIN "txn_by_year"   t   ON ob."year" = t."year"
)

-- Return the annual differences for all years common to both calculations
SELECT 
    "year",
    "avg_output_value_outputs",
    "avg_output_value_txn",
    "avg_output_value_difference"
FROM "diff_by_year"
ORDER BY "year";