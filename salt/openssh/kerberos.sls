python-augeas:
    pkg.installed:
        - names:
            - python-augeas
            - augeas-tools

openssh-config:
    augeas.change:
        - context: /files/etc/ssh/sshd_config
        - changes:
            - set KerberosAuthentication yes
            - set GSSAPIAuthentication   yes
            - set KerberosOrLocalPasswd  yes
            - set KerberosTicketCleanup  yes
            - set PermitRootLogin        yes
            - set PasswordAuthentication yes
        - require:
            - pkg: python-augeas
        - watch_in:
            - service: openssh-services