### teams Bot ###
from webexteamsbot import TeamsBot
from webexteamsbot.models import Response
### Utilities Libraries
import routers
import useless_skills as useless
import useful_skils as useful

# Router Info
device_address = routers.router['host']
device_username = routers.router['username']
device_password = routers.router['password']

# RESTCONF Setup
port = '443'
url_base = "https://{h}/restconf".format(h=device_address)
headers = {'Content-Type': 'application/yang-data+json',
            'Accept': 'application/yang-data+json'}

# Bot Details
bot_email = '381-02-Team-7@webex.bot'
teams_token = 'MzEyZjY1MTgtMzg3Yi00MGM3LThmN2YtMzMzNmVjNzc4ODM1OGEyNDAwOWMtNmYx_P0A1_da087be3-a5c4-42e0-91c2-0fc6d3da3fdb'
bot_url = 
bot_app_name = 'CNIT-381 Final Project Chat Bot'

# Create a Bot Object
bot = TeamsBot(
    bot_app_name,
    teams_bot_token=teams_token,
    teams_bot_url=bot_url,
    teams_bot_email=bot_email,
    debug=True,
    webhook_resource_event=[
        {'resource':'messages','event':'created'}
        {'resource':'attachmentActions','event':'created'},]
    )

# Create a function to respond to messages that lack any specific command
def greeting(incoming_msg):
    # Look up details about the sender
    sender = bot.teams.people.get(incoming_msg.personId)

    # Create a Response object and craft a reply in Markdown
    response = Response()
    response.markdown = "Hello {}, I'm a friendly CSR1100v assistant .  ".format(sender.firstName)
    response.markdown += "\n\nSee what I can do by asking for **/help**."
    return response

# Create a function to pull the current ipv4 configuration from the router

if __name__ == '__main__':
    # Run Bot
    bot.run(host='0.0.0.0',port=5000)