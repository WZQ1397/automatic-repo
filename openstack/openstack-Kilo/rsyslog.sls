/etc/rsyslog.d/openstack.conf:
    file.managed:
        - source: salt://files/openstack/rsyslog/openstack.conf
        - user: root
        - group: root
        - mode: 0644
