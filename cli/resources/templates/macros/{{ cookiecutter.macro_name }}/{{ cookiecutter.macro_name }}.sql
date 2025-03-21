{% raw %}
{% macro {% endraw %}{{ cookiecutter.macro_name }}{% raw %}(param) %}    
    {{ log("Start macro: " ~ param, info=True) }}
{% endmacro %}
{% endraw %}
