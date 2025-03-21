{% macro get_os_type(os_name) %}
    case
        when {{ os_name }} = 'Windows' then 'OS_WINDOWS'
        when {{ os_name }} = 'Mac' then 'OS_MACOS'
        when {{ os_name }} = 'Linux' then 'OS_LINUX'
        else 'OS_OTHER'
    end
{% endmacro %}
