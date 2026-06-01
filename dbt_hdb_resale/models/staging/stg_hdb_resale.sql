{{ config(materialized='table') }}

WITH raw_source AS (
    SELECT
        id,
        PARSE_DATE('%Y-%m', month) AS resale_month,
        town,
        flat_type,
        block,
        street_name,
        storey_range,
        CAST(floor_area_sqm AS FLOAT64) AS floor_area_sqm,
        flat_model,
        lease_commence_date,
        remaining_lease,
        -- Extract years, default to 0 if not found, multiply by 12
        COALESCE(CAST(REGEXP_EXTRACT(remaining_lease, r'(\d+) year') AS INT64), 0) * 12 +
        -- Extract months, default to 0 if not found
        COALESCE(CAST(REGEXP_EXTRACT(remaining_lease, r'(\d+) month') AS INT64), 0) 
        AS remaining_lease_months,
        CAST(resale_price AS FLOAT64) AS resale_price,
        -- Keep your timestamp column to identify the freshest record
        updated_at
    -- Changed to underscore to avoid BigQuery compilation bugs
    FROM {{ source('hdb_resale_source', 'public_hdb_resale_flat_prices_e2e') }}
),

deduplicated AS (
    SELECT 
        *,
        -- Assigns 1 to the most recent record per individual ID
        ROW_NUMBER() OVER (
            PARTITION BY id 
            ORDER BY updated_at DESC
        ) AS row_num
    FROM raw_source
)

SELECT
    id,
    resale_month,
    town,
    flat_type,
    block,
    street_name,
    storey_range,
    floor_area_sqm,
    flat_model,
    lease_commence_date,
    remaining_lease,
    remaining_lease_months,
    resale_price,
    resale_price / floor_area_sqm AS price_per_sqm
FROM deduplicated
-- Filters out any duplicate records pulled by your replication tool
WHERE row_num = 1