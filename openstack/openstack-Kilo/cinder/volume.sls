cinder-packages:
    pkg.installed:
        - names:
            - lvm2
            - cinder-volume

cinder-volume:
    service.running:
        - enable: True
        - requires:
            - pkg: cinder-packages
            - file: /etc/cinder
        - watch:
            - file: /etc/cinder

/etc/cinder:
    file.recurse:
        - source: salt://files/openstack/cinder-volume
        - require:
            - pkg: cinder-packages