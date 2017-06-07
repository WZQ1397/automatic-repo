{% set app_name = 'kafka-mesos' -%}
{% set kafka_home = salt['system.home_dir'](app_name) -%}
{% set kafka = pillar[app_name] -%}

{% set zk_str = salt['zookeeper.ensemble_address']() -%}
{% set api_url = 'http://$HOST:$PORT0' -%}
{% set config = {'api': api_url, 'master': 'zk://{0}/mesos'.format(zk_str), 'zk': zk_str} -%}
{% do config.update(kafka.get('schedulerConfiguration', {})) -%}
{% set cmd_line = salt['kafka.format_options'](config) -%}

{% set kafka_command = 'chmod u+x ./kafka-mesos.sh && ./kafka-mesos.sh scheduler {0}'.format(cmd_line) %}

{% from 'marathon/deploy.sls' import service_deploy with context -%}
{{ service_deploy({'id': app_name, 'cmd': kafka_command}) }}

{% set broker_instances = kafka.get('brokerInstances', 1) -%}
{% set broker_config = kafka.get('brokerConfiguration', {}) -%}
{% set broker_meta = {'instances': broker_instances} -%}
{% set tmp_dir = pillar['system']['tmp'] -%}

{% if kafka['jmxPort'] is defined %}
{% set jmx = ' -Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false -Dcom.sun.management.jmxremote.port={0}'.format(kafka['jmxPort']) -%}
{% set new_config = {'jvmOptions': broker_config['jvmOptions'] + jmx }%}
{% do broker_config.update(new_config) -%}
{% endif %}

{% do broker_meta.update(broker_config) -%}

broker-configuration:
  file.managed:
    - name: {{ tmp_dir }}/kafka-mesos-broker-config.json
    - source: salt://kafka/files/kafka-mesos-broker-config.json
    - user: root
    - group: root
    - mode: 755
    - template: jinja
    - context:
        config: {{ broker_meta | yaml  }}

broker-reconfigure:
  module.wait:
    - name: kafka.reconfigure
    - config: {{ broker_config | yaml }}
    - no_of_instances: {{ broker_instances }}
    - require:
      - module: run-service-deploy-kafka-mesos
      - module: run-service-redeploy-kafka-mesos
    - watch:
      - file: broker-configuration
