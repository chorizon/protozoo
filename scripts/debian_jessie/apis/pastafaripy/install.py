#!/usr/bin/python3 -u

#A simple script for install pastafari

from base64 import b64encode
from subprocess import call, Popen, PIPE
from pathlib import Path
from socket import gethostname
import argparse
import shutil
import os
import hashlib

#Add user pastafari

parser = argparse.ArgumentParser(description='A script for install pastafari')

parser.add_argument('--user', help='The user for pastafari', required=True)

parser.add_argument('--port', help='The port where pastafari listen the requests', required=True)

parser.add_argument('--secret_key', help='A secret key used for identify the server. Please use the most random key possible', required=True)

parser.add_argument('--ip', help='The server IP from you access to this machine', required=True)

parser.add_argument('--cert', help='Cert string with this format: /C=US/ST=California/L=Palo Alto/O=IT/CN=www.example.com', default='/C=US/ST=California/L=Palo Alto/O=IT/CN='+gethostname())

args = parser.parse_args()

#Add new user

user=args.user

if call("sudo useradd -m -s /bin/false "+user,  shell=True) > 0:
    print('Error, cannot create user')
    exit(1)
else:
    print('Created user '+user+' sucessfully')

#Change permissions to directory



#Install Paramecio framework

if call("sudo git clone https://github.com/webtsys/paramecio.git /home/"+user+"/site/paramecio",  shell=True) > 0:
    print('Error, cannot install Paramecio Framework')
    exit(1)
else:
    print('Installed Paramecio Framework')
    
    
#Install Pastafari framework

if call("sudo git clone https://github.com/chorizon/pastafaripy.git /home/"+user+"/site/paramecio/modules/pastafari",  shell=True) > 0:
    print('Error, cannot install Pastafari')
    exit(1)
else:
    print('Installed Pastafari')

#Configure Paramecio

#Configure keys

secret_key=args.secret_key

# Generate random secret_key for pastafari. For this things i hate the python documentation

random_bytes = os.urandom(24)
secret_key_pastafari = b64encode(random_bytes).decode('utf-8').strip()

f=open('tmp/config.py')

config_py=f.read()

f.close()

config_py=config_py.replace('secret_key', secret_key_pastafari)

m=hashlib.sha512()

code=secret_key_pastafari+'+'+secret_key

code=code.encode('utf-8')

m.update(code)

secret_key_hashed=m.hexdigest()

config_py=config_py.replace('key_hashed', secret_key_hashed)

# Config available ip

config_py=config_py.replace('allowed_ips=[]', 'allowed_ips=["'+args.ip+'"]');

f=open("tmp/new_config.py", "w")

f.write(config_py)

f.close()

if call("sudo cp tmp/new_config.py /home/"+user+"/site/paramecio/settings/config.py", shell=True) > 0:
    print('Error, cannot install config.py file')
    exit(1)
else:
    print('Added config.py for config paramecio')

#Create certs

ssl_path="/home/"+user+"/ssl"

if call("sudo mkdir "+ssl_path, shell=True) > 0:
    print('Error, cannot create ssl directory')
    exit(1)
else:
    print('Added ssl directory for new certs')

if call("sudo openssl req -nodes -x509 -newkey rsa:4096 -keyout "+ssl_path+"/pastafari.key -out "+ssl_path+"/pastafari.crt -days 1024 -subj \""+args.cert+"\"", shell=True)>0:
    print('Error, cannot create the new cert')
    exit(1)

#Copy ca.crt for authentication https

if call("sudo cp tmp/ca.crt "+ssl_path, shell=True) > 0:
    print('Error, cannot install ca.crt file')
    exit(1)
else:
    print('Installed ca.crt file')

#Add sudo configuration

f=open("tmp/supastafari")

supastafari=f.read()

f.close()

supastafari=supastafari.replace("pastafari ALL = NOPASSWD: /usr/bin/python3 modules/pastafari/daemon/daemon.py", user+" ALL = NOPASSWD: /usr/bin/python3 modules/pastafari/daemon/daemon.py")

f=open("tmp/new_supastafari", "w")

f.write(supastafari)

f.close()

if call("sudo cp tmp/new_supastafari /etc/sudoers.d/pastafari", shell=True) > 0:
    print('Error, cannot install sudoers file')
    exit(1)
else:
    print('Added sudoers file for pastafari command')

#Add new uwsgi configuration

f=open("tmp/pastafari-uwsgi.ini")

pastafari_uwsgi=f.read()

f.close()

pastafari_uwsgi=pastafari_uwsgi.replace('pastafari', user)

f=open("tmp/pastafari_uwsgi_new", "w")

f.write(pastafari_uwsgi)

f.close()

if call("sudo cp tmp/pastafari_uwsgi_new /etc/uwsgi/apps-enabled/pastafari.ini", shell=True) > 0:
    print('Error, cannot install uwsgi pastafari')
    exit(1)
else:
    print('Added uwsgi file for pastafari')

#Add nginx configuration and reload

f=open("tmp/pastafari-nginx.conf")

pastafari_nginx=f.read()

f.close()

#listen 2048;
#listen [::]:2048;
#/home/pastafari
# allow 192.168.1.1

pastafari_nginx=pastafari_nginx.replace('listen 8443', 'listen '+args.port)
pastafari_nginx=pastafari_nginx.replace('listen [::]:8443', 'listen [::]:'+args.port)

pastafari_nginx=pastafari_nginx.replace('/home/pastafari', '/home/'+user)

pastafari_nginx=pastafari_nginx.replace('allow 192.168.1.1', 'allow '+args.ip)

f=open("tmp/new_pastafari_nginx", "w")

f.write(pastafari_nginx)

f.close()

if call("sudo cp tmp/new_pastafari_nginx /etc/nginx/sites-enabled/pastafari.conf", shell=True) > 0:
    print('Error, cannot install pastafari nginx file')
    exit(1)
else:
    print('Added pastafari nginx file')

#Fix permissions
"""
if call("sudo chown -R root:root /etc/sudoers.d/pastafari", shell=True) > 0:
    print('Error, cannot update owners of supastafari file')
    exit(1)
else:
    print('Modify supastafari permissions')
"""

if call("sudo chown -R root:root /home/"+user+"/site/paramecio", shell=True) > 0:
    print('Error, cannot update owners of pastafari directory')
    exit(1)
else:
    print('Modify site permissions')
    
if call("sudo chmod a=x /home/"+user, shell=True) > 0:
    print('Error, updating permissions for pastafari home')
    exit(1)
else:
    print('Modify home permissions')
    
#Restart php5-fpm and nginx

if call("sudo systemctl restart nginx", shell=True) > 0:
    print('Error, cannot restart nginx')
    exit(1)
else:
    print('Nginx restarted')
    
if call("sudo systemctl restart uwsgi", shell=True) > 0:
    print('Error, cannot restart uwsgi')
    exit(1)
else:
    print('uwsgi restarted')

print('All things done. Pastafari running...')



