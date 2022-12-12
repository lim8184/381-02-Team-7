### teams Bot ###
from webexteamsbot import TeamsBot
from webexteamsbot.models import Response
### Utilities Libraries
import routers
import useful_skills as useful
import netconf_add as netadd
import netconf_delete as netdel
### Utilites for Ansible Monitor
from subprocess import call

device_address = routers.router['host']
device_username = routers.router['username']
device_password = routers.router['password']

bot_email = '381-02-Team-7@webex.bot'
teams_token = 'MzEyZjY1MTgtMzg3Yi00MGM3LThmN2YtMzMzNmVjNzc4ODM1OGEyNDAwOWMtNmYx_P0A1_da087be3-a5c4-42e0-91c2-0fc6d3da3fdb'
bot_url = "https://dd81-144-13-254-62.ngrok.io"
bot_app_name = 'CNIT-381 Network Auto Chat Bot'

bot = TeamsBot(
    bot_app_name,
    teams_bot_token=teams_token,
    teams_bot_url=bot_url,
    teams_bot_email=bot_email,
    debug=True,
    webhook_resource_event=[
        {"resource": "messages", "event": "created"},
        {"resource": "attachmentActions", "event": "created"},],
)

def greeting(incoming_msg):

    sender = bot.teams.people.get(incoming_msg.personId)


    response = Response()
    response.markdown = "Hello {}, I'm a bot made by team 7!  ".format(
        sender.firstName
    )
    response.markdown += "\n\nSee what I can do by asking for **/help**."
    return response


def monitor(incoming_msg):
    call(["ansible-playbook","Monitor.yml"])
    response = Response()
    response.markdown = "I finished monitoring the vpn connection!"
    return response

def backup(incoming_msg):
    call(["ansible-playbook", "Backup.yml"])
    response = Response()
    response.markdown = "I backed up all the devices for you!"
    return response

def loopback_add(incoming_msg):
    response = Response()
    netadd.netconf_add()
    response.markdown = "Loopback 1 has been created"
    return response

def loopback_delete(incoming_msg):
    response = Response()
    netdel.netconf_delete()
    response.markdown = "Loopback 1 has been deleted"
    return response

# Create a function to pull the current ipv4 configuration from the router
def getInterfaces(incoming_msg):
    ## Return information about interfaces
    response = Response()
    routerInfo = {'hostname':device_address,'port':'22','username':device_username,'password':device_password,'look_for_keys':False,'allow_agent':False}
    ints = useful.getInterfaces(routerInfo) ## ??
    response.markdown = ints
    return response


bot.set_greeting(greeting)
bot.add_command("monitor", "Check VPN status", monitor)
bot.add_command("backup", "Backup Cisco devices", backup)
bot.add_command("Add loopback", "Adds new loopback", loopback_add)
bot.add_command("Delete loopback", "Deletes loopback", loopback_delete)
bot.add_command('show interfaces', 'Show the interfaces and their ipv4 addresses', getInterfaces)

bot.remove_command("/echo")


if __name__ == "__main__":

    bot.run(host="0.0.0.0", port=5000)

