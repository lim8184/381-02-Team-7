import os
import sys
import paramiko
import time
import datetime
import routers

def getInterfaces(router):
    ## Return the output of "show ip int br"
    sshClient = paramiko.SSHClient()
    sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sshClient.connect(**router)
    shell = sshClient.invoke_shell()
    shell.send('show ip interface brief\n')
    time.sleep(1)
    output = shell.recv(10000)
    output = output.decode('utf-8')
    sshClient.close()
    return '\n'.join(output.splitlines()[16:-1])


