{{% set HADOOP_HOME=/etc/hadoop/ %}}
{{ HADOOP_HOME }}/etc/hdfs-site.xml:
  file.managed:
    - source: salt://HADOOP/etc/hdfs-site.xml
    - user: root
    - group: root
    - mode: '0755'

{{ HADOOP_HOME }}/etc/core-site.xml:
  file.managed:
    - source: salt://HADOOP/etc/core-site.xml
    - user: root
    - group: root
    - mode: '0755'

