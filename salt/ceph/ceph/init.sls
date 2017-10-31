include:
    #- base:services.linux.ipmi
    #- base:services.linux.intel_me_disable
    - base: services.zabbix.agent
    - base: services.diamond
    - base: services.ceph
    - base: services.ceph.crush

extend:
    diamond-config:
        file.recurse:
            - source: salt://states/ceph/_files/diamond
            - saltenv: dev

/etc/ceph/.crush:
    file.managed:
        - source: salt://states/ceph/crush.rules
        - user: root
        - group: root
        - mode: '0600'
        - watch_in:
            - cmd: /usr/local/bin/update_crush_map

/etc/ceph:
    file.directory:
        - user: root
        - group: root
        - mode: '0755'

/etc/ceph/ceph.conf:
    file.managed:
        - user: root
        - group: root
        - mode: '0644'
        - require:
            - file: /etc/ceph

ceph_global_section:
    ini.sections_present:
        - name    : /etc/ceph/ceph.conf
        - sections:
            global:
                fsid                     : f9ec71ce-82c5-405f-b922-56c94b1d4ab5
                mon initial members      : s12
                mon host                 : 172.16.8.12:6789
                public network           : 172.16.8.0/24
                cluster network          : 172.16.9.0/24
                auth cluster required    : cephx
                auth service required    : cephx
                auth client required     : cephx
                osd journal size         : '10240'
                osd pool default size    : '2'
                filestore xattr use omap : 'true'
                mon clock drift allowed  : '1'
                ms nocrc                 : 'true'
                ms crc header            : 'true'
                ms crc data              : 'false'
                cephx sign messages      : 'false'
                #log to syslog            : 'true'
                #err to syslog            : 'true'
            osd:
                # !!!!!!!!!!!!!!!!!!
                #     very important, 
                #     disable /usr/libexec/ceph/ceph-osd-prestart.sh 
                # !!!!!!!!!!!!!!!!!!
                osd crush update on start             : '0'
                ms_dispatch_throttle_bytes            : '8589934592'
                filestore fd cache size               : '65535'
                filestore omap header cache size      : '2048'
                filestore wbthrottle enable           : 'false'
                filestore_queue_max_ops               : '60000'
                filestore_queue_max_bytes             : '8589934592'
                filestore_queue_committing_max_ops    : '60000'
                filestore_queue_committing_max_bytes  : '8589934592'
                journal_max_write_entries             : '60000'
                journal_max_write_bytes               : '8589934592'
                journal_queue_max_ops                 : '60000'
                journal_queue_max_bytes               : '8589934592'
                objecter_inflight_ops                 : '60000'
                objecter_infilght_op_bytes            : '8589934592'
                #osd_client_message_size_cap           : '8589934592'
                #osd_client_message_cap                : '8589934592'
                journal_force_aio                     : 'true'
                # osd_op_threads                        : '5'
                # filestore_op_threads                  : '5'
                # rbd_op_threads                        : '5'
            # osd.2:
            #     osd journal size         : '128'
            # osd.3:
            #     osd journal size         : '128'
        - require:
            - file: /etc/ceph/ceph.conf

/etc/ceph/ceph.client.admin.keyring:
    file.managed:
        - contents: |
            [client.admin]
                 key = AQD6Dr5UGPQMBRAABHN8Yzt1g7cFluiRhj8gHQ==
                 auid = 0
                 caps mds = "allow"
                 caps mon = "allow *"
                 caps osd = "allow *"
        - user: root
        - group: root
        - mode: '0600'
        - require:
            - file: /etc/ceph

/usr/local/bin/latency:
    file.managed:
        - source: salt://states/ceph/latency.py
        - mode: '0700'
        - user: 'root'
        - group: 'root'
