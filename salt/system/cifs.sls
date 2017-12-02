cifs-utils:
    pkg.installed

/data/rootDir:
    mount.mounted:
        - device: //192.168.36.21/rootDir
        - fstype: cifs
        - opts: 
            - nosuid,noexec
            - uid=webapp,gid=root,dir_mode=0755,file_mode=0644
            - username=sharefile,password=ZgVj5pldYDgWrXSZ
            - ip=192.168.36.21
        - requires:
            - file: /data/rootDir
