nova-compute-packages:
    pkg.installed:
        - names:
            - nova-common
            - nova-compute-kvm
            - python-guestfs

nova-compute-services:
    service.running:
        - names:
            #- nova-api-metadata
            - nova-compute
        - enable: True
        - require:
            - pkg: nova-compute-kvm
            - file: /etc/nova
        - watch:
            - file: /etc/nova

/etc/nova:
    file.recurse:
        - source: salt://files/openstack/nova-compute
        - template: jinja
        - require:
            - pkg: nova-compute-packages
        - default:
            my_ip: 0.0.0.0

nova-ssh-pubkey:
  ssh_auth.present:
    - user: nova
    - source: salt://utils/openstack/nova/id_rsa.pub

/var/lib/nova/.ssh/id_rsa.pub:
  ssh_auth.present:
    - source: salt://utils/openstack/nova/id_rsa.pub
    - user: nova
    - group: nova
    - mode: '0600'

/var/lib/nova/.ssh/id_rsa:
  file.managed:
    - user: nova
    - source: salt://utils/openstack/nova/id_rsa
    - user: nova
    - group: nova
    - mode: '0600'

/var/lib/nova/.ssh/config:
    file.managed:
        - contents: |
            Host *
                StrictHostKeyChecking no
                UserKnownHostsFile=/dev/null
        - user: nova
        - group: nova