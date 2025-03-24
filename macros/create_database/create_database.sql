{% macro create_database(database_name) %}
  {{ adapter.dispatch('create_database')(database_name) }}
{% endmacro %}

{% macro snowflake__create_database(database_name) %}    
    {{ log("Create Database: " ~ database_name, info=True) }}
    {% do run_query("CREATE DATABASE IF NOT EXISTS " ~ database_name) %}
{% endmacro %}

{% macro bigquery__create_database(database_name) %}    
    {{ log("Create Database: " ~ database_name, info=True) }}
    {% do run_query("CREATE SCHEMA " ~ database_name ~ "OPTIONS (location = 'US')") %}
{% endmacro %}
