{% macro normalized_asset_name(n, lower_case=false, remove_special_chars=false) %}
    case
        when {{n}} in ('', 'localhost', NULL, 'nan') then 'Unknown'
        else REGEXP_REPLACE({{ n }}, '\.local$|\.lan$', '')
    end
{% endmacro %}
