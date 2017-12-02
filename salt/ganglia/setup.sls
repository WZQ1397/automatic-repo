#https://github.com/ganglia/gmond_python_modules
{% from "ganglia/map.jinja" import ganglia with context %}

{% for cnf in ['gmond.conf','gmetad.conf'] %}
{{ ganglia.confpath }}/{{ cnf }}:
  file.managed:
    - source: salt://ganglia/{{ cnf }}
    - template: jinja
    - user: root
    - group: root
    - mode: '0755'
{% endfor %}
