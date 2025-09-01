-- Step 1: Identify studies that satisfy both business rules
--   a) SegmentedPropertyTypeCodeSequence contains the code ‘15825003’
--   b) Study belongs to the ‘Community’ or ‘nsclc_radiomics’ collections
-- The CTE returns one row per qualifying StudyInstanceUID.

WITH filtered_studies AS (
    SELECT  
        "StudyInstanceUID"
    FROM "IDC"."IDC_V17"."DICOM_PIVOT"
    WHERE 
        -- Segmented property type condition (the code may be embedded in a delimited list)
        "SegmentedPropertyTypeCodeSequence" ILIKE '%15825003%'
        
        -- Desired collections
        AND "collection_id" IN ('Community', 'nsclc_radiomics')
    GROUP BY "StudyInstanceUID"   -- deduplicate
)
-- We will add subsequent CTEs/queries after user confirmation.