{% macro get_os_dist(platform_name, os_version) %}
    CASE
        WHEN {{ platform_name }} = 'Windows' THEN
            CASE
                WHEN regexp_substr({{ os_version }}, '(server\\s{0,1}2022|10.0.20\\d{3})', 1, 1,'i', 0) is not null THEN 'Windows Server 2022'
                WHEN regexp_substr({{ os_version }}, '(server\\s{0,1}2019)', 1, 1,'i', 0) is not null THEN 'Windows Server 2019'
                WHEN regexp_substr({{ os_version }}, '(server\\s{0,1}2016)', 1, 1,'i', 0) is not null THEN 'Windows Server 2016'
                WHEN regexp_substr({{ os_version }}, '(server\\s{0,1}2012\\s{0,1}r2)', 1, 1,'i', 0) is not null THEN 'Windows Server 2012 R2'
                WHEN regexp_substr({{ os_version }}, '(server\\s{0,1}2012)', 1, 1,'i', 0) is not null THEN 'Windows Server 2012'
                WHEN regexp_substr({{ os_version }}, '(server\\s{0,1}2008\\s{0,1}r2)', 1, 1,'i', 0) is not null THEN 'Windows Server 2008 R2'
                WHEN regexp_substr({{ os_version }}, '(server\\s{0,1}2008)', 1, 1,'i', 0) is not null THEN 'Windows Server 2008'
                WHEN regexp_substr({{ os_version }}, '(server\\s{0,1}2003\\s{0,1}r2)', 1, 1,'i', 0) is not null THEN 'Windows Server 2003 R2'
                WHEN regexp_substr({{ os_version }}, '(server\\s{0,1}2003)', 1, 1,'i', 0) is not null THEN 'Windows Server 2003'
                WHEN regexp_substr({{ os_version }}, '(server)', 1, 1,'i', 0) is not null THEN 'Windows Server'
                WHEN regexp_substr({{ os_version }}, '(windows\\s{0,1}11|10.0.2(2|3|5)\\d{3})', 1, 1,'i', 0) is not null THEN 'Windows 11'
                WHEN regexp_substr({{ os_version }}, '(windows\\s{0,1}10|10.0.(19|18|17|16|14)\\d{3}|^10$)', 1, 1,'i', 0) is not null THEN 'Windows 10'
                WHEN regexp_substr({{ os_version }}, '(windows\\s{0,1}8\.1)', 1, 1,'i', 0) is not null THEN 'Windows 8.1'
                WHEN regexp_substr({{ os_version }}, '(windows\\s{0,1}8)', 1, 1,'i', 0) is not null THEN 'Windows 8'
                WHEN regexp_substr({{ os_version }}, '(windows\\s{0,1}7)', 1, 1,'i', 0) is not null THEN 'Windows 7'
                WHEN regexp_substr({{ os_version }}, '(windows\\s{0,1}vista)') is not null THEN 'Windows Vista'
                WHEN regexp_substr({{ os_version }}, '(windows\\s{0,1}xp)', 1, 1,'i', 0) is not null THEN 'Windows XP'
                WHEN regexp_substr({{ os_version }}, '(windows)', 1, 1,'i', 0) is not null THEN 'Windows'
            END
        WHEN {{ platform_name }} = 'macOS' THEN
            CASE
                WHEN regexp_substr({{ os_version }}, '(Sonoma|^\.14(\.\\d+)?|23(.\\d+)?)', 1, 1,'i', 0) is not null THEN 'Sonoma'
                WHEN regexp_substr({{ os_version }}, '(Ventura|^\.13(\.\\d+)?|22(.\\d+)?)', 1, 1,'i', 0) is not null THEN 'Ventura'
                WHEN regexp_substr({{ os_version }}, '(Monterey|^\.12(\.\\d+)?|21(.\\d+)?)', 1, 1,'i', 0) is not null THEN 'Monterey'
                WHEN regexp_substr({{ os_version }}, '(Big Sur|\\b11(\.\\d+)?|20(.\\d+)?)', 1, 1,'i', 0) is not null THEN 'Big Sur'
                WHEN regexp_substr({{ os_version }}, '(Catalina|10\.15(\\d+)?|19(.\\d+)?)', 1, 1,'i', 0) is not null THEN 'Catalina'
                WHEN regexp_substr({{ os_version }}, '(Mojave|10\.14(\\d+)?|18(.\\d+)?)', 1, 1,'i', 0) is not null THEN 'Mojave'
                WHEN regexp_substr({{ os_version }}, '(High Sierra|10\.13(\\d+)?|17(.\\d+)?)', 1, 1,'i', 0) is not null THEN 'High Sierra'
                WHEN regexp_substr({{ os_version }}, '(Sierra|10\.12(\\d+)?|16(.\\d+)?)', 1, 1,'i', 0) is not null THEN 'Sierra'
            END
        WHEN {{ platform_name }} = 'Linux' THEN
            CASE
                WHEN regexp_substr({{ os_version }}, '(Ubuntu)', 1, 1,'i', 0) is not null THEN 'Ubuntu'
                WHEN regexp_substr({{ os_version }}, '(CentOS)', 1, 1,'i', 0) is not null THEN 'CentOS'
                WHEN regexp_substr({{ os_version }}, '(openSuse|SuseLinux|sles)', 1, 1,'i', 0) is not null THEN 'SLES'
                WHEN regexp_substr({{ os_version }}, '(Fedora)', 1, 1,'i', 0) is not null THEN 'Fedora'
                WHEN regexp_substr({{ os_version }}, '(RHEL|RedHat)', 1, 1,'i', 0) is not null THEN 'RHEL'
                WHEN regexp_substr({{ os_version }}, '(Debian)', 1, 1,'i', 0) is not null THEN 'Debian'
            END
        ELSE NULL
    END
{% endmacro %}
