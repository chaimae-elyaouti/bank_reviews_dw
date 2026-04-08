{{ config(materialized='table') }}

SELECT
    r.review_id,
    
    MD5(
        CASE 
            WHEN UPPER(r.bank_name) LIKE '%CIH%' THEN 'CIH BANK'
            WHEN UPPER(r.bank_name) LIKE '%ATTIJARI%' THEN 'ATTIJARIWAFA BANK'
            WHEN UPPER(r.bank_name) LIKE '%POPULAIRE%' THEN 'BANQUE POPULAIRE'
            WHEN UPPER(r.bank_name) LIKE '%UMNIA%' THEN 'UMNIA BANK'
            ELSE UPPER(r.bank_name)
        END
    ) as bank_key,

    MD5(r.branch_address) as branch_key,

    r.rating as stars,
    r.published_date,
    
    r.sentiment_label,
    r.topic_id,
    r.topic_label,
    
    r.review_text

FROM {{ ref('stg_enriched_reviews') }} r