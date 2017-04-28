unlimited-security-limits:
  file.blockreplace:
    - name: /etc/security/limits.conf
    - marker_start: "# START managed zone system -DO-NOT-EDIT-"
    - marker_end: "# END managed zone system --"
    - content: |
        *    hard    nofile  127680
        *    soft    nofile  127680
        *    hard  nproc  32000
        *    soft  nproc  32000
        root    hard    nofile  127680
        root    soft    nofile  127680
        root    hard  nproc  32000
        root    soft  nproc  32000        
    - append_if_not_found: True
    - backup: '.bak'
    - show_changes: True

unlimited-security-limits-in-session:
  file.blockreplace:
    - names: 
        - /etc/pam.d/common-session
        - /etc/pam.d/common-session-noninteractive
    - marker_start: "# START managed zone system -DO-NOT-EDIT-"
    - marker_end: "# END managed zone system --"
    - content: |
        session required pam_limits.so        
    - append_if_not_found: True
    - backup: '.bak'
    - show_changes: True 

