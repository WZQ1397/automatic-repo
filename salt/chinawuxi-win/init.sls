D:\webhome:
    file.directory:
        - names:
            - D:\webhome
            - D:\webhome\weixinb.chinawuxi.cn
            - D:\webhome\weixina.chinawuxi.cn
            - D:\webhome\weixin.chinawuxi.cn
            - D:\webhome\phone.chinawuxi.cn
            - D:\webhome\app.chinawuxi.cn
            - D:\webhome\wxhailiang.chinawuxi.cn
            - D:\webhome\wxyzx.chinawuxi.cn
            - D:\software

D:\software\php-5.2.17-Win32-VC6-x86.zip:
    file.managed:
        - source: http://mirrors.hwdzsw.net/public/software/php-5.2.17-Win32-VC6-x86.zip
        - source_hash: sha1=23e1cf2f6e1bf64585ae921462340e5748fcc939

D:\software\mysql-5.6.17-win32.msi:
    file.managed:
        #- source: http://cdn.mysql.com/Downloads/MySQL-5.6/mysql-5.6.17-win32.zip
        - source: http://mirrors.hwdzsw.net/public/software/mysql-5.6.17-win32.msi
        - source_hash: sha1=e1531590aee01acb771b2040c7631f8794c4696d 

D:\software\mysql-installer-web-community-5.6.17.0.msi:
    file.managed:
        - source: http://cdn.mysql.com/Downloads/MySQLInstaller/mysql-installer-web-community-5.6.17.0.msi
        - source_hash: md5=a725d668da1b9da064e6ae2a8170e9d7 

D:\software\ProcessExplorer.zip:
    file.managed:
        - source: http://mirrors.hwdzsw.net/public/software/ProcessExplorer.zip
        - source_hash: sha1=77bce4b61a0112c743c43ed0935842bb5515f573

D:\software\FileZilla_Server-0_9_44.exe:
    file.managed:
        - source: http://mirrors.hwdzsw.net/public/software/FileZilla_Server-0_9_44.exe
        - source_hash: sha1=2e81cba242fda8146ae61a077d45353fa31d1edf

D:\software\AspNetMVC3ToolsUpdateSetup.exe:
    file.managed:
        - source: http://mirrors.hwdzsw.net/public/software/AspNetMVC3ToolsUpdateSetup.exe
        - source_hash: sha1=7a15ca7a49ac8a9edfe71ac0873a8aa38338c029

D:\software\AspNetMVC3ToolsUpdateSetup_CHS.exe:
    file.managed:
        - source: http://mirrors.hwdzsw.net/public/software/AspNetMVC3ToolsUpdateSetup_CHS.exe
        - source_hash: sha1=d7a97764f7a653684f31e3b239e0501be1ec80e7



#pool-weixin.chinawuxi.cn:
#    cmd.run:
#        - name: C:\windows\system32\inetsrv\appcmd.exe add apppool -name:weixin.chinawuxi.cn  -managedRuntimeVersion:"v4.0"
#        - unless: c:\windows\system32\inetsrv\appcmd.exe list apppool -name:weixin.chinawuxi.cn

#pool-wcf.phone.chinawuxi.cn:
#    cmd.run:
#        - name: C:\windows\system32\inetsrv\appcmd.exe add apppool -name:wcf.phone.chinawuxi.cn  -managedRuntimeVersion:"v4.0"
#        - unless: c:\windows\system32\inetsrv\appcmd.exe list apppool -name:wcf.phone.chinawuxi.cn

{% for pool in ['phone.chinawuxi.cn', 'weixin.chinawuxi.cn', 'app.chinawuxi.cn', 'weixina.chinawuxi.cn', 'weixinb.chinawuxi.cn', 'wxhailiang.chinawuxi.cn', 'wxyzx.chinawuxi.cn'] %}
pool-{{pool}}:
    cmd.run:
        - name: C:\windows\system32\inetsrv\appcmd.exe add apppool -name:{{pool}}  -managedRuntimeVersion:"v4.0"
        - unless: c:\windows\system32\inetsrv\appcmd.exe list apppool -name:{{pool}}

