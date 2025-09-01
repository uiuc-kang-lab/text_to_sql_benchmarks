-- Final Query : Average reputation and badge count by completed membership years (users who joined on or before 2021-10-01)
WITH 
"users_with_years" AS (
    -- Convert user creation_date (micro-seconds) and keep users whose join date ≤ 2021-10-01
    SELECT  
        "id"                                                      AS "user_id",
        "reputation"                                              AS "reputation",
        TO_DATE( TO_TIMESTAMP_NTZ( "creation_date" / 1000000 ) )  AS "creation_date",
        -- calendar-year difference
        DATEDIFF(
            year,
            TO_DATE( TO_TIMESTAMP_NTZ( "creation_date" / 1000000 ) ),
            DATE '2021-10-01'
        )                                                         AS "raw_years",
        -- completed years only
        CASE 
            WHEN DATEADD(
                     year,
                     DATEDIFF(year, TO_DATE(TO_TIMESTAMP_NTZ("creation_date" / 1000000)), DATE '2021-10-01'),
                     TO_DATE(TO_TIMESTAMP_NTZ("creation_date" / 1000000))
                 ) > DATE '2021-10-01' THEN 
                 DATEDIFF(year, TO_DATE(TO_TIMESTAMP_NTZ("creation_date" / 1000000)), DATE '2021-10-01') - 1
            ELSE 
                 DATEDIFF(year, TO_DATE(TO_TIMESTAMP_NTZ("creation_date" / 1000000)), DATE '2021-10-01')
        END                                                       AS "membership_years"
    FROM STACKOVERFLOW.STACKOVERFLOW.USERS
    WHERE TO_DATE( TO_TIMESTAMP_NTZ( "creation_date" / 1000000 ) ) <= DATE '2021-10-01'
),
-----------------------------------------------------------
"badge_counts" AS (
    -- Count badges earned on or before 2021-10-01 (BADGES.date is micro-seconds)
    SELECT 
        "user_id"                               AS "user_id",
        COUNT(*)                                AS "badge_count"
    FROM STACKOVERFLOW.STACKOVERFLOW.BADGES
    WHERE TO_DATE( TO_TIMESTAMP_NTZ( "date" / 1000000 ) ) <= DATE '2021-10-01'
    GROUP BY "user_id"
),
-----------------------------------------------------------
"users_plus" AS (
    -- Combine users and their badge counts (missing → 0)
    SELECT 
        u.*,
        COALESCE(b."badge_count", 0)           AS "badge_count"
    FROM "users_with_years" u
    LEFT JOIN "badge_counts" b
           ON u."user_id" = b."user_id"
)
-----------------------------------------------------------
SELECT 
    "membership_years",
    COUNT(*)                                    AS "user_count",
    AVG("reputation")                          AS "avg_reputation",
    AVG("badge_count")                         AS "avg_badge_count"
FROM "users_plus"
GROUP BY "membership_years"
ORDER BY "membership_years";