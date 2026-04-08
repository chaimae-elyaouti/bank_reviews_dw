{{ config(materialized='table') }}

SELECT DISTINCT
    sentiment_label,
    CASE 
        WHEN sentiment_label = 'Positive' THEN 1
        WHEN sentiment_label = 'Neutral' THEN 2
        WHEN sentiment_label = 'Negative' THEN 3
        ELSE 4
    END as sentiment_rank
FROM {{ ref('stg_enriched_reviews') }}