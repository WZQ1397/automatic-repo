include:
    - .basic

keystone:
    pkg:
        - installed
    service.running:
        - enable: True
        - requires:
            - pkg: keystone
            - file: /etc/keystone
        - watch:
            - file: /etc/keystone

/etc/keystone:
    file.recurse:
        - source: salt://files/openstack/keystone/
        - user: root
        - group: root
        - dir_mode: '0775'
        - file_mode: '0644'
        - clean: True
        - require:
            - pkg: keystone
