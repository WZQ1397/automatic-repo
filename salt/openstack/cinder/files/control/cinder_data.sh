export OS_PROJECT_DOMAIN_NAME=Default
export OS_USER_DOMAIN_NAME=Default
export OS_PROJECT_NAME=admin
export OS_USERNAME=admin
export OS_PASSWORD="{{ADMIN_PASSWD}}"
export OS_AUTH_URL=http://{{CONTROL_IP}}:35357/v3
export OS_IDENTITY_API_VERSION=3
export OS_IMAGE_API_VERSION=2

openstack user create --domain default --password {{ CINDER_PASS }} {{ CINDER_USER }}
openstack role add --project service --user {{ CINDER_USER }} admin
openstack service create --name {{ CINDER_USER }} --description "OpenStack Block Storage" volume
openstack service create --name {{ CINDER_USER }}v2 --description "OpenStack Block Storage" volumev2

openstack endpoint create --region RegionOne volume public http://{{CONTROL_IP}}:8776/v1/%\(tenant_id\)s
openstack endpoint create --region RegionOne volume internal http://{{CONTROL_IP}}:8776/v1/%\(tenant_id\)s
openstack endpoint create --region RegionOne volume admin http://{{CONTROL_IP}}:8776/v1/%\(tenant_id\)s
openstack endpoint create --region RegionOne volumev2 public http://{{CONTROL_IP}}:8776/v2/%\(tenant_id\)s
openstack endpoint create --region RegionOne volumev2 internal http://{{CONTROL_IP}}:8776/v2/%\(tenant_id\)s
openstack endpoint create --region RegionOne volumev2 admin http://{{CONTROL_IP}}:8776/v2/%\(tenant_id\)s

su -s /bin/sh -c "cinder-manage db sync" cinder
service nova-api restart
service cinder-scheduler restart
service apache2 restart