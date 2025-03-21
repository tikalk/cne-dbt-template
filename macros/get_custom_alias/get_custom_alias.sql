{% macro generate_alias_name(custom_alias_name=none, node=none) -%}
    {%- set staging_table_part = var('staging_table_part','_stg') -%}    
    {%- if node["resource_type"]=="model" and node["package_name"]=="apex_dbt" -%}
        {%- if custom_alias_name is none -%}    
            {% set table_parts = node.name.split('__') %}
            {% set node_name = table_parts[1] %}
            {{ node.name | replace(staging_table_part, "") }} 
        {%- else -%}
            {{ custom_alias_name | trim }}
        {%- endif -%}
    {%- else -%}
        {%- if custom_alias_name -%}
            {{ custom_alias_name | trim }}

        {%- elif node.version -%}
            {{ return(node.name ~ "_v" ~ (node.version | replace(".", "_"))) }}

        {%- else -%}
            {{ node.name }}

        {%- endif -%}
    {%- endif -%}
{%- endmacro %}
