{% macro get_os_build_version(os_dist, os_version) %}

    case
        when  os_dist = 'Windows Server 2022' or  os_dist  = 'Windows Server 2019' or  os_dist  = 'Windows Server 2016'
            or  os_dist  = 'Windows Server 2012 R2' or  os_dist  = 'Windows Server 2012' or  os_dist  = 'Windows Server 2008 R2' or  os_dist  = 'Windows Server 2008'
            or  os_dist  = 'Windows Server 2003 R2' or  os_dist  = 'Windows Server 2003' or  os_dist  = 'Windows Server' or  os_dist  = 'Windows 11'
            or  os_dist  = 'Windows 10' or  os_dist  = 'Windows 8.1' or  os_dist  = 'Windows 8'
            or  os_dist  = 'Windows 7' or  os_dist  = 'Windows Vista' or  os_dist  = 'Windows XP' or  os_dist  = 'Windows'
        then coalesce( regexp_substr( os_version , '((\\d{1,2}(\.0(\.\\d{4,5}(\.\\d+)?)?)?))', 1, 1, 'i', 1), '')
        when  os_dist  = 'Sonoma' or  os_dist  = 'Ventura' or  os_dist  = 'Monterey' or  os_dist  = 'Big Sur'
            or  os_dist  = 'Catalina' or  os_dist  = 'Mojave' or  os_dist  = 'High Sierra' or  os_dist  = 'Sierra'
        then coalesce( regexp_substr( os_version , '((\\d{1,2}[a-z]{1}\\d+[a-z]{0,1})| \\b\\d+(\.\\d+)+\\b)', 1, 1, 'i', 1), '')
        when  os_dist  = 'Ubuntu'
        then coalesce( regexp_substr( os_version , '(((2|1)[0-9]{1}\.[0-9]{2}))', 1, 1, 'i', 1), '')
        when  os_dist  = 'CentOS' or  os_dist  = 'SLES' or  os_dist  = 'Fedora' or  os_dist  = 'RHEL' or  os_dist  = 'Debian'
        then coalesce( regexp_substr( os_version , '((\\d{1,2}(\.\\d+){0,2}))', 1, 1, 'i', 1), '')
    end
{% endmacro %}
