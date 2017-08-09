neutron-compute-packages:
    pkg.installed:
        - names:
            - neutron-common
            - neutron-plugin-ml2
            #- neutron-plugin-openvswitch-agent
            - neutron-plugin-linuxbridge-agent
            #- openvswitch-datapath-dkms
            
net.ipv4.conf.all.rp_filter:
    sysctl.present:
        - value: 0

net.ipv4.conf.default.rp_filter:
    sysctl.present:
        - value: 0    

/etc/neutron:
    file.recurse:
        - source: salt://files/openstack/neutron-compute/
        - template: jinja
        #- clean: True
        - require:
            - pkg: neutron-compute-packages

neutron-network-services:
    service.running:
        - names:
            #- neutron-plugin-openvswitch-agent
            - neutron-plugin-linuxbridge-agent
        - enable: True
        - requires:
            - pkg: neutron-compute-packages
            - file: /etc/neutron
        - watch:
            - file: /etc/neutron