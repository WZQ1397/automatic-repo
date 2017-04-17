include:
  - openstack.nova.nova_config
  - openstack.nova.nova_compute_install

nova-compute-service:
  file.managed:
    - name: /etc/init.d/openstack-nova-compute
    - source: salt://openstack/nova/files/openstack-nova-compute
    - user: root
    - group: root
    - mode: 755
  cmd.run:
    - name: chkconfig --add openstack-nova-compute
    - unless: chkconfig --list | grep openstack-nova-compute
    - require:
      - file: nova-compute-service
  service.running:
    - name: openstack-nova-compute
    - enable: True
    - watch:
      - file: /etc/nova/api-paste.ini
      - file: /etc/nova/logging.conf
      - file: /etc/nova/policy.json
      - file: /etc/nova/rootwrap.conf
      - file: /etc/nova/release
      - file: /etc/nova/nova.conf
      - file: /etc/nova/rootwrap.d/api-metadata.filters
      - file: /etc/nova/rootwrap.d/baremetal-compute-ipmi.filters
      - file: /etc/nova/rootwrap.d/baremetal-deploy-helper.filters
      - file: /etc/nova/rootwrap.d/compute.filters
      - file: /etc/nova/rootwrap.d/network.filters
    - require:
      - cmd.run: nova-compute-install
      - cmd.run: nova-compute-service
      - file: /var/log/nova
      - file: /var/lib/nova/instances
