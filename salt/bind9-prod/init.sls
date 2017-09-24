include:
  - bind

{% 
    set props = salt['grains.filter_by']({
        
        'ns1.eyou.tonyc.cn': { 
            'primary': True, 
            'zonedir': '/var/cache/bind' },

        'ns2.eyou.tonyc.cn': { 
            'primary': False, 
            'zonedir': '/var/cache/bind' }

    }, 'id')
%}

{% if grains['os_family'] in 'Debian' %}

{%if props.primary %}

/etc/bind:
  file.recurse:
    - source: salt://states/dns/bind.primary
    - template: jinja
    - context: {{props}}

{{props.zonedir}}:
  file.recurse:
    - source: salt://states/dns/zones/

{% else %}

/etc/bind:
  file.recurse:
    - source: salt://states/dns/bind.secondary
    - template: jinja
    - context: {{props}}

{{props.zonedir}}: file.directory

{% endif %}

{% endif %}

rndc reload:
    cmd.wait:
        - require:
            - service: bind9-services
        - watch:
            - file: {{props.zonedir}}

rndc reconfig:
    cmd.wait:
        - require:
            - service: bind9-services
        - watch:
            - file: /etc/bind
