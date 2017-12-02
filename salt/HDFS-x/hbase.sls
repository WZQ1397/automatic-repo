{{% set HBASE_HOME=/hadoop/hbase %}}
{% for item in ['hbase-site.xml'] %}}
{{ HBASE_HOME }}conf/{{ item }}:
  file.managed:
    - source: salt://HADOOP/etc/{{ item }}
    - user: root
    - group: root
    - mode: '0755'
{{% endfor %}}
