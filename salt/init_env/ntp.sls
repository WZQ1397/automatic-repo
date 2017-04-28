ntp:
  pkg.installed

ntpdate:
  pkg.installed

/etc/ntp.conf:
  file.managed:
    - source: salt://system/files/ntp.conf
    - user: root
    - group: root
    - mode: 644
    - template: jinja
    - require:
      - pkg: ntp
      - pkg: ntpdate

ntp-service:
  service.running:
    - name: ntp
    - enable: True
    - require:
      - pkg: ntp
      - pkg: ntpdate
    - watch:  
      - file: /etc/ntp.conf

