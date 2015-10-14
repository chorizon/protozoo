#!/usr/bin/python3

from socket import getfqdn
import subprocess

if subprocess.call("sudo DEBIAN_FRONTEND=noninteractive apt-get -y install postfix procmail",  shell=True) > 0:
    print('Error')
    exit(1)
else:
    print('Postfix installed successfully')

f=open("tmp/main.cf", 'r')

main_cf=f.read()

main_cf=main_cf.replace('myhostname = localhost.localdomain', 'myhostname = '+getfqdn())

main_cf=main_cf.replace('mydestination = localhost.localdomain', 'mydestination = '+getfqdn())

f.close()

f=open("tmp/main.cf", 'w')

f.write(main_cf)

f.close()

#Install normal files

if subprocess.call("sudo touch /etc/postfix/virtual_mailbox /etc/postfix/white_list /etc/postfix/virtual_domains",  shell=True) > 0:
    exit(1)
else:
    print('Postfix mailbox db and white_list db created')
    if subprocess.call("sudo postmap hash:/etc/postfix/virtual_mailbox && sudo postmap hash:/etc/postfix/virtual_domains && sudo postmap hash:/etc/postfix/white_list",  shell=True) > 0:
        print('Error, cannot create db files for postfix')
        exit(1)



if subprocess.call("sudo cp tmp/master.cf tmp/main.cf /etc/postfix",  shell=True) > 0:
    print('Error')
    exit(1)
else:
    print('Postfix files installed successfully')
    exit(0)



