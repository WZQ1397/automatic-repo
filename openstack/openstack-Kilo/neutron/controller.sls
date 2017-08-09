neutron-server-packages:
    pkg.installed:
        - names:
            - neutron-server
            - neutron-plugin-ml2

neutron-server:
    service.running:
        - enable: True
        - requires:
            - pkg: neutron-server-packages
            - pkg: nova-packages
        - watch:
            - file: /etc/neutron

/etc/neutron:
    file.recurse:
        - source: salt://files/openstack/neutron-control/
        - clean: True
        - require:
            - pkg: neutron-server-packages