{% set dhcpd = salt['grains.filter_by']({
    'Debian': {'pkg': 'isc-dhcp-server', 'srv': 'isc-dhcp-server'},
    'RedHat': {'pkg': 'isc-dhcp-server', 'srv': 'isc-dhcp-server'}
}, default='Debian') %}


isc-dhcp-server:
    pkg.installed:
        - name: {{ dhcpd.pkg }}
    service.running:
        - name: {{ dhcpd.srv }}
        - enable: True
        - require:
            - pkg: {{ dhcpd.pkg }}

# /etc/dhcp/dhcpd.conf:
#    file.managed:
#        - source: salt://services/dhcpd/dhcpd.conf
#        - watch_in:
#          - service: {{ dhcpd.pkg }}
