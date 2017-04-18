nova-compute:
  pkg.installed[]
        
/etc/nova:
  file.recurse:
    - source: salt://openstack/nova/files/nova-computer
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
    - require:
      - pkg: nova-compute
    - watch_in:
      - service: nova-compute

nova_com-reload:
  cmd.run:
    - name: service nova-compute restart
    
libvirtd_remove_default_network:
  cmd.run:
    - name: virsh net-destroy default && virsh net-undefine default
    - onlyif: virsh net-info default 1>/dev/null 2>&1
