export OS_PROJECT_DOMAIN_NAME=Default
export OS_USER_DOMAIN_NAME=Default
export OS_PROJECT_NAME=admin
export OS_USERNAME=admin
export OS_PASSWORD="{{ADMIN_PASSWD}}"
export OS_AUTH_URL=http://{{CONTROL_IP}}:35357/v3
export OS_IDENTITY_API_VERSION=3
export OS_IMAGE_API_VERSION=2

openstack user create --domain default --password {{NOVA_PASS}} {{NOVA_USER}}
openstack role add --project service --user {{NOVA_USER}} admin
openstack service create --name {{NOVA_USER}} --description "OpenStack Compute" compute
openstack endpoint create --region RegionOne compute public http://{{CONTROL_IP}}:8774/v2.1/%\(tenant_id\)s
openstack endpoint create --region RegionOne compute internal http://{{CONTROL_IP}}:8774/v2.1/%\(tenant_id\)s 
openstack endpoint create --region RegionOne compute admin http://{{CONTROL_IP}}:8774/v2.1/%\(tenant_id\)s

openstack service create --name placement --description "Placement API" placement
openstack endpoint create --region RegionOne placement public http://{{CONTROL_IP}}:8778
openstack endpoint create --region RegionOne placement internal http://{{CONTROL_IP}}:8778
openstack endpoint create --region RegionOne placement admin http://{{CONTROL_IP}}:8778