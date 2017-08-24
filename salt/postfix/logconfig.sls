postfix: 
    pkg:
        - installed
    service.running:
        - enable: True
        - require:
            - pkg: postfix

{% if grains.os == 'Ubuntu'%}
postfix-pcre:
    pkg:
        - installed
        - require_in:
            - service: postfix
{% endif %}

pflogsumm:
    pkg.installed:
        - pkg: postfix

/var/log/report:
    file.directory:
        - user   : root
        - group  : root
        - mode   : 0700

/etc/postfix/mail_log_report:
    file.managed:
        - source : salt://postfix/mail_log_report
        - user   : root
        - group  : root
        - mode   : 0700
        - require:
            - pkg  : pflogsumm
            - file : /var/log/report

report_postfix_log:
    cron.present:
        - name:  "/etc/postfix/mail_log_report 2>&1 | /usr/bin/logger -p daemon.info -t mail_log_report"
        - identifier: report_postfix_log
        - minute: 0,30
        - require:
            - file: /etc/postfix/mail_log_report
