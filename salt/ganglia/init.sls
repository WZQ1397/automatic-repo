{% from "ganglia/map.jinja" import ganglia with context %}
#{% set ganglia_web=ganglia.conf %}
include:
  - apache2
  - ganglia
  
ganglia_admin:
  cmd.run:
    - 'htpasswd -c {{ ganglia.authpath }} {{ ganglia.name }}'
    # /etc/httpd/auth.basic zach
    
/etc/httpd/conf.d/{{ ganglia.web }}:
  file.managed:
    - source: salt://ganglia/conf.d/{{ ganglia.web }}
    - user: root
    - group: root
    - mode: '0755'
    - template: jinja
    - require:
      - pkg: apache2
    - watch_in:
      - service: ganglia


    
    
