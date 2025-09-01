-- Step 1: Build a list of uniquely-identified, non-binary Swift files with their copy count
WITH "swift_files" AS (
    SELECT
        f."id"            AS "file_id",          -- unique identifier of the file
        f."repo_name"     AS "repository_name",  -- repository where the file resides
        f."path"          AS "file_path",        -- full path – used for .swift filter
        c."copies"        AS "copy_count"        -- number of copies recorded for this file
    FROM   "GITHUB_REPOS"."GITHUB_REPOS"."SAMPLE_FILES"    AS f
    JOIN   "GITHUB_REPOS"."GITHUB_REPOS"."SAMPLE_CONTENTS" AS c
           ON f."id" = c."id"                              -- ensure same file
    WHERE  c."binary" = FALSE                               -- exclude binary files
      AND  LOWER(f."path") LIKE '%.swift'                    -- keep only *.swift files
)

-- Expose the intermediate result for downstream steps
SELECT *
FROM   "swift_files";