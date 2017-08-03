include:
    - network.racoon
    - network.openvpn
    - network.iptables

/etc/openvpn:
    file.recurse:
        - source: salt://nodes/others/_files/openvpn

/etc/racoon:
    file.recurse:
        - source: salt://nodes/others/_files/racoon

/etc/ipsec-tools.conf:
    file.managed:
        - source: salt://nodes/others/_files/ipsec-tools.conf

quagga:
    pkg:
        - installed
    service.running:
        - enable: True
        - sig: zebra
        - watch:
            - file: /etc/quagga/*

isc-dhcp-server:
    pkg:
        - installed
    service.running:
        - enable: True
        - watch:
            - file: /etc/dhcp
        - require:
            - pkg: isc-dhcp-server

squid3:
    pkg:
        - installed
    service.running:
        - enable: True
        - require:
            - pkg: squid3
        - watch:
            - file: /etc/squid3

/etc/dhcp:
    file.recurse:
        - source: salt://nodes/others/_files/dhcp

/etc/squid3:
    file.recurse:
        - source: salt://nodes/others/_files/squid3

/etc/quagga/daemons:
    file.sed:
        - before: 'no'
        - after: 'yes'
        - limit: '^(zebra|ospfd)='

/etc/quagga/Quagga.conf:
    file.managed:
        - source: salt://nodes/others/quagga.conf
        - user: root
        - group: quaggavty
        - mode: 0640

/usr/local/bin/dyndns:
    file.managed:
        - source: salt://nodes/others/dyndns
        - user: root
        - group: root
        - mode: 0711
    cron.file:
        - name: salt://nodes/others/crontab
        - user: root
