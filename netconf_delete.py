from ncclient import manager 
import xml.dom.minidom 
 
try:
        with open(args.inventory, "r") as f:
            device_data = json.load(f)
    except (ValueError, IOError, OSError) as err:
        merge_device("Could not read the 'devices' file:", err)
 
netconf_reply = m.get_config(source="running") 
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml()) 
 
netconf_filter = """ 
<filter> 
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native" /> 
</filter>
""" 
netconf_reply = m.get_config(source="running", filter=netconf_filter) 
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml()) 

 
netconf_loopback = """ 
<config> 
 <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native"> 
  <interface>
   <interface operation="delete">
            <name>Loopback1</name> 
  </interface> 
 </native> 
</config> 
""" 
netconf_reply = m.edit_config(target="running", config=netconf_loopback) 
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml()) 