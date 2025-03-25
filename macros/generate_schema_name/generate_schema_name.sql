{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- set staging_fqn = var('staging_fqn','_stg') -%}    
    {%- set package_name = var('package_name','tikal_dbt') -%}    
    {%- if node["resource_type"]=="model" -%}
        {% set dir_path = node["path"].split('/') %}
        {% set model_type = dir_path[1] %}
        
        {%- if node["package_name"]==package_name -%}
            {% set domain = node["fqn"][1] %}
            {%- if staging_fqn in node["fqn"] -%}
                {% set position = node["fqn"].index(staging_fqn)-1 %}
                {%- if position > 1 -%}
                    {% set domain = node["fqn"][position-1] ~ "_" ~ node["fqn"][position] %}
                {%- else -%}
                    {% set domain = node["fqn"][position] %}
                {% endif %}            
            {% endif %}            
            {{ domain | trim }}
        {%- else -%}
            {{ custom_schema_name | trim }}
        {% endif %}
    {%- else -%}
        {{ custom_schema_name | trim }}
    {% endif %}
{%- endmacro %}
