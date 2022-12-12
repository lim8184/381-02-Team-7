import routers
from ncclient import manager, xml_

# Router Info 
device_address = routers.router['host']
device_username = routers.router['username']
device_password = routers.router['password']
# RESTCONF Setup
device_restconf_port = '443'
restcofnf_url_base = "https://{h}/restconf".format(h=device_address)
resconf_headers = {'Content-Type': 'application/yang-data+json',
           'Accept': 'application/yang-data+json'}
# NETCONF Setup
device_netconf_port = routers.router['port']
netconf_device = manager.connect(
    host=device_address,
    port=device_netconf_port,
    username=device_username,
    password=device_password,
    hostkey_verify=False)
