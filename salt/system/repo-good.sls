{% set source = {'RedHat': {  '7': '/CentOS7-Base-163.repo',
                              '6': '/CentOS6-Base-163.repo',
                              '5': '/CentOS5-Base-163.repo',}.get(grains.osmajorrelease),
                 'Debian': {  '7': '/debian7-lts.list',
                              '6': '/debian6-lts.list',}.get(grains.osmajorrelease),
                 'Ubuntu': { '16': '/sources.trusty.list',
                             '14': '/sources.trusty.list',
                             '12': '/ubuntu1204-lts.list',}.get(grains.osmajorrelease)}.get(grains.os) %}
                             
{% set dst = {'RedHat': '/etc/yum.repo.d/CentOS-Base-163.repo',
              'Debian': '/etc/apt/apt.conf.d/Debian-Ubuntu-lts.list',}.get(grains.os_family) %}
              
{% set epel6src = '/epel-6.repo' %}
{% set epel6dst = '/etc/yum.repo.d/CentOS-epel-6.repo' %}

{% set epel7src = '/epel-7.repo' %}
{% set epel7dst = '/etc/yum.repo.d/CentOS-epel-7.repo' %}

repo-get:
  file.managed:
    - name: {{ dst }}
    - source: 
      - salt://system/files/repo{{ source }}
    - user: root
    - group: root
    - mode: 644

{% if grains['os_family'] == 'RedHat' %}
  {% if grains['osmajorrelease'] == '6' %}
  epel-get:
    file.managed:
      - name: {{ epel6dst }}
      - source:
        - salt://{{ epel6src }}
  {% else %}
  epel-get:
    file.managed:
      - name: {{ epel7dst }}
      - source:
        - salt://{{ epel7src }}
{% endif %}

apt-get-update:
  cmd.run:
    {% if grains['os_family'] == 'RedHat' %}
    - name: yum update
    {% elif grains['os_family'] == 'Debian' or grains['os_family'] == 'Ubuntu' %}
    - name: apt-get update
    {% else %}
    - name: echo "not unix"
    {% endif %}
    - require:
      - cmd: repo-get
