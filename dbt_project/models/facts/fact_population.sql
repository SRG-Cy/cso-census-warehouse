SELECT
    bp.county_code,
    bp.census_year,
    bp.county_name,
    bp.province,
    bp.population,
    -- population change vs previous census
    bp.population - LAG(bp.population) OVER (
        PARTITION BY bp.county_name
        ORDER BY bp.census_year
    ) AS population_change,
    -- percentage change vs previous census
    ROUND(
        CAST(
            (bp.population - LAG(bp.population) OVER (
                PARTITION BY bp.county_name
                ORDER BY bp.census_year
            )) * 100.0 / NULLIF(LAG(bp.population) OVER (
                PARTITION BY bp.county_name
                ORDER BY bp.census_year
            ), 0) AS NUMERIC
        ), 2
    ) AS pct_change
FROM {{ source('cso_bronze', 'bronze_population') }} bp
ORDER BY bp.county_name, bp.census_year