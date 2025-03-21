{% macro delete_database(database_name,project_id='') %}
  {{ adapter.dispatch('delete_database')(database_name) }}
{% endmacro %}

{% macro snowflake__delete_database(database_name,project_id='') %}    
    {{ log("Drop Database: " ~ database_name, info=True) }}
    {% do run_query("DROP DATABASE IF EXISTS " ~ database_name) %}
{% endmacro %}


{% macro bigquery__delete_database(database_name,project_id) %}
    -- Fetch all view names in the dataset
    {% set view_query %}
  SELECT table_name
  FROM `{{ project_id }}.{{ dataset_name }}.INFORMATION_SCHEMA.TABLES`
  where table_type = 'VIEW'
    {% endset %}

    {% set view_list = run_query(view_query) %}

    -- Loop through the tables and drop them
    {% for view in view_list %}
        {% if view['table_name'] is not none %}
            {{ log("Drop View: " ~ view['table_name'], info=True) }}
            {% do run_query("DROP VIEW `" ~ project_id ~ "." ~ dataset_name ~ "." ~ view['table_name'] ~ "`") %}
        {% endif %}
    {% endfor %}

    -- Fetch all table names in the dataset
    {% set tables_query %}
  SELECT table_name
  FROM `{{ project_id }}.{{ dataset_name }}.INFORMATION_SCHEMA.TABLES`
  where table_type like '%TABLE'
    {% endset %}

    {% set table_list = run_query(tables_query) %}

    {% for table in table_list %}
        {{ log("Table: " ~ table['table_name'], info=True) }}
    {% endfor %}

    -- Loop through the tables and drop them
    {% for table in table_list %}
        {% if table['table_name'] is not none %}
            {{ log("Drop Table: " ~ table['table_name'], info=True) }}
            {% do run_query("DROP TABLE `" ~ project_id ~ "." ~ dataset_name ~ "." ~ table['table_name'] ~ "`") %}
        {% endif %}
    {% endfor %}

    -- Drop the dataset
    {{ log("Drop Schema: " ~ project_id ~ "." ~ dataset_name, info=True) }}

    {% do run_query("DROP SCHEMA `" ~ project_id ~ "." ~ dataset_name ~ "`") %}

{% endmacro %}
