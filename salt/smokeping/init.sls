{% set SMOKE_PATH = smokeping %}
{% set ADV = /opt/}
{{ADV}}{{ SMOKE_PATH }}/etc/:
  file.managed:
    - source: salt://{{ SMOKE_PATH }}/smokeping_config
    - user: root
    - file_mode: '0644'