
/*
in production table name will be without [domain]_slv__
*/
WITH source AS (

    SELECT * FROM {{ ref('<MODEL_NAME>') }}

), <MODEL_NAME> AS (

    SELECT <COLUMN_LIST>
    FROM source

)

SELECT * 
FROM <MODEL_NAME>
