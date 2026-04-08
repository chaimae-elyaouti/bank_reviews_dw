{{ config(materialized='table') }}

WITH base_reviews AS (
    SELECT * FROM {{ ref('stg_reviews') }}
)

SELECT
    *,
    CAST(NULL AS VARCHAR) as language,
    CASE 
        WHEN rating >= 4 THEN 'Positive'
        WHEN rating <= 2 THEN 'Negative'
        ELSE 'Neutral'
    END as sentiment_label,
    CAST(NULL AS INTEGER) as topic_id,
    CAST(NULL AS VARCHAR) as topic_label
FROM base_reviews