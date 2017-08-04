{%
    set url = salt['grains.filter_by']({
        'Debian' : 'http://repo.zabbix.com/zabbix/3.2/debian/pool/main/z/zabbix-release/zabbix-release_3.2-1+jessie_all.deb',
        'Ubuntu' : 'http://repo.zabbix.com/zabbix/3.2/ubuntu/pool/main/z/zabbix-release/zabbix-release_3.2-1+xenial_all.deb',
        'Redhat' : 'http://repo.zabbix.com/zabbix/3.2/rhel/7/x86_64/zabbix-release-3.2-1.el7.noarch.rpm',
        'Centos' : 'http://repo.zabbix.com/zabbix/3.2/rhel/7/x86_64/zabbix-release-3.2-1.el7.noarch.rpm',
    }, grain='os')
%}

{% set updatetype = salt['grains.filter_by']({
        'RedHat': 'yum',
        'Debian': 'apt-get',
    },grain='os_family')
%}

zabbix_apt_update:
    cmd.wait:
        - name: {{ updatetype }} update

zabbix-release:
    pkg.installed:
        - sources:
            - zabbix-release: {{url}}
        - watch_in:
            - cmd: zabbix_apt_update