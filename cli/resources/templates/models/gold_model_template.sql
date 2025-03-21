{{
  config(
    cluster_by=['org_id', 'job_id']
  )
}}

/*
in production table name will be without [domain]__
*/
WITH staging AS (

    SELECT * FROM {{ ref('<MODEL_NAME>') }}

), <MODEL_NAME> AS (

    SELECT <COLUMN_LIST>
    FROM staging

)

SELECT * FROM <MODEL_NAME>
