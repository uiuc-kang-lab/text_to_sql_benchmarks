-- Diagnostic query confirmed rows exist when filtering only on address.
-- We will consider this sub-query CLOSED and proceed (next step will re-introduce
-- the selector logic and inspect the input field to verify the function
-- selectors).

WITH "usdc_address_only" AS (
    SELECT  
        "hash"               AS "tx_hash"      ,
        "block_timestamp"    AS "raw_block_ts" ,
        LEFT("input", 10)     AS "input_prefix" ,
        "input"              AS "full_input"
    FROM   CRYPTO.CRYPTO_ETHEREUM.TRANSACTIONS
    WHERE  LOWER("to_address") = '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'
    LIMIT  10
)
SELECT *
FROM   "usdc_address_only";