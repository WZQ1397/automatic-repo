nova-api-metadata:
    pkg:
        - installed

nova-network:
    pkg:
        - installed
    service.running:
        - enable: True
        - watch:
            - file: /etc/nova
            