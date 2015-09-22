#!/usr/bin/python3 -u

#A simple script for install pastafari

import argparse

#Add user pastafari

parser = argparse.ArgumentParser(description='A script for install pastafari')

parser.add_argument('--user', help='The user for pastafari', required=True)

parser.add_argument('--port', help='The port where pastafari listen the requests', required=True)

parser.add_argument('--secret_key', help='A secret key used for identify the server. Please use the most random key possible', required=True)

parser.add_argument('--ip', help='The server from you access to this machine', required=True)

args = parser.parse_args()

#Add new user

user=args.user

if subprocess.call("sudo useradd -m -s /bin/false "+user,  shell=True) > 0:
    print('Error, cannot create user')
    exit(1)
else:
    print('Created user '+user+' sucessfully')

#Install phango framework

if subprocess.call("sudo git clone https://github.com/phangoapp/phango /home/"+user+"/site/pastafari",  shell=True) > 0:
    print('Error, cannot install Phango Framework')
    exit(1)
else:
    print('Created Phango Framework')

#Install pastafari

#Configure Phango

#Create certs

#Add php-fpm configuration and reload

#Add sudo configuration and reload

#Add nginx configuration and reload

print('Installing pastafari with git...')