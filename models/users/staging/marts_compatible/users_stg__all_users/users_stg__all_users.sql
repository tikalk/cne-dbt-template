
/*
in production table name will be without [domain]_slv__
*/
WITH source AS (

    SELECT * FROM {{ ref('users_stg__user_cast') }}

)

SELECT * 
FROM source
