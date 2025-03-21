{% macro get_attributes(os_type, endpoint_type, system_product_name, internet_exposure) %}
    case
        when os_type != 'OS_LINUX' and endpoint_type is not null
            then case
                when endpoint_type = 'Server' then 'SERVER'
                when endpoint_type = 'Domain Controller' then 'SERVER'
                when endpoint_type = 'Workstation' then 'WORKSTATION'
                when endpoint_type = 'Virtual' then 'WORKSTATION'
                when endpoint_type = 'internet_exposure' then 'INTERNET_FACING'
            end
        when os_type = 'OS_WINDOWS' and system_product_name regexp '^(vmware|vbox|qemu|parallels|virtual)'
            then 'WORKSTATION'
        when internet_exposure = 'Yes' then 'INTERNET_FACING'
    end
{% endmacro %}
