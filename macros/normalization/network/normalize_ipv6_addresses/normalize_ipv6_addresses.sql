{% macro normalize_ipv6_addresses(ipv6_add) %}
    CASE
        WHEN
            PARSE_IP({{ ipv6_add }}, 'INET') IS NOT NULL AND PARSE_IP({{ ipv6_add }}, 'INET'):family = 6
            AND PARSE_IP({{ ipv6_add }}, 'INET'):hex_ipv6 NOT BETWEEN '00000000000000000000000000000000' AND '00000000000000000000000000000001' -- ::1/128 (loopback)
            AND PARSE_IP({{ ipv6_add }}, 'INET'):hex_ipv6 NOT BETWEEN 'FE800000000000000000000000000000' AND 'FE80FFFFFFFFFFFFFFFFFFFFFFFFFFFF' -- fe80::/10 (link-local)
            AND PARSE_IP({{ ipv6_add }}, 'INET'):hex_ipv6 NOT BETWEEN 'FF000000000000000000000000000000' AND 'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF' -- ff00::/8 (multicast)
        THEN {{ ipv6_add }}
        ELSE NULL
    END
{% endmacro %}
