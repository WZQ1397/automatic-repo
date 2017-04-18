export OS_PROJECT_DOMAIN_NAME=Default
export OS_USER_DOMAIN_NAME=Default
export OS_PROJECT_NAME=admin
export OS_USERNAME=admin
export OS_PASSWORD="{{ADMIN_PASSWD}}"
export OS_AUTH_URL=http://{{CONTROL_IP}}:35357/v3
export OS_IDENTITY_API_VERSION=3
export OS_IMAGE_API_VERSION=2

openstack endpoint create --region RegionOne identity public http://{{CONTROL_IP}}:5000/v3
openstack endpoint create --region RegionOne identity internal http://{{CONTROL_IP}}:5000/v3
openstack endpoint create --region RegionOne identity admin http://{{CONTROL_IP}}:35357/v3

openstack user create --domain default --password {{ GLANCE_PASS }} {{ GLANCE_USER }}
openstack role add --project service --user {{ GLANCE_USER }} admin
openstack service create --name {{ GLANCE_USER }}   --description "OpenStack Image" image

openstack endpoint create --region RegionOne image public http://{{CONTROL_IP}}:9292
openstack endpoint create --region RegionOne image internal http://{{CONTROL_IP}}:9292
openstack endpoint create --region RegionOne image admin http://{{CONTROL_IP}}:9292

su -s /bin/sh -c "glance-manage db_sync" glance

service glance-registry restart
sleep 3
service glance-api restart