{% macro normalize_last_seen_at(last_seen_at, collection_at) %}
    case
        when last_seen_at is null then collection_at
        when last_seen_at = TIMESTAMP '1970-01-01 00:00:00' then null
        else last_seen_at
    end
{% endmacro %}
