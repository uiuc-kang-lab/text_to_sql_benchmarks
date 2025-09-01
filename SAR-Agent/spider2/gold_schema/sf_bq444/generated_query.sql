-- Final Query: Earliest five Mint or Burn events for the specified contract
WITH "filtered_logs" AS (
    -- Filter logs by contract address and event-signature topics
    SELECT
        "block_timestamp",               -- Unix epoch (seconds)
        "block_number",                 -- Block height
        "transaction_hash",             -- Tx hash that emitted the log
        "topics"[0]::string AS "topic0" -- First topic = event signature
    FROM CRYPTO.CRYPTO_ETHEREUM.LOGS
    WHERE lower("address") = '0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8'
      AND "topics"[0]::string IN (
            '0x7a53080ba414158be7ec69b987b5fb7d07dee101fe85488f0853ae16239d0bde', -- Mint
            '0x0c396cd989a39f4459b5fa1aed6a9a8dcdbc45908acfd67e028cd568da98982c'  -- Burn
          )
),
"labeled_events" AS (
    -- Label each row as Mint or Burn
    SELECT
        "block_timestamp",
        "block_number",
        "transaction_hash",
        CASE
            WHEN "topic0" = '0x7a53080ba414158be7ec69b987b5fb7d07dee101fe85488f0853ae16239d0bde' THEN 'Mint'
            WHEN "topic0" = '0x0c396cd989a39f4459b5fa1aed6a9a8dcdbc45908acfd67e028cd568da98982c' THEN 'Burn'
            ELSE 'Unknown'
        END AS "event_type"
    FROM "filtered_logs"
)
SELECT
    "block_timestamp",
    "block_number",
    "transaction_hash",
    "event_type"
FROM "labeled_events"
ORDER BY "block_timestamp" ASC
LIMIT 5;