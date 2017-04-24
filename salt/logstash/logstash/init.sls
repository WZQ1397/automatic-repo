{%- from 'logstash/map.jinja' import logstash with context %}

{%- if logstash.use_upstream_repo %}
include:
  - .repo
{%- endif %}

{%- if salt['grains.get']('os', None) == "Ubuntu" %}
change service group in Ubuntu init script:
  file.replace:
    - name: /etc/init.d/logstash
    - pattern: "LS_GROUP=logstash"
    - repl: "LS_GROUP=adm"
    - watch_in:
      - service: logstash-svc

add adm group to logstash service account:
  user.present:
    - name: logstash
    - remove_groups: False
    - groups:
      - logstash
      - adm
{%- endif %}

{%- if logstash.inputs is defined %}
logstash-config-inputs:
  file.managed:
    - name: /etc/logstash/conf.d/01-inputs.conf
    - user: root
    - group: root
    - mode: 755
    - source: salt://logstash/files/01-inputs.conf
    - template: jinja
{%- else %}
logstash-config-inputs:
  file.absent:
    - name: /etc/logstash/conf.d/01-inputs.conf
{%- endif %}

{%- if logstash.filters is defined %}
logstash-config-filters:
  file.managed:
    - name: /etc/logstash/conf.d/02-filters.conf
    - user: root
    - group: root
    - mode: 755
    - source: salt://logstash/files/02-filters.conf
    - template: jinja
    - require:
      - pkg: logstash-pkg
{%- else %}
logstash-config-filters:
  file.absent:
    - name: /etc/logstash/conf.d/02-filters.conf
{%- endif %}

{%- if logstash.outputs is defined %}
logstash-config-outputs:
  file.managed:
    - name: /etc/logstash/conf.d/03-outputs.conf
    - user: root
    - group: root
    - mode: 755
    - source: salt://logstash/files/03-outputs.conf
    - template: jinja
    - require:
      - pkg: logstash-pkg
{%- else %}
logstash-config-outputs:
  file.absent:
    - name: /etc/logstash/conf.d/03-outputs.conf
{%- endif %}

logstash-svc:
  service.running:
    - name: {{logstash.svc}}
    - enable: true
    - watch:
      - file: logstash-config-inputs
      - file: logstash-config-filters
      - file: logstash-config-outputs
