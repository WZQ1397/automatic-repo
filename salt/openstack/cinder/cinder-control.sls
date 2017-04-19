include:
  - openstack.pre.control

cinder-install:
  pkg.installed:
    - pkgs:
      - cinder-api
      - cinder-scheduler

cinder-mysql:
  mysql_database.present:
    - name: {{ pillar['CINDER']['CINDER_DBNAME'] }}
    - require:
      - service: mysql-server
  mysql_user.present:
    - name: {{ pillar['CINDER']['CINDER_USER'] }}
    - host: {{ pillar['CINDER']['HOST_ALLOW'] }}
    - password: {{ pillar['CINDER']['CINDER_PASS'] }}
    - require:
      - mysql_database: cinder-mysql
  mysql_grants.present:
    - grant: all
    - database: {{ pillar['CINDER']['DB_ALLOW'] }}
    - user: {{ pillar['CINDER']['CINDER_USER'] }}
    - host: {{ pillar['CINDER']['HOST_ALLOW'] }}
    - require:
      - mysql_user: cinder-mysql

/etc/cinder/cinder.conf:
  file.managed:
    - source: salt://openstack/cinder/files/control/cinder.conf
    - mode: 755
    - user: root
    - group: root
    - template: jinja
    - defaults:
      CONTROL_IP: {{ pillar['CINDER']['CONTROL_IP'] }}
      CINDER_USER: {{ pillar['CINDER']['CINDER_USER'] }}
      CINDER_PASS: {{ pillar['CINDER']['CINDER_PASS'] }}
      MY_IP:{{ salt['network.ip_addrs ']('ens160') }}
      RABBITMQ_HOST: {{ pillar['nova']['RABBITMQ_HOST'] }}
      RABBITMQ_PORT: {{ pillar['nova']['RABBITMQ_PORT'] }}
      RABBITMQ_USER: {{ pillar['nova']['RABBITMQ_USER'] }}
      RABBITMQ_PASS: {{ pillar['nova']['RABBITMQ_PASS'] }}
      NOVNC_PROXY_URL: {{ pillar['nova']['NOVNC_PROXY_URL'] }}
      AUTH_KEYSTONE_HOST: {{ pillar['nova']['AUTH_KEYSTONE_HOST'] }}
      AUTH_KEYSTONE_PORT: {{ pillar['nova']['AUTH_KEYSTONE_PORT'] }}
      AUTH_KEYSTONE_PROTOCOL: {{ pillar['nova']['AUTH_KEYSTONE_PROTOCOL'] }}
      AUTH_ADMIN_PASS: {{ pillar['nova']['AUTH_ADMIN_PASS'] }}
      MYSQL_SERVER: {{ pillar['nova']['MYSQL_SERVER'] }}
      
cinder-data-init:
  file.managed:
    - name: /usr/local/bin/cinder_data.sh
    - source: salt://openstack/cinder/files/cinder_data.sh
    - mode: 755
    - user: root
    - group: root
    - template: jinja
    - defaults:
      ADMIN_PASSWD: {{ pillar['CINDER']['ADMIN_PASSWD'] }} 
      CONTROL_IP: {{ pillar['CINDER']['CONTROL_IP'] }}
      CINDER_USER: {{ pillar['CINDER']['CINDER_USER'] }}
      CINDER_PASS: {{ pillar['CINDER']['CINDER_PASS'] }}
    - watch_in:
      service: cinder-api
  cmd.run:
    - name: bash /usr/local/bin/cinder_data.sh && touch /var/run/cinder-datainit.lock
    - require:
      - service: cinder-api
      - service: cinder-scheduler
    - unless: test -f /var/run/cinder-datainit.lock

