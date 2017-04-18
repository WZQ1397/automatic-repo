include:
  - openstack.nova.nova_control

/etc/nova/nova.conf:
  file.recurse:
    - source: salt://openstack/nova/files/nova-control
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

/var/log/nova:
  file.directory:
    - user: root
    - group: root

/var/lib/nova:
  file.directory:
    - user: root
    - group: root

/usr/local/bin/nova_data.sh:
  file.managed:
    - source: salt://openstack/nova/files/nova_data.sh
    - mode: 755
    - user: root
    - group: root
    - template: jinja
    - defaults:
      ADMIN_PASSWD: {{ pillar['nova']['ADMIN_PASSWD'] }} 
      CONTROL_IP: {{ pillar['nova']['CONTROL_IP'] }}

nova-data-init:
  cmd.run:
    - name: bash /usr/local/bin/nova_data.sh && touch /var/run/nova-datainit.lock
    - require:
      - file: /usr/local/bin/nova_data.sh
      - cmd.run: nova-init
    - unless: test -f /var/run/nova-datainit.lock

nova-init:
  cmd.run:
    - name: su -s /bin/sh -c "nova-manage api_db sync" nova && touch /var/run/nova-dbsync.lock
    - require:
      - mysql_grants: nova-mysql
    - unless: test -f /var/run/nova-dbsync.lock

placement-reg:
  cmd.run:
    - name: |
        su -s /bin/sh -c "nova-manage cell_v2 map_cell0" nova
        su -s /bin/sh -c "nova-manage cell_v2 create_cell --name=cell1 --verbose" nova
        touch /var/run/nova-placement-reg.lock
    - require:
      - mysql_grants: nova-mysql
    - unless: test -f /var/run/nova-placement-reg.lock

 fin_placement:
    cmd.run:
      - name: su -s /bin/sh -c "nova-manage db sync" nova && nova-manage cell_v2 list_cells > nova-placement-reg.lock

NOVA_RELOAD:
    cmd.run:
      - name: |
        service nova-api restart
        service nova-consoleauth restart
        service nova-scheduler restart
        service nova-conductor restart
        service nova-novncproxy restart