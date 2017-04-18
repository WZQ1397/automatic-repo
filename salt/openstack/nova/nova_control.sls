nova-pkg:
  pkg.installed:
    - pkgs:
        - nova-api
        - nova-conductor
        - nova-consoleauth
        - nova-novncproxy
        - nova-scheduler
        - nova-placement-api
    
nova-mysql:
  mysql_database.present:
    - name: {{ pillar['nova']['NOVA_DBNAME'] }}
    - require:
      - service: mysql-server
  mysql_user.present:
    - name: {{ pillar['nova']['NOVA_USER'] }}
    - host: {{ pillar['nova']['HOST_ALLOW'] }}
    - password: {{ pillar['nova']['NOVA_PASS'] }}
    - require:
      - mysql_database: nova-mysql
  mysql_grants.present:
    - grant: all
    - database: {{ pillar['nova']['DB_ALLOW'] }}
    - user: {{ pillar['nova']['NOVA_USER'] }}
    - host: {{ pillar['nova']['HOST_ALLOW'] }}
    - require:
      - mysql_user: nova-mysql

nova-api-mysql:
  mysql_database.present:
    - name: {{ pillar['nova']['NOVA_API_DBNAME'] }}
    - require:
      - service: mysql-server
  mysql_user.present:
    - name: {{ pillar['nova']['NOVA_USER'] }}
    - host: {{ pillar['nova']['HOST_ALLOW'] }}
    - password: {{ pillar['nova']['NOVA_PASS'] }}
    - require:
      - mysql_database: nova-api-mysql
  mysql_grants.present:
    - grant: all
    - database: {{ pillar['nova']['API_DB_ALLOW'] }}
    - user: {{ pillar['nova']['NOVA_USER'] }}
    - host: {{ pillar['nova']['HOST_ALLOW'] }}
    - require:
      - mysql_user: nova-api-mysql

placement-api-mysql:
  mysql_database.present:
    - name: {{ pillar['nova']['PLACEMENT_DBNAME'] }}
    - require:
      - service: mysql-server
  mysql_user.present:
    - name: {{ pillar['nova']['NOVA_USER'] }}
    - host: {{ pillar['nova']['HOST_ALLOW'] }}
    - password: {{ pillar['nova']['NOVA_PASS'] }}
    - require:
      - mysql_database: placement-api-mysql
  mysql_grants.present:
    - grant: all
    - database: {{ pillar['nova']['PLACEMENT_ALLOW'] }}
    - user: {{ pillar['nova']['NOVA_USER'] }}
    - host: {{ pillar['nova']['HOST_ALLOW'] }}
    - require:
      - mysql_user: placement-api-mysql

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