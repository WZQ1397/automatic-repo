include:
  - openstack.init.control

keystone:
  pkg.installed[]

/etc/keystone/keystone.conf:
  file.managed:
    - source: salt://openstack/keystone/files/keystone.conf
    - mode: 644
    - user: root
    - group: root
    - template: jinja
    - defaults:
      MYSQL_SERVER: {{ pillar['keystone']['MYSQL_SERVER'] }}
      KEYSTONE_PASS: {{ pillar['keystone']['KEYSTONE_PASS'] }}
      KEYSTONE_USER: {{ pillar['keystone']['KEYSTONE_USER'] }}
      KEYSTONE_DBNAME: {{ pillar['keystone']['KEYSTONE_DBNAME'] }}
      ADMIN_TOKEN: {{ pillar['keystone']['ADMIN_TOKEN'] }}

/var/log/keystone:
  file.directory:
    - user: root
    - group: root

keystone-mysql:
  mysql_database.present:
    - name: {{ pillar['keystone']['KEYSTONE_DBNAME'] }}
    - require:
      - service: mysql-server
  mysql_user.present:
    - name: {{ pillar['keystone']['KEYSTONE_USER'] }}
    - host: {{ pillar['keystone']['HOST_ALLOW'] }}
    - password: {{ pillar['keystone']['KEYSTONE_PASS'] }}
    - require:
      - mysql_database: keystone-mysql
  mysql_grants.present:
    - grant: all
    - database: {{ pillar['keystone']['DB_ALLOW'] }}
    - user: {{ pillar['keystone']['KEYSTONE_USER'] }}
    - host: {{ pillar['keystone']['HOST_ALLOW'] }}
    - require:
      - mysql_user: keystone-mysql

keystone-init:
  cmd.run:
    - name: su -s /bin/sh -c "keystone-manage db_sync" keystone && touch /var/run/keystone-dbsync.lock
    - require:
      - mysql_grants: keystone-mysql
    - unless: test -f /var/run/keystone-dbsync.lock

keystone-data-init:
  file.managed:
    - name: /usr/local/bin/keystone_data.sh
    - source: salt://openstack/keystone/files/keystone_data.sh
    - mode: 755
    - user: root
    - group: root
    - template: jinja
    - defaults:
      ADMIN_PASSWD: {{ pillar['keystone']['ADMIN_PASSWD'] }} 
      ADMIN_TOKEN: {{ pillar['keystone']['ADMIN_TOKEN'] }}
      USER_PASSWD: {{ pillar['keystone']['USER_PASSWD'] }}
      CONTROL_IP: {{ pillar['keystone']['CONTROL_IP'] }}
  cmd.run:
    - name: bash /usr/local/bin/keystone_data.sh && touch /var/run/keystone-datainit.lock
    - require:
      - file: keystone-data-init
    - unless: test -f /var/run/keystone-datainit.lock

#create ENV
/root/keystone_admin.sh:
  file.managed:
    - source: salt://openstack/keystone/files/keystone_admin.sh
    - mode: 755
    - user: root
    - group: root
    - template: jinja
    - defaults:
      ADMIN_PASSWD: {{ pillar['keystone']['ADMIN_PASSWD'] }}
      ADMIN_TOKEN: {{ pillar['keystone']['ADMIN_TOKEN'] }}
      CONTROL_IP: {{ pillar['keystone']['CONTROL_IP'] }}
