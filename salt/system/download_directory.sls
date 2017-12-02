{% if grains['kernel'] == 'Windows' %}

download_directory:
    file.directory:
        - names:
            - D:\software

{% elif grains['kernel'] == 'Linux' %}

download_directory:
    file.directory:
        - names:
            - /root/software
            
{% endif %}