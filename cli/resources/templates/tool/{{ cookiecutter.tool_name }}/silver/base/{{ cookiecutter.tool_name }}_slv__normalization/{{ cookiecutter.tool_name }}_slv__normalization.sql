{% raw %}


WITH source AS (

    SELECT * FROM {{ source('<SOURCE_NAME>', '<TABLE_NAME>') }}

), <MODEL_NAME> AS (

    SELECT <COLUMN_LIST>
    FROM source

)

SELECT * 
FROM <MODEL_NAME>
{% endraw %}
