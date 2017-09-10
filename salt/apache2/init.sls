{% set apache = salt['grains.filter_by'](
                    {'RedHat': 'httpd','Debian': 'apache2'}), default='Debian') %} 
#, grain='os'
{{ apache }}:
  pkg:
    - installed
  service.running:
    - enable: True
    - reload: True
    - watch:
      - pkg: {{ apache }}

