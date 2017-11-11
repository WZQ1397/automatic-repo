{{% set taokeeper = taokeeper %}}
{{% set taokeeper_mon = taokeeper-monitor-config.properties %}}

/etc/salt/minion.d/taokeeper-minion.conf:
 	file.managed:
    - source: salt://HADOOP/taokeeper/taokeeper-minion.conf

{{ taokeeper }}:
  mysql_database.present
  file.managed:
    - name: /tmp/taokeeper.sql
    - source: salt://HADOOP/taokeeper/taokeeper.sql
  mysql_query.run
    - database: {{ taokeeper }}
    - query:    "source /tmp/taokeeper.sql"
    
 /etc/salt/minion.d/{{ taokeeper_mon }}:
 	file.managed:
    - source: salt://HADOOP/taokeeper/{{ taokeeper_mon }}
