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