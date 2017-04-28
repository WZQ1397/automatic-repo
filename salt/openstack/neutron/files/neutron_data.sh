export OS_PROJECT_DOMAIN_NAME=Default
export OS_USER_DOMAIN_NAME=Default
export OS_PROJECT_NAME=admin
export OS_USERNAME=admin
export OS_PASSWORD="{{ADMIN_PASSWD}}"
export OS_AUTH_URL=http://{{CONTROL_IP}}:35357/v3
export OS_IDENTITY_API_VERSION=3
export OS_IMAGE_API_VERSION=2

openstack user create --domain default --password {{ NEUTRON_PASS }} {{ NEUTRON_USER }}
openstack role add --project service --user {{ NEUTRON_USER }} admin
openstack service create --name {{ NEUTRON_USER }} --description "OpenStack Networking" network

openstack endpoint create --region RegionOne network public http://{{CONTROL_IP}}:9696
openstack endpoint create --region RegionOne network internal http://{{CONTROL_IP}}:9696
openstack endpoint create --region RegionOne network admin http://{{CONTROL_IP}}:9696

