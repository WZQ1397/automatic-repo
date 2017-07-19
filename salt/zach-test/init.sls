{%- if grains['os'] == 'Ubuntu' %}
{{ pillar.zach.admin_user.username}}:
  user.present:
    - password: {{ pillar.zach.admin_user.password}}
    - uid: 600
    - gid: 600
    - system: True
    - groups:
      - root
{%- else %}
zach:
  group.present:
    - gid: 600
xyc:
  user.present:
    - password: {{ pillar.zach.admin_user.password}}
    - uid: 600
    - gid: 600
    - system: False
    - groups:
      - zach
{%- endif %}
