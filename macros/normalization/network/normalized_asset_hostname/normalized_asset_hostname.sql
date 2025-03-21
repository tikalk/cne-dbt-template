{% macro normalized_asset_hostname(n, lower_case=true, remove_special_chars=true) %}
    (
        REGEXP_REPLACE(
            {% if remove_special_chars %}
                REPLACE(REGEXP_REPLACE(lower(TRIM({{ n }})), '[\'`’"]', ''), ' ', '-')
            {% else %}
                TRIM({{ n }})
            {% endif %}
            , '\.local$|\\.lan$', ''
        )
    )

{% endmacro %}
