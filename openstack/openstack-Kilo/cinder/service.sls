cinder-common:
    pkg:
        - installed
        
cinder-api:
    pkg:
        - installed
    service.running:
        - enable: True
        - watch:
            - file: /etc/cinder
            
cinder-scheduler:
    pkg:
        - installed
    service.running:
        - enable: True
        - watch:
            - file: /etc/cinder

/etc/cinder:
    file.recurse:
        - source: salt://files/openstack/cinder-control/
        #- clean: True
        - require:
            - pkg: cinder-api
            - pkg: cinder-scheduler