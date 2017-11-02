# ceph-apt-key:
#     cmd.run:
#         - name: wget -q -O- 'https://ceph.com/git/?p=ceph.git;a=blob_plain;f=keys/release.asc' | sudo apt-key add -
#         - unless: apt-key list | grep 17ED316D

# /etc/apt/sources.list.d/ceph.list:
#     file.managed:
#         - contents: deb http://ceph.com/debian/ trusty main

# ceph_apt_update:
#     cmd.wait:
#         - name: 'apt-get update'
#         - watch:
#             - file: /etc/apt/sources.list.d/ceph.list

deb http://ceph.com/debian/ trusty main:
    pkgrepo.managed:
        - name: deb http://ceph.com/debian/ trusty main
        - file: /etc/apt/sources.list.d/ceph.list
        - key_url: 'https://raw.githubusercontent.com/ceph/ceph/master/keys/release.asc'
        #- key_url: 'https://ceph.com/git/?p=ceph.git;a=blob_plain;f=keys/release.asc'
        - order: 10

deb-src http://ceph.com/debian/ trusty main:
    pkgrepo.managed:
        - file: /etc/apt/sources.list.d/ceph.list
        #- key_url: 'https://raw.githubusercontent.com/ceph/ceph/master/keys/release.asc'
        #- key_url: 'https://ceph.com/git/?p=ceph.git;a=blob_plain;f=keys/release.asc'
        - order: 10

#ceph-packages:
#    pkg.installed:
#        - names:
#            - ceph
#            - ceph-mds
#            - ceph-common
#            - ceph-fs-common
#            - gdisk