setpool-{{ pool }}:
    cmd.run:
        - name: >
            C:\windows\system32\inetsrv\appcmd.exe set app "{{ pool }}/" /applicationPool:"{{ pool }}"
        - unless: C:\windows\system32\inetsrv\appcmd.exe list app /apppool.name:"{{ pool }}" | find "{{ pool }}/" 
        - require:
            - cmd: {{ pool }}
{% endfor %}

phone.chinawuxi.cn:
    cmd.run:
        - name: >
            C:\windows\system32\inetsrv\appcmd.exe add site 
            /id:2 
            /name:"phone.chinawuxi.cn"
            /bindings:http://phone.chinawuxi.cn:80 
            /physicalPath:"D:\webhome\phone.chinawuxi.cn"
        - unless: C:\windows\system32\inetsrv\appcmd.exe list site /id:2 
        - require:
            - file: D:\webhome\phone.chinawuxi.cn
            - cmd: pool-phone.chinawuxi.cn

weixin.chinawuxi.cn:
    cmd.run:
        - name: >
            C:\windows\system32\inetsrv\appcmd.exe add site 
            /id:3 
            /name:"weixin.chinawuxi.cn"
            /bindings:http://weixin.chinawuxi.cn:80 
            /physicalPath:"D:\webhome\weixin.chinawuxi.cn"
        - unless: C:\windows\system32\inetsrv\appcmd.exe list site /id:3
        - require:
            - file: D:\webhome\weixin.chinawuxi.cn

weixina.chinawuxi.cn:
    cmd.run:
        - name: >
            C:\windows\system32\inetsrv\appcmd.exe add site 
            /id:5 
            /name:"weixina.chinawuxi.cn"
            /bindings:http://weixina.chinawuxi.cn:80 
            /physicalPath:"D:\webhome\weixina.chinawuxi.cn"
        - unless: C:\windows\system32\inetsrv\appcmd.exe list site /id:5
        - require:
            - file: D:\webhome\weixina.chinawuxi.cn

weixinb.chinawuxi.cn:
    cmd.run:
        - name: >
            C:\windows\system32\inetsrv\appcmd.exe add site 
            /id:6
            /name:"weixinb.chinawuxi.cn"
            /bindings:http://weixinb.chinawuxi.cn:80 
            /physicalPath:"D:\webhome\weixinb.chinawuxi.cn"
        - unless: C:\windows\system32\inetsrv\appcmd.exe list site /id:6
        - require:
            - file: D:\webhome\weixinb.chinawuxi.cn

app.chinawuxi.cn:
    cmd.run:
        - name: >
            C:\windows\system32\inetsrv\appcmd.exe add site 
            /id:4
            /name:"app.chinawuxi.cn"
            /bindings:http://app.chinawuxi.cn:80 
            /physicalPath:"D:\webhome\app.chinawuxi.cn"
        - unless: C:\windows\system32\inetsrv\appcmd.exe list site /id:4 
        - require:
            - file: D:\webhome\app.chinawuxi.cn
            - cmd: pool-app.chinawuxi.cn
            
wxhailiang.chinawuxi.cn:
    cmd.run:
        - name: >
            C:\windows\system32\inetsrv\appcmd.exe add site 
            /id:7
            /name:"wxhailiang.chinawuxi.cn"
            /bindings:http://wxhailiang.chinawuxi.cn:80 
            /physicalPath:"D:\webhome\wxhailiang.chinawuxi.cn"
        - unless: C:\windows\system32\inetsrv\appcmd.exe list site /id:7 
        - require:
            - file: D:\webhome\wxhailiang.chinawuxi.cn
            - cmd: pool-wxhailiang.chinawuxi.cn

wxyzx.chinawuxi.cn:
    cmd.run:
        - name: >
            C:\windows\system32\inetsrv\appcmd.exe add site 
            /id:8
            /name:"wxyzx.chinawuxi.cn"
            /bindings:http://wxyzx.chinawuxi.cn:80 
            /physicalPath:"D:\webhome\wxyzx.chinawuxi.cn"
        - unless: C:\windows\system32\inetsrv\appcmd.exe list site /id:8 
        - require:
            - file: D:\webhome\wxyzx.chinawuxi.cn
            - cmd: pool-wxyzx.chinawuxi.cn

