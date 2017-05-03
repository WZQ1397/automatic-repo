zebra_enabled:
    file.replace:
        - name: /etc/quagga/daemons
        - pattern: '^zebra=no'
        - repl: 'zebra=yes'
        - backup: False
        - require:
            - pkg: quagga
        - watch_in:
            - service: quagga
