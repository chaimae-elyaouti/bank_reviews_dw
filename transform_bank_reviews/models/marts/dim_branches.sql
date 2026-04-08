{{ config(materialized='table') }}

WITH unique_branches AS (
    SELECT DISTINCT 
        bank_name,
        branch_address
    FROM {{ ref('stg_reviews') }}
),

clean_branches AS (
    SELECT
        MD5(branch_address) as branch_key,
        
        CASE 
            WHEN UPPER(bank_name) LIKE '%CIH%' THEN 'CIH BANK'
            WHEN UPPER(bank_name) LIKE '%ATTIJARI%' THEN 'ATTIJARIWAFA BANK'
            WHEN UPPER(bank_name) LIKE '%POPULAIRE%' THEN 'BANQUE POPULAIRE'
            WHEN UPPER(bank_name) LIKE '%UMNIA%' THEN 'UMNIA BANK'
            ELSE UPPER(bank_name)
        END as bank_name,
        
        branch_address,
        
        split_part(branch_address, ',', 1) as branch_name,
        
        TRIM(split_part(branch_address, ',', 3)) as city
    FROM unique_branches
)

SELECT * FROM clean_branches