include:
    - services.postfix
    
/etc/postfix/main.cf:
    file.managed:
        - source: salt://states/eyou/postfix/main.cf
        - watch_in:
            - service: postfix
        - template: jinja

/etc/postfix/master.cf:
    file.managed:
        - source: salt://states/eyou/postfix/master.cf
        - watch_in:
            - service: postfix

{% macro table(tabfile, type='hash') -%}
/etc/postfix/tables/{{tabfile}}:
    file.managed:
        - source : salt://states/eyou/postfix/tables/{{tabfile}}
        - user   : root
        - group  : root
        - require :
            - pkg : postfix
        - watch_in:
            - service: postfix

{% if type not in ['pcre'] %}

postmap {{type}}:{{tabfile}}:
    cmd.wait:
        - name: postmap {{type}}:/etc/postfix/tables/{{tabfile}}
        - output_loglevel: debug
        - watch:
            - file: /etc/postfix/tables/{{ tabfile }}
        - watch_in:
            - service: postfix

{% endif %}

{%- endmacro %}

{{ table('ip_relay')   }}
{{ table('transports') }}
{{ table('sender_transports') }}
{{ table('header_checks','pcre') }}
{{ table('recipient_bcc_maps') }}
{{ table('sender_bcc_maps') }}

# /etc/postfix/tables:
#     file.recurse:
#         - source: salt://states/eyou/postfix/tables
#         - watch_in:
#             - service: postfix


# /tmp/test: 
#     postfix.table:
#         - type: hash
#         - context: 'aaaaaa'