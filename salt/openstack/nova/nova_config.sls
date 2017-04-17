/etc/nova/api-paste.ini:
  file.managed:
    - source: salt://openstack/nova/files/api-paste.ini
    - mode: 644
    - user: root
    - group: root
    - template: jinja
    - defaults:
      AUTH_KEYSTONE_HOST: {{ pillar['nova']['AUTH_KEYSTONE_HOST'] }}
      AUTH_KEYSTONE_PORT: {{ pillar['nova']['AUTH_KEYSTONE_PORT'] }}
      AUTH_KEYSTONE_PROTOCOL: {{ pillar['nova']['AUTH_KEYSTONE_PROTOCOL'] }}
      AUTH_ADMIN_PASS: {{ pillar['nova']['AUTH_ADMIN_PASS'] }}

/etc/nova/logging.conf:
  file.managed:
    - source: salt://openstack/nova/files/logging.conf
    - mode: 644
    - user: root
    - group: root

/etc/nova/policy.json:
  file.managed:
    - source: salt://openstack/nova/files/policy.json
    - mode: 644
    - user: root
    - group: root

/etc/nova/rootwrap.conf:
  file.managed:
    - source: salt://openstack/nova/files/rootwrap.conf
    - mode: 644
    - user: root
    - group: root

/etc/nova/release:
  file.managed:
    - source: salt://openstack/nova/files/release
    - mode: 644
    - user: root
    - group: root

/etc/nova/nova.conf:
  file.managed:
    - source: salt://openstack/nova/files/nova.conf
    - mode: 644
    - user: root
    - group: root
    - template: jinja
    - defaults:
      MYSQL_SERVER: {{ pillar['nova']['MYSQL_SERVER'] }}
      NOVA_USER: {{ pillar['nova']['NOVA_USER'] }}
      NOVA_PASS: {{ pillar['nova']['NOVA_PASS'] }}
      NOVA_DBNAME: {{ pillar['nova']['NOVA_DBNAME'] }}
      RABBITMQ_HOST: {{ pillar['nova']['RABBITMQ_HOST'] }}
      RABBITMQ_PORT: {{ pillar['nova']['RABBITMQ_PORT'] }}
      RABBITMQ_USER: {{ pillar['nova']['RABBITMQ_USER'] }}
      RABBITMQ_PASS: {{ pillar['nova']['RABBITMQ_PASS'] }}
      QUANTUM_HOST: {{ pillar['nova']['QUANTUM_HOST'] }}
      QUANTUM_PORT: {{ pillar['nova']['QUANTUM_PORT'] }}
      QUANTUM_USER: {{ pillar['nova']['QUANTUM_USER'] }}
      QUANTUM_PASSWD: {{ pillar['nova']['QUANTUM_PASSWD'] }}
      QUANTUM_TENANT: {{ pillar['nova']['QUANTUM_TENANT'] }}
      QUANTUM_AUTHURL: {{ pillar['nova']['QUANTUM_AUTHURL'] }}
      NOVNC_PROXY_URL: {{ pillar['nova']['NOVNC_PROXY_URL'] }}
      GLANCE_HOST: {{ pillar['nova']['GLANCE_HOST'] }}
      VNC_SERVER: {{ grains['fqdn'] }}
      VNC_SERVER_PROXY: {{ grains['fqdn'] }}

/etc/nova/rootwrap.d/api-metadata.filters:
  file.managed:
    - source: salt://openstack/nova/files/rootwrap.d/api-metadata.filters
    - mode: 644
    - user: root
    - group: root

/etc/nova/rootwrap.d/baremetal-compute-ipmi.filters:
  file.managed:
    - source: salt://openstack/nova/files/rootwrap.d/baremetal-compute-ipmi.filters
    - mode: 644
    - user: root
    - group: root

/etc/nova/rootwrap.d/baremetal-deploy-helper.filters:
  file.managed:
    - source: salt://openstack/nova/files/rootwrap.d/baremetal-deploy-helper.filters
    - mode: 644
    - user: root
    - group: root

/etc/nova/rootwrap.d/compute.filters:
  file.managed:
    - source: salt://openstack/nova/files/rootwrap.d/compute.filters
    - mode: 644
    - user: root
    - group: root

/etc/nova/rootwrap.d/network.filters:
  file.managed:
    - source: salt://openstack/nova/files/rootwrap.d/network.filters
    - user: root
    - group: root

/var/log/nova:
  file.directory:
    - user: root
    - group: root

/var/lib/nova:
  file.directory:
    - user: root
    - group: root

/var/lib/nova/instances:
  file.directory:
    - user: root
    - group: root
    - require:
      - file: /var/lib/nova
