{% from "telegraf/map.jinja" import telegraf with context %}

telegraf-config:
  file.managed:
    - name: /etc/telegraf/telegraf.conf
    - source: salt://telegraf/files/telegraf.conf
    - user: root
    - group: root
    - mode: 644
    - context:
        telegraf: {{ telegraf }}
    - template: jinja
    - require:
      - sls: telegraf.install

{%- if telegraf.use_system_inputs == True %}
telegraf-system-inputs:
  file.managed:
    - name: /etc/telegraf/telegraf.d/system.conf
    - source: salt://telegraf/files/system.conf
    - user: root
    - group: root
    - mode: 644
    - require:
      - sls: telegraf.install
{%- else %}
telegraf-system-inputs:
  file.absent:
    - name: /etc/telegraf/telegraf.d/system.conf
{%- endif %}

{%- if telegraf.inputs is defined %}
telegraf-inputs:
  file.managed:
    - name: /etc/telegraf/telegraf.d/inputs.conf
    - user: root
    - group: root
    - mode: 644
    - source: salt://telegraf/files/inputs.conf
    - template: jinja
    - require:
      - sls: telegraf.install
    - watch_in:
      - service: telegraf-service
{%- else %}
telegraf-inputs:
  file.absent:
    - name: /etc/telegraf/telegraf.d/inputs.conf
{%- endif %}

{%- if telegraf.global_tags is defined %}
telegraf-global_tags:
  file.managed:
    - name: /etc/telegraf/telegraf.d/global_tags.conf
    - user: root
    - group: root
    - mode: 644
    - source: salt://telegraf/files/global_tags.conf
    - template: jinja
    - require:
      - sls: telegraf.install
    - watch_in:
      - service: telegraf-service
{%- else %}
telegraf-global_tags:
  file.absent:
    - name: /etc/telegraf/telegraf.d/global_tags.conf
{%- endif %}

{%- if telegraf.outputs is defined %}
telegraf-outputs:
  file.managed:
    - name: /etc/telegraf/telegraf.d/outputs.conf
    - user: root
    - group: root
    - mode: 644
    - source: salt://telegraf/files/outputs.conf
    - template: jinja
    - require:
      - sls: telegraf.install
    - watch_in:
      - service: telegraf-service
{%- else %}
telegraf-outputs:
  file.absent:
    - name: /etc/telegraf/telegraf.d/outputs.conf
{%- endif %}
