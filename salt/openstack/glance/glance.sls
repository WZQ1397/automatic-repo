include:
  - openstack.init.control

file_bak:
  file.managed:
    - name: /tmp/glancebak.sh
    - source: salt://openstack/glance/files/glancebak.sh
  cmd.run:
    - name: bash /tmp/glancebak.sh && touch /var/run/glance-bak
    - unless: test -f /var/run/glance-bak

/etc/glance/schema-image.json:
  file.managed:
    - source: salt://openstack/glance/files/schema-image.json
    - mode: 644
    - user: root
    - group: root

/etc/glance/policy.json:
  file.managed:
    - source: salt://openstack/glance/files/policy.json
    - mode: 644
    - user: root
    - group: root

/etc/glance/glance-scrubber.conf:
  file.managed:
    - source: salt://openstack/glance/files/glance-scrubber.conf
    - mode: 644
    - user: root
    - group: root

/etc/glance/glance-registry-paste.ini:
  file.managed:
    - source: salt://openstack/glance/files/glance-registry-paste.ini
    - mode: 644
    - user: root
    - group: root

/etc/glance/glance-api-paste.ini:
  file.managed:
    - source: salt://openstack/glance/files/glance-api-paste.ini
    - mode: 644
    - user: root
    - group: root

/etc/glance/glance-cache.conf:
  file.managed:
    - source: salt://openstack/glance/files/glance-cache.conf
    - mode: 644
    - user: root
    - group: root

/etc/glance/glance-api.conf:
  file.managed:
    - source: salt://openstack/glance/files/glance-api.conf
    - mode: 644
    - user: root
    - group: root
    - template: jinja
    - defaults:
      MYSQL_SERVER: {{ pillar['glance']['MYSQL_SERVER'] }}
      GLANCE_USER: {{ pillar['glance']['GLANCE_USER'] }}
      GLANCE_PASS: {{ pillar['glance']['GLANCE_PASS'] }}
      GLANCE_DBNAME: {{ pillar['glance']['GLANCE_DBNAME'] }}
      RABBITMQ_HOST: {{ pillar['glance']['RABBITMQ_HOST'] }}
      RABBITMQ_PORT: {{ pillar['glance']['RABBITMQ_PORT'] }}
      RABBITMQ_USER: {{ pillar['glance']['RABBITMQ_USER'] }}
      RABBITMQ_PASS: {{ pillar['glance']['RABBITMQ_PASS'] }}
      AUTH_KEYSTONE_HOST: {{ pillar['glance']['AUTH_KEYSTONE_HOST'] }}
      AUTH_ADMIN_PASS: {{ pillar['glance']['AUTH_ADMIN_PASS'] }}

/etc/glance/glance-registry.conf:
  file.managed:
    - source: salt://openstack/glance/files/glance-registry.conf
    - mode: 644
    - user: root
    - group: root
    - template: jinja
    - defaults:
      MYSQL_SERVER: {{ pillar['glance']['MYSQL_SERVER'] }}
      GLANCE_USER: {{ pillar['glance']['GLANCE_USER'] }}
      GLANCE_PASS: {{ pillar['glance']['GLANCE_PASS'] }}
      GLANCE_DBNAME: {{ pillar['glance']['GLANCE_DBNAME'] }}
      AUTH_KEYSTONE_HOST: {{ pillar['glance']['AUTH_KEYSTONE_HOST'] }}
      AUTH_ADMIN_PASS: {{ pillar['glance']['AUTH_ADMIN_PASS'] }}

/var/log/glance:
  file.directory:
    - user: root
    - group: root

/var/lib/glance:
  file.directory:
    - user: root
    - group: root

glance-mysql:
  mysql_database.present:
    - name: {{ pillar['glance']['GLANCE_DBNAME'] }}
    - require:
      - service: mysql-server
  mysql_user.present:
    - name: {{ pillar['glance']['GLANCE_USER'] }}
    - host: {{ pillar['glance']['HOST_ALLOW'] }}
    - password: {{ pillar['glance']['GLANCE_PASS'] }}
    - require:
      - mysql_database: glance-mysql
  mysql_grants.present:
    - grant: all
    - database: {{ pillar['glance']['DB_ALLOW'] }}
    - user: {{ pillar['glance']['GLANCE_USER'] }}
    - host: {{ pillar['glance']['HOST_ALLOW'] }}
    - require:
      - mysql_user: glance-mysql

glance-data-init:
  file.managed:
    - name: /usr/local/bin/glance_data.sh
    - source: salt://openstack/glance/files/glance_data.sh
    - mode: 755
    - user: root
    - group: root
    - template: jinja
    - defaults:
      ADMIN_PASSWD: {{ pillar['glance']['ADMIN_PASSWD'] }} 
      ADMIN_TOKEN: {{ pillar['glance']['ADMIN_TOKEN'] }}
      CONTROL_IP: {{ pillar['glance']['CONTROL_IP'] }}
    - watch_in:
      service: glance-api
  cmd.run:
    - name: bash /usr/local/bin/glance_data.sh && touch /var/run/glance-datainit.lock
    - require:
      - service: openstack-glance-api
      - service: openstack-glance-registry
    - unless: test -f /var/run/glance-datainit.lock


glance-api:
  service:
    enable: True
    reload: True

glance-api:
  service:
    enable: True
    reload: True