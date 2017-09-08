{% from "telegraf/map.jinja" import telegraf with context %}

telegraf-pkg:
  file.managed:
    - name: /tmp/telegraf_{{ telegraf.version }}{{ telegraf.pkgsuffix }}
    - source: {{ telegraf.source_url }}{{ telegraf.version }}{{ telegraf.pkgsuffix }}
    - source_hash: md5={{ telegraf.source_hash }}
    - unless: test -f /tmp/telegraf_{{ telegraf.version }}{{ telegraf.pkgsuffix }}

telegraf-install:
  pkg.installed:
    - sources:
      - telegraf: /tmp/telegraf_{{ telegraf.version }}{{ telegraf.pkgsuffix }}
    - require:
      - file: telegraf-pkg
    - watch:
      - file: telegraf-pkg
