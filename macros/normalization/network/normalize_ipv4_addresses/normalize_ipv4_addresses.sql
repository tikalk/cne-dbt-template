{% macro normalize_ipv4_addresses(ipv4_add) %}
    CASE
        WHEN
            REGEXP_LIKE({{ ipv4_add }}, '^(25[0-5]|2[0-4][0-9]|1?[0-9]?[0-9])(\\.(25[0-5]|2[0-4][0-9]|1?[0-9]?[0-9])){3}$')
            AND
            NOT SEARCH_IP(PARSE_IP({{ ipv4_add }}, 'INET'), '127.0.0.0/8')
            AND
            NOT SEARCH_IP(PARSE_IP({{ ipv4_add }}, 'INET'), '169.254.0.0/16')
            AND
            NOT SEARCH_IP(PARSE_IP({{ ipv4_add }}, 'INET'), '224.0.0.0/4')
        THEN {{ ipv4_add }}
        ELSE NULL
    END
{% endmacro %}
