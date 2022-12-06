CNIT 381 Chatbot Final Project
Monitoring:
For monitoring we used Ansible to automate the process of changing the necessary crypto settings on our cisco devices to function with a dhcp enabled neighbor that will potentially have a constantly changing interface configuration.

Using Ansible we can make conditionals and check for facts from our cisco devices to know when our crypto session for the vpn is down. 
We do this by first clearing all crypto sessions. We do this because if there was a previous session then the processing of checking the session will be interferred with by the previous session which has a chance of not updating as fast as if were to just clear it.
Then after this we send a ping to 1.1.1.1 from 2.2.2.2, this is because we want to make sure the loopbacks can ping each other. We do this from CSR2 because a majority of the changes we will be making will be on this device, and we are assuming we have minimal ability to interact with CSR1 other then getting the interface.

The code will look like the following
![Screenshot 2022-12-05 231335](https://user-images.githubusercontent.com/118213821/205822337-f9165fc0-a4ad-43f5-b96b-b0a30d835522.png)
