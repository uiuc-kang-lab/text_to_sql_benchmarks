-- Cumulative query (Steps 1 – 4)
-- Counts how many unique StudyInstanceUIDs belong to the four requested
-- series categories inside the QIN-PROSTATE-Repeatability collection

WITH filtered_series AS (
    SELECT  
        "StudyInstanceUID",
        "SeriesInstanceUID",
        "SeriesDescription"
    FROM  "IDC"."IDC_V17"."DICOM_ALL"
    WHERE "collection_name" = 'QIN-PROSTATE-Repeatability'
      AND (      "SeriesDescription" ILIKE '%DWI%'
            OR   "SeriesDescription" ILIKE '%ADC%'
            OR   "SeriesDescription" ILIKE '%Apparent Diffusion Coefficient%'
            OR  ("SeriesDescription" ILIKE '%T2%' AND "SeriesDescription" ILIKE '%AX%')
            OR   "SeriesDescription" ILIKE '%SEG%'
          )
),
-- keep one row per study
distinct_studies AS (
    SELECT DISTINCT "StudyInstanceUID"
    FROM   filtered_series
)
SELECT COUNT(*) AS "unique_study_count"
FROM   distinct_studies;