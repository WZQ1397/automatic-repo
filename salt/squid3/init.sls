squid3:
    pkg:
        - installed
    service.running:
        - enable: True
        - require:
            - pkg: squid3

/etc/squid3/objects:
    file.directory:
        - user  : root
        - group : root
        - mode  : 0755
        - require:
            - pkg: squid3

{{pillar.squid3.config.target}}:
    file.managed:
        - source  : {{pillar.squid3.config.source}}
        - user    : root
        - group   : root
        - mode    : 0644
        - require :
            - pkg: squid3
        - watch_in:
            - service: squid3
