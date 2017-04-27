# Add ssh key to root account so it can deploy latest salt states
root:
  file.managed:
    - name: /root/.ssh/id_rsa
    - source: salt://users/keys/zach_dsa
    - mode: 600
    - makedirs: True

# Master users:
zach:
  user.present:
    - fullname: zach
    - shell: /bin/bash
    - home: /home/zach
    - groups:
      - sudo
  file.directory:
    - name: /home/zach/.ssh
    - user: zach
    - group: zach
    - mode: 755
    - makedirs: True
    - recurse:
      - user
      - group
    - require:
      - user: zach
  ssh_auth.present:
    - user: zach
    - source: salt://users/keys/zach_dsa.pub
    - require:
      - file: zach
