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
      NOVA_USER: {{ pillar['nova']['NOVA_USER'] }}
      NOVA_PASS: {{ pillar['nova']['NOVA_PASS'] }}
      NEUTRON_USER: {{ pillar['nova']['NEUTRON_USER'] }}
      NEUTRON_PASS: {{ pillar['nova']['NEUTRON_PASS'] }}
      PLACEMENT_USER: {{ pillar['nova']['PLACEMENT_USER'] }}
      PLACEMENT_PASS: {{ pillar['nova']['PLACEMENT_PASS'] }}
      RABBITMQ_HOST: {{ pillar['nova']['RABBITMQ_HOST'] }}
      RABBITMQ_PORT: {{ pillar['nova']['RABBITMQ_PORT'] }}
      RABBITMQ_USER: {{ pillar['nova']['RABBITMQ_USER'] }}
      RABBITMQ_PASS: {{ pillar['nova']['RABBITMQ_PASS'] }}
      NOVNC_PROXY_URL: {{ pillar['nova']['NOVNC_PROXY_URL'] }}
      GLANCE_HOST: {{ pillar['nova']['GLANCE_HOST'] }}
      AUTH_KEYSTONE_HOST: {{ pillar['nova']['AUTH_KEYSTONE_HOST'] }}
      AUTH_KEYSTONE_PORT: {{ pillar['nova']['AUTH_KEYSTONE_PORT'] }}
      AUTH_KEYSTONE_PROTOCOL: {{ pillar['nova']['AUTH_KEYSTONE_PROTOCOL'] }}
      AUTH_ADMIN_PASS: {{ pillar['nova']['AUTH_ADMIN_PASS'] }}
      VM_TYPE: {{ pillar['nova']['VM_TYPE'] }}
      CONTROL_IP: {{ pillar['keystone']['CONTROL_IP'] }}
      VNC_PROXY_URL: {{ pillar['nova']['VNC_PROXY_URL'] }}
      MY_IP:{{ salt['network.ip_addrs ']('ens160') }}
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
      service nova-compute restart
      service neutron-linuxbridge-agent restart
    
