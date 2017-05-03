quagga:
    pkg:
        - installed
    service.running:
        - enable: True
        - sig: zebra
        # - watch:
        #     - file: /etc/quagga/*

# /etc/quagga/Quagga.conf:
#     file.managed:
#         - user: root
#         - group: quaggavty
#         - mode: 0640
