{% macro get_platform_name(os_type) %}
    CASE
        WHEN os_type = 'OS_WINDOWS' THEN 'Windows'
        WHEN os_type = 'OS_MACOS' THEN 'macOS'
        WHEN os_type = 'OS_LINUX' THEN 'Linux'
        WHEN os_type = 'OS_EMBEDDED' THEN 'Embedded'
        ELSE NULL
    END
{% endmacro %}
