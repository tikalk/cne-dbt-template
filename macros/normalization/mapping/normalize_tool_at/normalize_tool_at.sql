{% macro normalize_tool_at(tool_at, collection_at) %}
    case
        when tool_at is null then collection_at
        else tool_at
    end
{% endmacro %}
