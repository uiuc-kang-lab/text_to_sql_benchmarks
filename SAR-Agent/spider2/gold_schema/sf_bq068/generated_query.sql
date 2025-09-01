-- FINAL QUERY: Maximum and minimum balances per address_type for March 2014
/*──────────────────────────────────────────────────────────────────────────────┐
  CTE 1: Filter transactions to March 2014                                     │
 └──────────────────────────────────────────────────────────────────────────────*/
WITH "march_2014_tx" AS (
    SELECT 
        "hash"    AS "transaction_hash",  -- unique transaction id
        "outputs" AS "outputs"              -- full outputs array
    FROM CRYPTO.CRYPTO_BITCOIN_CASH.TRANSACTIONS
    WHERE "block_timestamp_month" = '2014-03-01'::DATE
),
/*──────────────────────────────────────────────────────────────────────────────┐
  CTE 2: Flatten outputs → one row per output                                   │
 └──────────────────────────────────────────────────────────────────────────────*/
"address_outputs" AS (
    SELECT 
        mt."transaction_hash",
        ov.value:"addresses"[0]::STRING                                        AS "address",       -- first address
        COALESCE(
            ov.value:"type"::STRING,
            ov.value:"script_type"::STRING
        )                                                                       AS "address_type",  -- script / address type
        ov.value:"value"::NUMBER                                               AS "output_value"   -- satoshi amount
    FROM "march_2014_tx" mt,
         LATERAL FLATTEN(input => mt."outputs") ov
),
/*──────────────────────────────────────────────────────────────────────────────┐
  CTE 3: Aggregate to balance per (address, address_type)                       │
 └──────────────────────────────────────────────────────────────────────────────*/
"address_balances" AS (
    SELECT 
        ao."address_type",
        ao."address",
        SUM(ao."output_value") AS "balance_sats"
    FROM "address_outputs" ao
    GROUP BY ao."address_type", ao."address"
),
/*──────────────────────────────────────────────────────────────────────────────┐
  CTE 4: Max & Min balance for each address_type                                │
 └──────────────────────────────────────────────────────────────────────────────*/
"address_type_stats" AS (
    SELECT 
        ab."address_type",
        MAX(ab."balance_sats") AS "max_balance_sats",
        MIN(ab."balance_sats") AS "min_balance_sats"
    FROM "address_balances" ab
    GROUP BY ab."address_type"
)
SELECT *
FROM "address_type_stats"
ORDER BY "address_type";