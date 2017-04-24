include:
  - openstack.neutron.neutron_control

/etc/neutron/neutron.conf:
  file.recurse:
    - source: salt://openstack/neutron/files/control
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
      NOVA_API_DBNAME: {{ pillar['nova']['NOVA_API_DBNAME'] }}
      NOVA_DBNAME: {{ pillar['nova']['NOVA_DBNAME'] }}
      MYSQL_SERVER: {{ pillar['nova']['MYSQL_SERVER'] }}
      MY_IP:{{ salt['network.ip_addrs ']('ens160') }}
      
/var/log/neutron:
  file.directory:
    - user: root
    - group: root

/var/lib/neutron:
  file.directory:
    - user: root
    - group: root

/usr/local/bin/neutron_data.sh:
  file.managed:
    - source: salt://openstack/neutron/files/neutron_data.sh
    - mode: 755
    - user: root
    - group: root
    - template: jinja
    - defaults:
      ADMIN_PASSWD: {{ pillar['neutron']['ADMIN_PASSWD'] }} 
      CONTROL_IP: {{ pillar['neutron']['CONTROL_IP'] }}

neutron-data-init:
  cmd.run:
    - name: bash /usr/local/bin/neutron_data.sh && touch /var/run/neutron-datainit.lock
    - require:
      - file: /usr/local/bin/neutron_data.sh
      - cmd.run: neutron-init
    - unless: test -f /var/run/neutron-datainit.lock

neutron-init:
  cmd.run:
    - name: su -s /bin/sh -c "neutron-db-manage --config-file /etc/neutron/neutron.conf \
  --config-file /etc/neutron/plugins/ml2/ml2_conf.ini upgrade head" neutron && touch /var/run/neutron-dbsync.lock
    - require:
      - mysql_grants: neutron-mysql
    - unless: test -f /var/run/neutron-dbsync.lock

NEUTRON_RELOAD:
    cmd.run:
      - name: |
        service nova-api restart
        service neutron-server restart
        service neutron-linuxbridge-agent restart
        service neutron-dhcp-agent restart
        service neutron-metadata-agent restart
        service neutron-l3-agent restart