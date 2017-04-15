# Add more static hosts bellow
salt_host:
  host.present:
    - name: SaltMas1
    - ip: 172.16.10.119

master_host:
  host.present:
    - name: SaltMas2
    - ip: 172.16.10.115

storge_host1:
  host.present:
    - name: GlusterFSnode1
    - ip: 192.168.6.112

storge_host2:
  host.present:
    - name: GlusterFSnode2
    - ip: 192.168.6.113
    
172.16.6.214:
  host.present:
    - hostnames:
      - yz3ctrl1
      - yz3ctrl1.dev.tonyc.cn
      - yz3ctrl1.prod.tonyc.cn