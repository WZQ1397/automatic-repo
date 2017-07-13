{% 
    set props  = salt['grains.filter_by']({
        'Debian': { 'pkgs': ['bind9'], 'service': 'bind9'},
        'RedHat': { 'pkgs': ['bind'],  'service': 'named'}
    })
%}

bind9-packages:
   pkg.installed:
     - pkgs: {{props.pkgs}}

bind9-services:
   service.running:
     - name: {{props.service}}
     - enable: True
     - require:
        - pkg: bind9-packages