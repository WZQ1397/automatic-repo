keepalived:
    pkg:
        - installed
    service.running:
        - enable: True
        - sig: keepalived
        - watch:
            - file: /etc/keepalived/keepalived.conf
        - require:
            - pkg: keepalived

/etc/keepalived/keepalived.conf:
    file.managed:
        - source: {{pillar['keepalived']['config']}}
        - user: root
        - group: root
        - mode: 600
