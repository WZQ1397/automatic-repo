/etc/prometheus.yml:
  file.managed:
    - source: salt://prometheus/prometheus.yml
    - user: root
    - dir_mode: 775
    - file_mode: '0644'

/etc/alertmanager/rules:
  file.directory:
    - user: root
    - group: root
    - dir_mode: 755
    - file_mode: 644
    - makedirs: True
    - recurse:
      - user
      - group
      - mode
  file.recurse:
    - source: salt://prometheus/rules/
    - user: root
    - dir_mode: 775
    - file_mode: '0644'
    
/etc/alertmanager/templates:
  file.directory:
    - user: root
    - group: root
    - dir_mode: 755
    - file_mode: 644
    - makedirs: True
    - recurse:
      - user
      - group
      - mode
  file.managed:
    - source: salt://prometheus/zach.tmpl
    - user: root
    - dir_mode: 775
    - file_mode: '0644'
    
/etc/alertmanager/alertmanager.yml:
  file.managed:
    - source: salt://prometheus/alertmanager.yml
    - user: root
    - dir_mode: 775
    - file_mode: '0644'


