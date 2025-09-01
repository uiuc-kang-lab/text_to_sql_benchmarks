-- Step 1 : Identify all TCGA-BLCA cases that harbor a CDKN2A somatic mutation
WITH "cdkn2a_mutated_cases" AS (
    SELECT DISTINCT
           "case_barcode"      AS "case_barcode"      -- TCGA case identifier
    FROM   "TCGA"."TCGA_VERSIONED"."SOMATIC_MUTATION_HG19_DCC_2017_02"
    WHERE  "project_short_name" = 'TCGA-BLCA'          -- restrict to bladder cancer project
      AND  "Hugo_Symbol"        = 'CDKN2A'             -- keep only CDKN2A mutations
)
-- Preview the list of mutated cases
SELECT *
FROM   "cdkn2a_mutated_cases";