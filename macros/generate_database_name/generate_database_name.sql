{% macro generate_database_name(custom_database_name=none, node=none) -%}
    
    {%- set enable_separate_db = var('enable_separate_db',False) -%}    
    {%- set default_database = target.database -%}    
    {%- if enable_separate_db -%}
        {%- set marts_extension = var('marts_extension','_marts') -%}    
        {%- set staging_extension = var('staging_extension','_stg') -%}    
        {%- set package_name = var('tikal_dbt','tikal_dbt') -%}    
        {%- set marts_fqn = var('marts_fqn','marts') -%}    
        {%- set staging_fqn = var('staging_fqn','staging') -%}        

        {%- if node  and node["package_name"] == package_name -%}
            {%- if marts_fqn in node["fqn"] -%}
                {% set modified_database = default_database ~ marts_extension %}            
            {%- elif staging_fqn in node["fqn"] -%}
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
    {% else %}
        {%- if custom_database_name is none -%}

            {{ default_database }}

        {%- else -%}

            {{ custom_database_name | trim }}

        {%- endif -%}
        
    {%- endif -%}    
{%- endmacro %}
