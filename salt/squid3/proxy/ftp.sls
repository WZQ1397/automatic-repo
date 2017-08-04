ftp-proxy:
    pkg:
        - installed

/etc/default/ftp-proxy:
    file.replace:
        - pattern: RUN_DAEMON=no
        - repl: RUN_DAEMON=yes
        - require:
            - pkg: ftp-proxy

/etc/init.d/multi-ftp-proxy:
    file.managed:
        - source: salt://squid3/proxy/_files/multi-ftp-proxy
        - mode: '0755'
        - require:
            - pkg: ftp-proxy

multi-ftp-proxy:
    service.running:
        - enable: true
        - require:
             - file: /etc/init.d/multi-ftp-proxy


{% set ftps = salt['pillar.get']('proxy:ftps') %}

{%- if ftps %}
    {% for item in ftps %}

/etc/proxy-suite/ftp_proxy_{{item.name}}.conf:
    file.managed:
        - source: salt://squid3/proxy/_files/ftp-proxy.conf
        - mode: '0644'
        - template: jinja
        - defaults:
            name: {{item.name}}
            host: {{item.host}}
            port: {{item.port}}
            backend: {{item.backend}}
            backport: {{item.backport}}
        - require:
            - pkg: ftp-proxy
        - watch_in:
            - service: multi-ftp-proxy
    {% endfor %}
{% endif -%}
