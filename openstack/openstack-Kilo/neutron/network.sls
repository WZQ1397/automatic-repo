neutron-network-packages:
    pkg.installed:
        - names:
            - neutron-common
            - neutron-plugin-ml2
            - neutron-plugin-openvswitch-agent
            - neutron-plugin-linuxbridge-agent
            - openvswitch-datapath-dkms
            - neutron-l3-agent
            - neutron-dhcp-agent
#The following extra packages will be installed:
#  bridge-utils neutron-common neutron-dhcp-agent neutron-l3-agent
#  neutron-metadata-agent neutron-plugin-linuxbridge neutron-plugin-ml2
#  neutron-plugin-openvswitch-agent python-neutron
#The following NEW packages will be installed:
#  bridge-utils neutron-plugin-linuxbridge neutron-plugin-linuxbridge-agent
#The following packages will be upgraded:
#  neutron-common neutron-dhcp-agent neutron-l3-agent neutron-metadata-agent
#  neutron-plugin-ml2 neutron-plugin-openvswitch-agent python-neutron


net.ipv4.ip_forward:
    sysctl.present:
        - value: 1
        
net.ipv4.conf.all.rp_filter:
    sysctl.present:
        - value: 0

net.ipv4.conf.default.rp_filter:
    sysctl.present:
        - value: 0

/etc/neutron:
    file.recurse:
        - source: salt://files/openstack/neutron-network/
        - template: jinja
        #- clean: True
        - require:
            - pkg: neutron-network-packages

neutron-network-services:
    service.running:
        - names:
            - neutron-plugin-openvswitch-agent
            - neutron-plugin-linuxbridge-agent
            - neutron-dhcp-agent
            - neutron-l3-agent
            - neutron-metadata-agent
        - enable: True
        - requires:
            - pkg: neutron-network-packages
            - file: /etc/neutron
        - watch:
            - file: /etc/neutron
