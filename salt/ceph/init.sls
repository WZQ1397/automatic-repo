include:
    - .release

ceph: 
    pkg.installed

# ceph-mds:
#     pkg.installed

/lib/udev/rules.d/95-ceph-osd.rules.disabled:
    file.rename:
        - source: '/lib/udev/rules.d/95-ceph-osd.rules'
        - force: True
        
/usr/local/bin/ceph-osd-rm:
    file.managed:
        - contents: |
            #/bin/sh
            
            ceph osd down $1
            ceph osd out $1
            ceph osd crush  rm osd.$1
            ceph auth del osd.$1
            ceph osd rm $1

            echo 'ok'
        - user: root
        - group: root
        - mode: '0755'
        - require:
            - pkg: ceph

#ceph:
#    group.present:
#        - gid: 2000
#    user.present:
#        - createhome: True
#        - home: /home/ceph
#        - shell: /bin/bash
#        - uid: 2000
#        - gid: 2000
#        - groups:
#            - ceph
#        - password: $6$iR/1KpVq$ACa8wRvP1eKnvIrwVwCdxmkC3ayLdt5jRPSv6indxjgDxFlke2iOCE2.8GObTkx9RWZcOCEENFOLoIbk9AZ0U1        
#        - enforce_password: True
#        - requires:
#            - ceph
#
#/etc/sudoers.d/ceph:
#    file.managed:
#        - contents: "ceph ALL = (root) NOPASSWD:ALL\n"