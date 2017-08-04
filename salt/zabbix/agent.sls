include:
    - .release

zabbix-agent:
    pkg.installed:
        - require:
            - pkg: zabbix-release
    service.running:
        - enable: True
        - require:
            - pkg: zabbix-agent

/etc/zabbix/zabbix_agentd.d/server.conf:
    file.managed:
        - contents : |
            Server={{pillar['zabbix']['agent']['server']}}
            ServerActive={{pillar['zabbix']['agent']['server']}}
            Hostname={{grains['id']|lower}}
        - user    : root
        - group   : root
        - mode    : 0644
        - require :
            - pkg: zabbix-agent
        - watch_in:
            - service: zabbix-agent