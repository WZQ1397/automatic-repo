corosync:
    pkg:
        - installed
    service.running:
        - enable: True
        - require:
            - pkg: corosync
        - watch:
            - file: /etc/default/corosync
            - file: /etc/corosync

/etc/default/corosync:
    file.sed:
        - before: 'no'
        - after: 'yes'
        - limit: '^START'

/etc/corosync:
    file.recurse:
        - source: salt://utils/corosync/_files
        - template: jinja
        - clean: True
        - require:
            - pkg: corosync
