{{ config(materialized='table') }}

WITH raw_names AS (
    SELECT DISTINCT bank_name
    FROM {{ ref('stg_reviews') }}
),

standardized_banks AS (
    SELECT 
        bank_name as original_name,
        CASE 
            WHEN UPPER(bank_name) LIKE '%CIH%' THEN 'CIH BANK'
            WHEN UPPER(bank_name) LIKE '%ATTIJARI%' THEN 'ATTIJARIWAFA BANK'
            WHEN UPPER(bank_name) LIKE '%POPULAIRE%' THEN 'BANQUE POPULAIRE'
            WHEN UPPER(bank_name) LIKE '%UMNIA%' THEN 'UMNIA BANK'
            WHEN UPPER(bank_name) LIKE '%CREDIT POPULAIRE%' THEN 'BANQUE POPULAIRE'
            ELSE UPPER(bank_name)
        END as clean_bank_name
    FROM raw_names
)

SELECT
    -- L'ID est généré sur le nom PROPRE, donc CIH et CIH BANK auront le même ID !
    MD5(clean_bank_name) as bank_key,
    clean_bank_name as bank_name
FROM standardized_banks
GROUP BY 1, 2