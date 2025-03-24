
/*
in production table name will be without [domain]__
*/
WITH staging AS (

    SELECT * FROM {{ ref('users_stg__all_users') }}

)

SELECT * FROM staging
