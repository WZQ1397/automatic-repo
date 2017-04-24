neutron-pkg:
  pkg.installed:
    - pkgs:
        - neutron-server neutron-plugin-ml2
        - neutron-linuxbridge-agent
        - neutron-l3-agent
        - neutron-dhcp-agent
        - neutron-metadata-agent
    
neutron-mysql:
  mysql_database.present:
    - name: {{ pillar['neutron']['NEUTRON_DBNAME'] }}
    - require:
      - service: mysql-server
  mysql_user.present:
    - name: {{ pillar['neutron']['NEUTRON_USER'] }}
    - host: {{ pillar['neutron']['HOST_ALLOW'] }}
    - password: {{ pillar['neutron']['NEUTRON_PASS'] }}
    - require:
      - mysql_database: neutron-mysql
  mysql_grants.present:
    - grant: all
    - database: {{ pillar['neutron']['DB_ALLOW'] }}
    - user: {{ pillar['neutron']['NEUTRON_USER'] }}
    - host: {{ pillar['neutron']['HOST_ALLOW'] }}
    - require:
      - mysql_user: neutron-mysql

