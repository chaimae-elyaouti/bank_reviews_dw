{{ config(materialized='table') }}
WITH base_reviews AS (
    SELECT * FROM {{ ref('stg_reviews') }}
)
SELECT
    *,
    CASE 
        WHEN rating >= 4 THEN 'Positive'
        WHEN rating <= 2 THEN 'Negative'
        ELSE 'Neutral'
    END as sentiment_label
FROM base_reviews