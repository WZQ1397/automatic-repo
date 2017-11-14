{{% set ZOO_HOME=/zookeeper/ %}}
{% for item in ['zoo.cfg','log4j.properties'] %}}
{{ ZOO_HOME }}conf/{{ item }}:
  file.managed:
    - source: salt://HADOOP/etc/{{ item }}
    - user: root
    - group: root
    - mode: '0755'
{{% endfor %}}
