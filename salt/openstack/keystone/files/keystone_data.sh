export OS_PROJECT_DOMAIN_NAME=Default
export OS_USER_DOMAIN_NAME=Default
export OS_PROJECT_NAME=admin
export OS_USERNAME=admin
export OS_PASSWORD="{{ADMIN_PASSWD}}"
export OS_AUTH_URL=http://{{CONTROL_IP}}:35357/v3
export OS_IDENTITY_API_VERSION=3
export OS_IMAGE_API_VERSION=2

keystone-manage fernet_setup --keystone-user keystone --keystone-group keystone
keystone-manage credential_setup --keystone-user keystone --keystone-group keystone
keystone-manage bootstrap --bootstrap-password ADMIN_PASS \
  --bootstrap-admin-url http://{{ CONTROL_IP }}:35357/v3/ \
  --bootstrap-internal-url http://{{ CONTROL_IP }}:5000/v3/ \
  --bootstrap-public-url http://{{ CONTROL_IP }}:5000/v3/ \
  --bootstrap-region-id RegionOne

openstack project create --domain default --description "Service Project" service
openstack user create --domain default --password-prompt admin
openstack role create admin
openstack role add --project admin --user admin admin