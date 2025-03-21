{% macro filter_by_tool_and_endpoint(ref_name, tool_name, endpoint) %}
    {{ref_name}}."job_id" = '{{ var("job_id") }}' and
    {{ref_name}}."org_id" = '{{ var("organization_id") }}' and
    {{ref_name}}."instance_id" = '{{ var("instance_id") }}' and
    {{ref_name}}."tool" = '{{ tool_name }}' and
    {{ref_name}}."endpoint" = '{{ endpoint }}'
{% endmacro %}
