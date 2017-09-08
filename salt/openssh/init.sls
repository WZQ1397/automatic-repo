{%
    set packages = {
        'debian' : ['openssh-server', 'openssh-client'],
        'ubuntu' : ['openssh-server', 'openssh-client'],
        'centos' : ['openssh']
    }
%}

{%
    set services = {
        'debian' : 'ssh',
        'ubuntu' : 'ssh',
        'centos' : 'sshd',
        'redhat' : 'sshd'
    }
%}


openssh-packages:
    pkg.installed:
        - names: {{packages[grains.os|lower]}}

openssh-services:
    service.running:
        - name: {{services[grains.os|lower]}}
        - enable: True
        - require:
            - pkg: openssh-packages
            
openssh_root_keys:
    ssh_auth.present:
        - user: root
        - enc: ssh-rsa
        - source: salt://services/openssh/root.key.pub
        - require:
            - pkg: openssh-packages