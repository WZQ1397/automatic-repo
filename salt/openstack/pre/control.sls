software-properties-common:
  pkg.installed: []

/etc/apt/sources.list.d/aliyun.list:
  file.managed:
    - source: salt://openstack/pre/file/ubuntu1404-lts.list

/etc/hosts:
  file.managed:
    - source: salt://openstack/pre/file/hosts

repo_get:
  pkg.installed:
   - pkgs:
     - python-software-properties
     - software-properties-common

openstack_repo_install:
  cmd.run:
    - name: add-apt-repository cloud-archive:ocata
	
repo_update:
  cmd.run:
    - name: apt update && apt dist-upgrade

pre_install:
  pkg.installed:
    - pkgs:
      - python-openstackclient
      - rabbitmq-server
      - memcached
      - python-memcache

mysql_install:
  pkg.installed:
    - pkgs:
        - mariadb-server
        - python-pymysql

mysql_manage_file:
  file.managed:
    - name: /etc/mysql/mariadb.conf.d/99-openstack.cnf 
    - source: salt://openstack/pre/file/99-openstack.cnf
    - user: root
    - group: root
    - file_mode: 644
    - template: jinja
    - context:
      IP_ADDR: {{ pillar['horizon']['CONTROL_IP'] }}
    - require:
      - pkg: mysql_install

mysql_ser:
  cmd.run:
    - name: service mysql status > my.log
    - require:
      - pkg: pre_install
  cmd.run:
    - name: service mysql restart
    - require:
      - pkg: pre_install

/tmp/mysql_auto_file:
  file.managed:
    - source: salt://openstack/pre/file/mysql_auto.reply

mysql_sec_install:
  cmd.run:
    - name: mysql_secure_installation < /tmp/mysql_auto.reply

rabbitmq_priv:
  cmd.run:
    - name: rabbitmqctl add_user openstack edong;rabbitmqctl set_permissions openstack ".*" ".*" ".*" 
    - require:
      - pkg: pre_install

/etc/memcached.conf:
  file.replace:
    - pattern: "-l 127.0.0.1"
    - repl: "{{ pillar['horizon']['CONTROL_IP'] }}"
    - require:
      - pkg: pre_install
  cmd.run:
    - name: service memcached restart
    - require:
      - pkg: pre_install

ntp-install:
  pkg.installed:
    - names: 
      - ntp

ntpdate times.aliyun.com >> /dev/null:
  cron.present:
    - user: root
    - minute: '*/30'

