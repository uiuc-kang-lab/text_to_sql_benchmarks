-- Step 1:  Build the set of repositories that
--         • contain the programming language “Shell”
--         • use the “apache-2.0” license
--
-- NOTE on language detection
-- -------------------------
-- The LANGUAGES."language" column is a VARIANT that stores a JSON object
-- whose keys are language names (e.g. { "Shell" : 18342 , "Python" : 9911 …}).
-- The simplest and most reliable way to detect the presence of a key is to
-- use the VARIANT key-lookup operator :  "column" : "key" .  If the key is
-- present, the expression is non-NULL.

WITH shell_repos AS (
    /* Repositories that have any bytes attributed to the Shell language */
    SELECT DISTINCT
           "lr"."repo_name"
    FROM   "GITHUB_REPOS"."GITHUB_REPOS"."LANGUAGES" AS "lr"
    WHERE  "lr"."language" : "Shell" IS NOT NULL  -- key-lookup returns value or NULL
),
licensed_repos AS (
    /* Repositories whose license string exactly matches 'apache-2.0' */
    SELECT DISTINCT
           "lic"."repo_name"
    FROM   "GITHUB_REPOS"."GITHUB_REPOS"."LICENSES" AS "lic"
    WHERE  "lic"."license" = 'apache-2.0'
)

SELECT DISTINCT
       "s"."repo_name"
FROM   shell_repos     AS "s"
JOIN   licensed_repos  AS "l"
  ON   "s"."repo_name" = "l"."repo_name";