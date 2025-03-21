{% macro generate_database_name(custom_database_name=none, node=none) -%}
    {%- set marts_extension = var('marts_extension','_marts') -%}    
    {%- set staging_extension = var('staging_extension','_stg') -%}    

    {%- set default_database = target.database -%}    
    {%- if node  and node["package_name"] == "tikal_dbt" -%}
        {%- if "gold" in node["fqn"] -%}
            {% set modified_database = default_database ~ marts_extension %}            
        {%- elif "silver" in node["fqn"] -%}
            {% set modified_database = default_database ~ staging_extension %}
        {% else %}
            {% set modified_database = default_database %}
        {%- endif -%}                

        {{ modified_database  }}
    {% else %}
        {%- if custom_database_name is none -%}
            {{ default_database }}
        {%- else -%}
            {{ custom_database_name | trim }}
        {%- endif -%}

    {%- endif -%}
    
{%- endmacro %}
