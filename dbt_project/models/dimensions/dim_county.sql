SELECT DISTINCT
    county_code,
    county_name,
    province,
    CASE province
        WHEN 'Leinster' THEN 1
        WHEN 'Munster'  THEN 2
        WHEN 'Connacht' THEN 3
        WHEN 'Ulster'   THEN 4
    END AS province_order
FROM {{ source('cso_bronze', 'bronze_population') }}
ORDER BY county_name