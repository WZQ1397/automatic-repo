{% set filepath = 'system/files/repo' %}
repo-get:
  file.managed:
    {% if grains['os_family'] == 'RedHat' %}
    - name: /etc/yum.repo.d/CentOS-Base-163.repo
    - source: 
      {% if grains['osmajorrelease'] == '7' %}
      - salt://{{ filepath }}/CentOS7-Base-163.repo
      {% elif grains['osmajorrelease'] == '6' %}
      - salt://{{ filepath }}/CentOS6-Base-163.repo
      {% else %}
      - salt://{{ filepath }}/CentOS5-Base-163.repo
      {% endif %}
    - name: /etc/yum.repo.d/CentOS-epel.repo
    - source:
      - salt://{{ filepath }}/epel.repo
    {% endif %}
    {% if grains['os_family'] == 'Debian' or grains['os_family'] == 'Ubuntu' %}
    - name: /etc/apt/apt.conf.d/{{ grains['os'] }}-lts.list
    - source: 
      {% if grains['osmajorrelease'] == '7' %}
      - salt://{{ filepath }}/debian7-lts.list
      {% elif grains['osmajorrelease'] == '6' %}
      - salt://{{ filepath }}/debian6-lts.list
      {% elif grains['osmajorrelease'] > 14 %}
      - salt://{{ filepath }}/sources.trusty.list
      {% else %}
      - salt://{{ filepath }}/ubuntu1204-lts.list
      {% endif %}
    {% endif %}
    - user: root
    - group: root
    - mode: 644

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
