{%
    set packages = {
        'debian': 'libkrb5-3',
        'ubuntu': 'libkrb5-3',
        'redhat': 'krb5-libs',
        'centos': 'krb5-libs',
        'openbsd': None
    }
%}

{%
    set configs = {
        'debian'    : '/etc/krb5.conf',
        'ubuntu'    : '/etc/krb5.conf',
        'redhat'    : '/etc/krb5.conf',
        'centos'    : '/etc/krb5.conf',
        'openbsd'   : '/etc/kerberosV/krb5.conf'
    }
%}

kerberos-library-packages:
    pkg.installed:
        - name: {{packages[grains.os|lower]}}

kerberos-library-config:
    file.managed:
        - name: {{configs[grains.os|lower]}}
        - source:
            - salt://services/kerberos/krb5.{{grains.nodename|lower}}.conf
            - salt://services/kerberos/krb5.{{grains.os|lower}}.conf
            - salt://services/kerberos/krb5.conf
        - require:
            - pkg: kerberos-library-packages