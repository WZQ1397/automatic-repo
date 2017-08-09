include:
    - .service

#novnc:
#    pkg.installed:
#        - names:
#            - novnc
#            - nova-ajax-console-proxy
#            - nova-doc
#            - python-novaclient

nova-ssh-pubkey:
  ssh_auth.present:
    - user: nova
    - source: salt://utils/openstack/nova/id_rsa.pub

/var/lib/nova/.ssh/id_rsa:
  file.managed:
    - user: nova
    - source: salt://utils/openstack/nova/id_rsa
    - user: nova
    - group: nova
    - mode: '0600'