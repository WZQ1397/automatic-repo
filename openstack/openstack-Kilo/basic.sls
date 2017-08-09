python-mysqldb:
    pkg:
        - installed

{% if grains['os'] == 'Ubuntu' and grains['oscodename'] !='trusty' %}

openstack_sources_list:
    cmd.run:
        - name: add-apt-repository -y cloud-archive:icehouse
        - unless: ls -lah /etc/apt/sources.list.d/ | grep icehouse
        
{% endif %}
