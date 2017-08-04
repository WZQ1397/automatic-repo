include:
    - services.mysql
    - .agent

zabbix-server:
    pkg.installed:
        - names:
            - snmp
            - snmp-mibs-downloader
            - zabbix-server-mysql
            - zabbix-frontend-php
        - require:
            - pkg: mysql-server
            - pkg: zabbix-release
    service.running:
        - enable: True
        - require:
            - pkg: zabbix-server-mysql

# see http://php.net/manual/en/timezones.asia.php
/etc/zabbix/apache.conf:
    file.sed:
        - before: '# php_value date.timezone Europe/Riga'
        - after: 'php_value date.timezone Asia/Shanghai'
        - limit: 'date.timezone'
        - require:
            - pkg: zabbix-frontend-php

/usr/share/zabbix/include/locales.inc.php:
    file.sed:
        - require:
            - pkg: zabbix-frontend-php
        - before: 'false'
        - after: 'true'
        - limit: 'zh_CN.*display'