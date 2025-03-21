{% macro get_device_policy_external_id(device_policies) %}
    CASE
        WHEN device_policies:"prevention":"applied"::boolean THEN device_policies:"prevention":"policy_id"::text
        WHEN device_policies:"device_control":"applied"::boolean THEN device_policies:"device_control":"policy_id"::text
        ELSE NULL
    END
{% endmacro %}
