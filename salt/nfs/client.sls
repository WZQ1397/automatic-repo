# NFS Client states
nfs_client:
  pkg.installed:
    - name: nfs-common

#imapd_conf:
#  file.managed:
#    - name: /etc/idmapd.conf
#    - source: salt://nfs/server/idmapd.conf
#    - user: root
#    - group: root
#    - mode: 644
#    - require:
#      - pkg: nfs-common
