{% if grains['os'] == 'Ubuntu' %}
ubuntukey-add:
  cmd.run:
    - name: wget -O - https://repo.saltstack.com/apt/ubuntu/{{ grains.os_family }}.04/amd64/2016.11/SALTSTACK-GPG-KEY.pub | sudo apt-key add -
  file.append:
    - name: /etc/apt/sources.list
    - text: deb http://repo.saltstack.com/apt/ubuntu/16.04/amd64/2016.11 xenial main
{% endif %}

{% if grains['os'] in ['Centos','Redhat'] %}
rhel-pre:
  cmd.run:
    - name: rpm -e --nodeps python2-pycryptodomex
  pkg.installed:
    - pkgs: 
      - python-crypto
      - https://repo.saltstack.com/yum/redhat/salt-repo-2016.11-2.el{{ grains.os_family }}.noarch.rpm
{% endif %}

repo-update:
  cmd.run:
    {% if grains['os'] in ['Centos','Redhat'] %}
    - name: yum clean expire-cache && yum update
    - require:
      - pkg: python-crypto
    {% endif %}
    {% if grains['os'] == 'Ubuntu' %}
    - name: apt-get update
    {% endif %}
  
salt-master:
  pkg:
    - installed
  service.running:
    - enable: True
    - require:
      - pkg: salt-master
    - watch:
      - file: /etc/salt/master.d/

/etc/salt/master.d/:
  file.recurse:
    - source: salt://saltstack/_files/
    - dir_mode: '0755'
    - file_mode: '0644'
    - user: root
    - group: root
    - clean: True
    