#!/usr/bin/python3 -u

#A simple script for install pastafari

from base64 import b64encode
import argparse
from subprocess import call,Popen, PIPE
import shutil
import os

#Add user pastafari

parser = argparse.ArgumentParser(description='A script for install pastafari')

parser.add_argument('--user', help='The user for pastafari', required=True)

parser.add_argument('--port', help='The port where pastafari listen the requests', required=True)

parser.add_argument('--secret_key', help='A secret key used for identify the server. Please use the most random key possible', required=True)

parser.add_argument('--ip', help='The server from you access to this machine', required=True)

args = parser.parse_args()

#Add new user

user=args.user

if call("sudo useradd -m -s /bin/false "+user,  shell=True) > 0:
    print('Error, cannot create user')
    exit(1)
else:
    print('Created user '+user+' sucessfully')

#Change permissions to directory



#Install phango framework

if call("sudo git clone https://github.com/phangoapp/phango /home/"+user+"/site/pastafari",  shell=True) > 0:
    print('Error, cannot install Phango Framework')
    exit(1)
else:
    print('Created Phango Framework')

#Install pastafari

if call("sudo git clone https://github.com/chorizon/pastafari.git /home/"+user+"/site/pastafari/modules/pastafari/",  shell=True) > 0:
    print('Error, cannot install Pastafari module')
    exit(1)
else:
    print('Added pastafari module')

#Configure Phango

secret_key=args.secret_key

# Generate random secret_key for pastafari. For this things i hate the python documentation

random_bytes = os.urandom(64)
secret_key_pastafari = b64encode(random_bytes).decode('utf-8')

f=open('tmp/config.php')

config_php=f.read()

f.close()

config_php=config_php.replace('secret_key', secret_key_pastafari)

p = Popen(['php', '-r "echo password_hash(\''+secret_key_pastafari+'+'+secret_key+'\', PASSWORD_DEFAULT);"'], stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)

out, err = p.communicate()

secret_key_hashed=out.decode('utf-8').strip()

config_php=config_php.replace('secret_key_with_pass', secret_key_hashed)

f=open("tmp/new_config.php", "w")

f.write(config_php)

f.close()

if call("sudo mv tmp/new_config.php /home/"+user+"/site/pastafari/config.php", shell=True) > 0:
    print('Error, cannot install Pastafari module')
    exit(1)
else:
    print('Added pastafari module')

"""
if call('php -r "echo password_hash(\'pslmciadmasdxXslsdl2990ds09as@#~df~@|@+opaopsdasdmxcpasdapsdxlcasdpamciaw\', PASSWORD_DEFAULT);"', shell=True):
    print('Error, cannot install Pastafari module')
    exit(1)
else:
    print('Added pastafari module')
"""
#shutil.move(

#Create certs

#Add php-fpm configuration and reload

#Add sudo configuration and reload

#Add nginx configuration and reload

print('Installing pastafari with git...')