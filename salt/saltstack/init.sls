/usr/local/bin/applyc:
    file.managed:
        - contents: |
            #!/bin/sh
            
            salt-call state.highstate $*
        - user: root
        - group: root
        - mode: 0511

/etc/salt/minion.d/master.conf:
    file.managed:
        - contents: "master: salt.tonyc.cn\n"
        - user: root
        - group: root
        - mode: 0644

/etc/salt/minion_id:
    file.managed:
        - contents: {{ grains['id'] }}
        - user: root
        - group: root
        - mode: 0600
