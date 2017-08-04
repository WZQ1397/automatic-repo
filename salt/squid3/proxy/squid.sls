include:
    - squid3.squid3

extend:
    {{pillar.squid3.config.target}}:
        file.managed:
            - source  : salt://squid3/proxy/_files/squid.conf

{% set ips = salt['pillar.get']('proxy:ips') %}
{% set hosts = salt['pillar.get']('proxy:hosts') %}

{%- if ips %}
    {% for item in ips %}

/etc/squid3/objects/{{item.name}}.conf:
    file.managed:
        - source: salt://squid3/proxy/_files/squid3.forward.conf
        - mode: '0644'
        - template: jinja
        - defaults:
            name: {{item.name}}
            host: {{item.host}}
            port: {{item.port}}
            backend: {{item.backend}}
            backport: {{item.backport}}

    {% endfor %}
{% endif -%}

{%- if hosts %}
    {% for item in hosts %}
/etc/squid3/objects/{{item.name}}.conf:
    file.managed:
        - source: salt://squid3/proxy/_files/squid3.urlproxy.conf
        - mode: '0644'
        - template: jinja
        - defaults:
            name: {{item.name}}
            host: {{item.host}}
            port: {{item.port}}
            backend: {{item.backend}}
            backport: {{item.backport}}
    {% endfor %}
{% endif -%}