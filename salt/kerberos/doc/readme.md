1.默认安装路径为 /etc/krb5kdc
etc/krb5.conf
 |
  -- etc/krb5kdc/kdc.conf

etc/krb5.conf
[kdc] kdc位置
[logging]日志位置 
[libdefaults]默认域
[realms]   kerberos域，表示KDC所管辖的范围；


2.etc/krb5kdc/kadm5.acl 若没有此文件则自己创建
> */admin@LOCAL.DOMAIN  *

3.创建 kerberos 数据库
$ /usr/sbin/kdb5_util create -r LOCAL.DOMAIN -s

创建数据库到/etc/krb5kdc/principal

Principal 是由三个部分组成：名字（name），实例（instance），REALM（域）。比如一个标准的 Kerberos 的用户是：name/instance@REALM 

4.登录 kerberos 
`$ /usr/sbin/kadmin.local`   
查看用户
`kadmin.local   ： listprincs`
添加用户
`kadmin.local   ： addprinc kadmin/admin@LOCAL.DOMAIN`
删除用户
`kadmin.local   ： delprinc kadmin/admin@LOCAL.DOMAIN`
创建keytable文件  生成 kadmin/admin kadmin/changepw 两个用户的 keytab 文件到 krb5kdc 目录
kadmin.local ：ktadd -k /etc/krb5kdc/kadm5.keytab kadmin/admin kadmin/changepw
注意：keytab 得与配置文件kdc.conf里面配置一致


5、重启krb5kdc和kadmind进程 
```shell
/usr/sbin/kadmind 
/usr/sbin/krb5kdc 
```

6、运行kerberos
```shell
$ sudo /usr/sbin/krb5kdc
$ sudo /usr/sbin/kadmind
```

7、在KDC服务器上测试申请票据，测试票据请求 
```shell
$ /usr/sbin/kadmin.local 
$ kadmin.local: addprinc linlin@LOCAL.DOMAIN
提示创建密码，然后退出 
$ su linlin 
$ kinit  linlin@LOCAL.DOMAIN
$ klist 
$ /usr/sbin/kadmin.local 
$ kadmin.local: addprinc -randkey hdfs/LL-167@LOCAL.DOMAIN 
ktadd -norandkey -k hdfs.keytab hdfs/LL-167
```
查看自己申请的票据 

PS:http://blog.csdn.net/tonyhuang_google_com/article/details/40861179