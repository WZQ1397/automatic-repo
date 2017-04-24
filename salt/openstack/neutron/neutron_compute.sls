neutron-compute:
  pkg.installed:
    - name: neutron-linuxbridge-agent
        
/etc/neutron:
  file.recurse:
    - source: salt://openstack/neutron/files/computer
    - mode: 644
    - user: root
    - group: root
    - template: jinja
    - defaults:
      NEUTRON_USER: {{ pillar['neutron']['NEUTRON_USER'] }}
      NEUTRON_PASS: {{ pillar['neutron']['NEUTRON_PASS'] }}
      AUTH_KEYSTONE_HOST: {{ pillar['neutron']['AUTH_KEYSTONE_HOST'] }}
      AUTH_KEYSTONE_PORT: {{ pillar['neutron']['AUTH_KEYSTONE_PORT'] }}
      AUTH_ADMIN_PASS: {{ pillar['neutron']['AUTH_ADMIN_PASS'] }}
      CONTROL_IP: {{ pillar['keystone']['CONTROL_IP'] }}
      INTERFACE:{{ pillar['neutron']['INTERFACE'] }}
    - require:
      - pkg: neutron-compute
    - watch_in:
      - service: neutron-compute
      
/var/log/neutron:
  file.directory:
    - user: root
    - group: root

/var/lib/neutron:
  file.directory:
    - user: root
    - group: root
    
neutron_com-reload:
  cmd.run:
    - name: |
      service neutron-compute restart
      service neutron-linuxbridge-agent restart
    
