{% macro get_os_display_name(platform_name, os_dist, os_version) %}
    case
        when {{ platform_name }} is null then ''
        when {{ os_dist }} is null then {{ platform_name }}
        when {{ platform_name }} != 'Linux' then {{ os_dist }}
        when {{ platform_name }} = 'Linux' then
            case
                when {{ os_dist }} = 'Ubuntu' then concat('Ubuntu ', coalesce(regexp_substr({{ os_version }}, '(((2|1)[0-9]{1}\.[0-9]{2}))', 1, 1, 'i', 1), ''))
                when {{ os_dist }} = 'CentOS' then concat('CentOS ', coalesce(regexp_substr({{ os_version }}, '((\\d{1,2}(\.\\d+){0,2}))', 1, 1, 'i', 1), ''))
                when {{ os_dist }} = 'SLES' then concat('SLES ', coalesce(regexp_substr({{ os_version }}, '((\\d{1,2}(\.\\d+){0,2}))', 1, 1, 'i', 1), ''))
                when {{ os_dist }} = 'Fedora' then concat('Fedora ', coalesce(regexp_substr({{ os_version }}, '((\\d{1,2}(\.\\d+){0,2}))', 1, 1, 'i', 1), ''))
                when {{ os_dist }} = 'RHEL' then concat('RHEL ', coalesce(regexp_substr({{ os_version }}, '((\\d{1,2}(\.\\d+){0,2}))', 1, 1, 'i', 1), ''))
                when {{ os_dist }} = 'Debian' then concat('Debian ', coalesce(regexp_substr({{ os_version }}, '((\\d{1,2}(\.\\d+){0,2}))', 1, 1, 'i', 1), ''))
            end
    end
{% endmacro %}
