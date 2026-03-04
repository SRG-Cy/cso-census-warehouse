SELECT DISTINCT
    census_year,
    FLOOR(census_year / 100) + 1    AS century,
    CASE WHEN census_year >= 1990
         THEN TRUE ELSE FALSE
    END                             AS is_modern_era,
    CASE WHEN census_year >= 2000
         THEN TRUE ELSE FALSE
    END                             AS is_21st_century
FROM {{ source('cso_bronze', 'bronze_population') }}
ORDER BY census_year