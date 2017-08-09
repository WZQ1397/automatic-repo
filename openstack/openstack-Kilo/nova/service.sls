nova-packages:
    pkg.installed:
        - names:
            - nova-api
            - nova-cert
            - nova-conductor
            - nova-consoleauth
            - nova-novncproxy
            - nova-scheduler
            - python-novaclient

nova-services:
    service.running:
        - names:
            - nova-api
            - nova-cert
            - nova-consoleauth
            - nova-scheduler
            - nova-conductor
            - nova-novncproxy
        - enable: True
        #- reload: True
        - requires:
            - pkg: nova-packages
            - file: /etc/nova/
        - watch:
            - file: /etc/nova/

/etc/nova/:
    file.recurse:
        - source: salt://files/openstack/nova-control/
        - require:
            - pkg: nova-packages