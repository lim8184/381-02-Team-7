from ncclient import manager 
import xml.dom.minidom 

def netconf_delete():

    m = manager.connect( 
        host="192.168.56.104", 
        port=830, 
        username="cisco", 
        password="cisco123!", 
        hostkey_verify=False 
        ) 
 
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
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                    <interface operation="delete">
                            <name>Loopback1</name>
                    </interface>
            </interfaces>
    </config>
    """ 
    netconf_reply = m.edit_config(target="running", config=netconf_loopback) 
    print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml()) 
