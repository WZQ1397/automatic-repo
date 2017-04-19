include:
  - openstack.pre.control

software-properties-common:
  pkg.installed: []

openstack-dashboard:
  file.managed:
    - name: /etc/openstack-dashboard/local_settings.py
    - source: salt://openstack/pre/file/local_settings.py
    - template: jinja
    - defaults:
      CONTROL_IP: {{ pillar['horizon']['CONTROL_IP'] }}
    - require:
      - pkg: openstack-dashboard

/var/lib/openstack-dashboard/secret_key:
  file.managed:
    - user: www-data
    - group: www-data

