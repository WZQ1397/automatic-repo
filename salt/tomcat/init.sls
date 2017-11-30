{% set tomcat_pkg = salt['grains.kernel']({
    'Windows': {'name': 'apache-tomcat-6.0.39-windows-x64','hash': '3f5a018666b4b1b36f6a62059666bed4c27429b9'}
    'Linux': {'name': 'apache-tomcat-6.0.39','hash': '09db6cda165c6180f19c65cd95732b546bada456'}
}, default='Linux') %}

include:
    - .java


D:\software\{{ tomcat_pkg.name }}.zip:
    file.managed:
        - source: http://mirrors.hwdzsw.net/public/software/{{ tomcat_pkg.name }}.zip
        - source_hash: sha1={{ tomcat_pkg.hash }}

{% if grains['kernel'] == 'Windows' %}
D:\webapp:
    file.directory:
        - names: 
            - D:\webapp

tomcat_unzip:
    cmd.run:
        - name: >
            "C:\program files\7-zip\7z.exe" 
            x D:\software\{{ tomcat_pkg.name }}.zip
            -oD:\webapp\ -y && move D:\webapp\apache-tomcat-* D:\webapp\tomcat
        - unless: dir D:\webapp\tomcat\bin >nul
        - require:
            - file: D:\webapp
            - file: D:\software\{{ tomcat_pkg.name }}.zip

{% elif grains['kernel'] == 'Linux' %}


apache-tomcat-6-unpack:
    cmd.wait:
        - name: rm -f /usr/java/{{ tomcat_pkg.name }} && tar -xzvf /root/software/{{ tomcat_pkg.name }}.tar.gz -C /usr/java
        - watch:
            - file: /root/software/{{ tomcat_pkg.name }}.tar.gz
        - requires:
            - file: /root/software/{{ tomcat_pkg.name }}.tar.gz
{% endif %}
