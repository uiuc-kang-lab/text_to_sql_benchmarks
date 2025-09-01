-- FINAL QUERY ───────────────────────────────────────────────────────────
-- 1) Locate the U.S. patent that has the greatest number of BACKWARD
--    citations whose cited-patent application date lies within the
--    one-year period preceding the citing patent’s own application date.
-- 2) For that patent, count the FORWARD citations it receives from patents
--    whose application date falls within one year after (or on) its own
--    application date.
--
-- Result:  one row – the focal patent_id plus its forward_cnt_1yr value.
-----------------------------------------------------------------------------
WITH 
/*==========================================================================
   Earliest application date for ALL patents (any country)
  =========================================================================*/
"all_patents_appdate" AS (
    SELECT
        a."patent_id"                              AS "patent_id",
        MIN(TRY_TO_DATE(a."date", 'YYYY-MM-DD')) AS "app_date"
    FROM PATENTSVIEW.PATENTSVIEW."APPLICATION" a
    WHERE TRY_TO_DATE(a."date", 'YYYY-MM-DD') IS NOT NULL
    GROUP BY a."patent_id"
),
/*==========================================================================
   Earliest application date for U.S. patents – these will be the *citing*
   patents when determining backward citations.
  =========================================================================*/
"us_patents_appdate" AS (
    SELECT
        a."patent_id"                              AS "patent_id",
        MIN(TRY_TO_DATE(a."date", 'YYYY-MM-DD')) AS "app_date"
    FROM PATENTSVIEW.PATENTSVIEW."APPLICATION" a
    WHERE a."country" = 'US'
      AND TRY_TO_DATE(a."date", 'YYYY-MM-DD') IS NOT NULL
    GROUP BY a."patent_id"
),
/*==========================================================================
   Backward citations within 1-year PRIOR window
  =========================================================================*/
"backward_citations_1yr" AS (
    SELECT
        c."patent_id"  AS "citing_patent_id",   -- U.S. patent
        c."citation_id" AS "cited_patent_id"    -- prior-art patent
    FROM PATENTSVIEW.PATENTSVIEW."USPATENTCITATION" c
    JOIN "us_patents_appdate"   cp ON cp."patent_id" = c."patent_id"
    JOIN "all_patents_appdate" sp ON sp."patent_id" = c."citation_id"
    WHERE sp."app_date" BETWEEN DATEADD(day,-365, cp."app_date")
                             AND cp."app_date"
),
"backward_counts" AS (
    SELECT
        bc."citing_patent_id" AS "patent_id",
        COUNT(*)               AS "backward_cnt_1yr"
    FROM "backward_citations_1yr" bc
    GROUP BY bc."citing_patent_id"
),
"top_backward_patent" AS (
    SELECT
        bc."patent_id",
        bc."backward_cnt_1yr"
    FROM "backward_counts" bc
    ORDER BY bc."backward_cnt_1yr" DESC, bc."patent_id" ASC
    LIMIT 1
),
/*==========================================================================
   Fetch focal patent’s application date
  =========================================================================*/
"focal_patent_appdate" AS (
    SELECT
        tbp."patent_id"  AS "patent_id",
        apa."app_date"   AS "app_date"
    FROM "top_backward_patent" tbp
    JOIN "all_patents_appdate" apa ON apa."patent_id" = tbp."patent_id"
),
/*==========================================================================
   Forward citations RECEIVED within 1-year AFTER focal patent’s app date
  =========================================================================*/
"forward_citations_1yr" AS (
    SELECT
        c."patent_id"   AS "citing_patent_id",
        c."citation_id" AS "focal_patent_id"
    FROM PATENTSVIEW.PATENTSVIEW."USPATENTCITATION" c
    JOIN "focal_patent_appdate" fp           ON fp."patent_id" = c."citation_id"
    JOIN "all_patents_appdate"     ap_citing ON ap_citing."patent_id" = c."patent_id"
    WHERE ap_citing."app_date" BETWEEN fp."app_date" 
                                   AND DATEADD(day, 365, fp."app_date")
),
/*==========================================================================
   Aggregate forward citations
  =========================================================================*/
"forward_count" AS (
    SELECT
        fp."patent_id"                  AS "patent_id",
        COUNT(fc."citing_patent_id")   AS "forward_cnt_1yr"
    FROM "focal_patent_appdate" fp
    LEFT JOIN "forward_citations_1yr" fc
           ON fc."focal_patent_id" = fp."patent_id"
    GROUP BY fp."patent_id"
)
/*==========================================================================
   Final output
  =========================================================================*/
SELECT *
FROM "forward_count";