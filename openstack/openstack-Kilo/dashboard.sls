memcached:
    pkg:
        - installed
    service.running:
        - enable: True
        - reload: True
        - watch:
            - file: /etc/memcached.conf
        - require:
            - pkg: memcached
apache2:
    pkg:
        - installed
    service.running:
        - enable: True
        - reload: True
        - watch:
            - file: /etc/apache2/*
            - file: /etc/openstack-dashboard
        - require:
            - pkg: apache2

libapache2-mod-wsgi:
    pkg:
        - installed

openstack-dashboard:
    pkg:
        - installed

/etc/openstack-dashboard:
    file.recurse:
        - source: salt://files/{{ grains['fqdn'] }}/openstack-dashboard/
        
/etc/memcached.conf:
    file.managed:
        - source: salt://files/{{ grains['fqdn'] }}/memcached.conf

/etc/apache2/empty:
    file.absent

