glance:
    pkg.installed:
        - names:
            - glance
            - python-glanceclient

glance-api:
    service.running:
        - enable: True
        - requires:
            - pkg: glance
            - file: /etc/glance
        - watch:
            - file: /etc/glance

glance-registry:
    service.running:
        - enable: True
        - requires:
            - pkg: glance
            - file: /etc/glance
        - watch:
            - file: /etc/glance

/etc/glance:
    file.recurse:
        - source: salt://files/openstack/glance/
        - require:
            - pkg: glance
