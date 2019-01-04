# UCarp
# 只能监控到机器的存活，不能监控到服务，如果服务停了，但机器还是正常运转，它就没有办法拉
## Start UCarp
# https://download.pureftpd.org/pub/ucarp/

* vip: 10.0.0.10
* node1: 10.0.0.11
* node2: 10.0.0.12

### On node 10.0.0.11

```
ucarp --interface=eth0 --srcip=10.0.0.11 --vhid=10 --pass=10.0.0.10 --addr=10.0.0.10 --upscript=/etc/vip-up.sh --downscript=/etc/vip-down.sh
```

### On node 10.0.0.12

```
ucarp --interface=eth0 --srcip=10.0.0.12 --vhid=10 --pass=10.0.0.10 --addr=10.0.0.10 --upscript=/etc/vip-up.sh --downscript=/etc/vip-down.sh
```
