ospfd_enabled:
    file.replace:
        - name: /etc/quagga/daemons
        - pattern: '^ospfd=no'
        - repl: 'ospfd=yes'
        - backup: False
        - require:
            - pkg: quagga
        - watch_in:
            - service: quagga
