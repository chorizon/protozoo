#!/usr/bin/python3

import subprocess

if subprocess.call("sudo DEBIAN_FRONTEND=noninteractive apt-get -y install dovecot-core dovecot-imapd",  shell=True) > 0:
    print('Error')
    exit(1)
else:
    print('Dovecot installed successfully')
    
#Install config files

if subprocess.call("sudo cp tmp/dovecot.conf /etc/dovecot",  shell=True) > 0:
    print('Error copying dovecot.conf')
    exit(1)
else:
    print('Dovecot principal conf files installed successfully')



if subprocess.call("sudo cp tmp/10-master.conf tmp/10-auth.conf tmp/10-mail.conf /etc/dovecot/conf.d",  shell=True) > 0:
    print('Error copying conf.d files')
    exit(1)
else:
    print('Dovecot conf files installed successfully')
    
if subprocess.call("sudo systemctl restart dovecot",  shell=True) > 0:
    print('Error')
    exit(1)
else:
    print('Dovecot reload successfully')

if subprocess.call("sudo systemctl restart postfix",  shell=True) > 0:
    print('Error')
    exit(1)
else:
    print('Postfix reload successfully for use dovecot sasl')

exit(0)


