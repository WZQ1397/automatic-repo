{% set ganglia_web=/etc/httpd/conf.d/ganglia.conf %}
include:
  - apache2

{{ ganglia_web }}:
  file.managed:
    source: salt://ganglia/conf.d/ganglia.conf
        - user: root
        - group: root
        - mode: '0755'
        - require:
            - pkg: apache2
