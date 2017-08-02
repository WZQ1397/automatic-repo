{% set mogopath = '/mongo/' %}

mongodb-src:
  archive.extracted:
    - name: {{ mogopath }}
    - source: https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-3.4.6.tgz
    - skip_verify: True

/root/.bashrc:
  file.append:
    - text:
      - 'export PATH={{ mogopath }}bin:$PATH'

mongodb-bin:
  file.managed:
    - name: {{ mogopath }}/link.sh
    - source: salt://mongodb/link.sh
    - user: root
    - group: root
    - mode: 0775

mongodb-exec:
  cmd.run:
    - name: /bin/bash {{ mogopath }}/link.sh
    - watch:
      file: {{ mogopath }}/link.sh
  file.directory:
    - name: /data/db
    - user: root
    - group: root
    - mode: 0775
    - recurse:
      - user
      - group
      - mode 
    


    
    

      
    

