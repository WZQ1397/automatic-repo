/etc/selinux/config:
    file.sed:
        - before: enforcing
        - after: disabled
        - limit: ^SELINUX=

disable_selinux:
    cmd.wait:
        - name: setenforce 0
        - watch:
            - file: /etc/selinux/config