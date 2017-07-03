{% from "chrony/map.jinja" import chrony with context %}

chrony:
  pkg.installed:
    - name: {{ chrony.package }}
  service.running:
    - enable: True
    - name: {{ chrony.service }}
    - require:
      - pkg: {{ chrony.package }}
