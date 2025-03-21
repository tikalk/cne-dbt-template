{% macro normalize_mac_address(mac_add) %}
    CASE
        WHEN REGEXP_LIKE(
            -- Remove non-hexadecimal characters and standardize the format
            REGEXP_REPLACE(LOWER(TRIM({{mac_add}})), '[^0-9a-f]', ''),
            -- Validate MAC address (12 hexadecimal digits)
            '^[0-9a-f]{12}$'
        )
        THEN
            -- Reformat to standard MAC address notation (e.g., xx:xx:xx:xx:xx:xx)
            RTRIM(
                    REGEXP_REPLACE(
                        REGEXP_REPLACE(LOWER(TRIM({{mac_add}})), '[^0-9a-f]', ''),
                        '(.{2})', '\\1:'
                    ),
                    ':'
                )
        ELSE NULL
    END
{% endmacro %}
