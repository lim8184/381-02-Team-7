# CNIT 381 Chatbot Final Project

## NETCONF

Our NETCONF skill provides the capability to add and delete a loopback interface but can be modified to add or delete any number of interfaces.

Using NETCONF we were able to directly connect to one of our routers in order to modify the router configuration.
This is done through creating Python code that is defined as a function to be called by our chat bot. This is done in order to ease the process of creating or deleting interfaces on any number of routers.

The code will look like the following for the add loopback code

image

The code will look like the following for the delete loopback code

image

The print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml()) command is used to allow the output to be depicted in a more readable state rather than the original xml format.
The prior command defines the desired loopback interface configuration with ip address and subnet mask.

The delete file has the same output toprettyxml command used for the same purpose as above.
The delete code simply tells the router that the interface known as Loopback1, or whichever interface you wish to call, needs to be deleted.

The NETCONF code is simple but easy to use and understand.  It can be modified at will to change the functionality of the code without impacting the chat bot.

## Monitoring

For monitoring we used Ansible to automate the process of changing the necessary crypto settings on our cisco devices to function with a dhcp enabled neighbor that will potentially have a constantly changing interface configuration.

Using Ansible we can make conditionals and check for facts from our cisco devices to know when our crypto session for the vpn is down. 
We do this by first clearing all crypto sessions. We do this because if there was a previous session then the processing of checking the session will be interferred with by the previous session which has a chance of not updating as fast as if were to just clear it.
Then after this we send a ping to 1.1.1.1 from 2.2.2.2, this is because we want to make sure the loopbacks can ping each other. We do this from CSR2 because a majority of the changes we will be making will be on this device, and we are assuming we have minimal ability to interact with CSR1 other then getting the interface.

The code will look like the following

![Screenshot 2022-12-05 231335](https://user-images.githubusercontent.com/118213821/205822337-f9165fc0-a4ad-43f5-b96b-b0a30d835522.png)

The delegate_to line is to ensure that we make sure only the devices that we running will run the code. In this instance CSR2 is the one delegated to run the task.

Following this we have a check which is the one where all the future conditionals will be based on. This requires two tasks as we will need to extract the specific data we need from this as well.

The first task is to just send a show crypto session command get the status output from the cisco device and register it to a variable. Then the second task will take that variable and create a new variable where it only takes the necessary part (Which in our case will be UP-ACTIVE when the connection is up) and stores it in that variable.

![Screenshot 2022-12-05 232234](https://user-images.githubusercontent.com/118213821/205823455-c3fa9be2-d453-4691-8833-4e7da169a670.png)

We use the .stdout tag on the end of the command to get the raw output of the variable as ansible will put a lot of formatting on top of that. The following parts with .split[0] just tells what parts need to be cut off from the value so we can get what we need, which is UP-ACTIVE

### The following tasks will start to use an Ansible conditional When. This is a pretty simple conditional, all it does is compare two items and if the result is true then the task will run. In this case we compared the variable from the previous step to "UP-ACTIVE", and whenever the variable didn't match this than it would run the task.

The next thing that the task will do is to solve a problem with security. This part doesn't need to be done if you don't care about keeping previous entries of the crypto session. But to prevent anyone from spoofing a previous ip address we'll be removing the old entries.
  
This section is quite simple. We will just utilize cisco's pipe (|) filtering to get the pre-exsiting commands from the running configuration.
#### Show run | s cisco isakmp key cisco address
This will save the result to another variable, with the content being the command that we need to remove. We will need to do this twice, for both the crypto isakmp key, and set peer commands.

The set peer command requires us to use a special tag after our normal ios_config. This being the parent command, as "set peer" is in a different level that requires us to state that we need to enter "crypto map Crypt 10 ipsec-isakmp" first. Otherwise we'll encounter errors as ios_config does not allow direct manipulation of that level without telling it that we are going into it first.

![Screenshot 2022-12-05 233917](https://user-images.githubusercontent.com/118213821/205825823-990c07bc-3671-40f1-93bd-7d4960cc18a6.png)

The final steps will require us to get the ip address from CSR1. In our circumstance, we've already saved that into a variable called ip_addr. This was done at the beginning of the script, so that it would always have it even if it wasn't necessary. With the ip address of CSR1's Gig 2 interface we are able to use it in the following steps pretty much as we've been doing so far. 

With crypto isakmp key we need the ip address then we will put {{}} brackets around ip_addr, so that the command will know that we are using a variable.

![Screenshot 2022-12-05 234352](https://user-images.githubusercontent.com/118213821/205826570-ac7b8735-f1a8-4df8-9724-72e3877d18aa.png)

Set peer is equally as simple, but it'll use a few more things that we've been using so far. Mainly the parent feature as set peer on a different level that ios_config cannot use without it.

![Screenshot 2022-12-05 234409](https://user-images.githubusercontent.com/118213821/205826792-71c88049-4490-4c4b-b5ef-5fe4f9d98c7d.png)

After all this we will clear the crypto session one more time to make sure the next person who tries to use the vpn connection will not get stuck because of the previous session.

#### Running Ansible playbook through python
To run the ansible playbook required to monitor the network we will be using the subprocess module in python. This will require us to import call from the subprocess module. After this is done you can execute cli commands through python. Like the below example.
##### call(["ansible-playbook","monitor.yml"])
