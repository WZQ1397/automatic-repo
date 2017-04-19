include:
  - openstack.pre.control

cinder-install:
  pkg.installed:
    - pkgs:
      - lvm
      - cinder-volume

/etc/cinder/cinder.conf:
  file.managed:
    - source: salt://openstack/cinder/files/storge/cinder.conf
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

/dev/{{DISK}}:
  lvm.pv_present

my_vg:
  lvm.vg_present:
    - devices: /dev/{{DISK}}

cinder-reload:
  cmd.run:
    - names: |
      service tgt restart
      service cinder-volume restart