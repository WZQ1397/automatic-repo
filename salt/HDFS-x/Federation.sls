{{% set HADOOP_HOME=/etc/hadoop/ %}}

{{% for item in ['hdfs-site','core-site','yarn-site'] %}}
{{ HADOOP_HOME }}/etc/{{ item }}.xml:
  file.managed:
    - source: salt://HADOOP/etc/{{ item }}-Federation.xml
    - user: root
    - group: root
    - mode: '0755'
{{% endfor %}}

{{ HADOOP_HOME }}/etc/mapred-site.xml:
  file.managed:
    - source: salt://HADOOP/etc/mapred-site.xml.yarnmode
    - user: root
    - group: root
- mode: '0755'
