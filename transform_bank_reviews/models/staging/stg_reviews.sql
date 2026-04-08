{{ config(materialized='table') }}



WITH raw_data AS (

    SELECT * FROM public.staging_bank_reviews

)



SELECT

    review_id,

    UPPER(bank_name) as bank_name,  

    branch_address,    

    reviewer_name as user_name,

    stars as rating,

    review_text,

    published_date,

    scraped_at

FROM raw_data

WHERE review_text IS NOT NULL AND review_text != 'Pas de texte'
