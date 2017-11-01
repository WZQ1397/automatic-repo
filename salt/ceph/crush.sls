/usr/local/bin/update_crush_map:
    file.managed:
        - source: salt://services/ceph/_files/update_crush_map
        - user: root
        - group: root
        - mode: '0700'
        - require:
            - pkg: ceph
    cmd.wait:
        - require:
            - file: /usr/local/bin/update_crush_map
        #- watch:
        #    - file: /etc/ceph/.crush

# /etc/ceph/.crush:
#     file.managed:
#         #- source: salt://states/ceph/_files/crush.rules
#         - user: root
#         - group: root
#         - mode: '0600'