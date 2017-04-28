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
      NEUTRON_USER: {{ pillar['neutron']['NEUTRON_USER'] }}
      NEUTRON_PASS: {{ pillar['neutron']['NEUTRON_PASS'] }}
      RABBITMQ_HOST: {{ pillar['neutron']['RABBITMQ_HOST'] }}
      RABBITMQ_PORT: {{ pillar['neutron']['RABBITMQ_PORT'] }}
      RABBITMQ_USER: {{ pillar['neutron']['RABBITMQ_USER'] }}
      RABBITMQ_PASS: {{ pillar['neutron']['RABBITMQ_PASS'] }}
      AUTH_KEYSTONE_HOST: {{ pillar['neutron']['AUTH_KEYSTONE_HOST'] }}
      AUTH_KEYSTONE_PORT: {{ pillar['neutron']['AUTH_KEYSTONE_PORT'] }}
      AUTH_ADMIN_PASS: {{ pillar['neutron']['AUTH_ADMIN_PASS'] }}
      CONTROL_IP: {{ pillar['keystone']['CONTROL_IP'] }}
      VNC_PROXY_URL: {{ pillar['neutron']['VNC_PROXY_URL'] }}
      MYSQL_SERVER: {{ pillar['neutron']['MYSQL_SERVER'] }}
      MY_IP:{{ salt['network.ip_addrs']('ens160') }}
      INTERFACE:{{ pillar['neutron']['INTERFACE'] }}
      
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
        service neutron-api restart
        service neutron-server restart
        service neutron-linuxbridge-agent restart
        service neutron-dhcp-agent restart
        service neutron-metadata-agent restart
        service neutron-l3-agent restart