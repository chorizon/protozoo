#!/usr/bin/python3 -u

#A simple script for install pastafari

from base64 import b64encode
from subprocess import call, Popen, PIPE
from pathlib import Path
from socket import gethostname
import argparse
import shutil
import os

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



#Install phango framework

if call("sudo git clone https://github.com/phangoapp/phango /home/"+user+"/site/pastafari",  shell=True) > 0:
    print('Error, cannot install Phango Framework')
    exit(1)
else:
    print('Created Phango Framework')

#Install pastafari, no necessary with new behaviour
"""
if call("sudo git clone https://github.com/chorizon/pastafari.git /home/"+user+"/site/pastafari/modules/pastafari/",  shell=True) > 0:
    print('Error, cannot install Pastafari module')
    exit(1)
else:
    print('Added pastafari module')

"""

#Install composer

if call("sudo php -r \"readfile('https://getcomposer.org/installer');\" | php",  shell=True) > 0:
    print('Error, cannot install Composer')
    exit(1)
else:
    print('Downloaded composer.phar')

if call("sudo mv composer.phar /home/"+user+"/site/pastafari/",  shell=True) > 0:
    print('Error, cannot move Composer')
    exit(1)
else:
    print('Moved composer.phar')

#Create composer.json
"""
if call("sudo php /home/"+user+"/site/pastafari/create_composer.php > tmp/composer.json",  shell=True) > 0:
    print('Error, cannot create composer.json')
    exit(1)
else:
    print('Created composer.json')
"""

if call("sudo mv tmp/composer.json /home/"+user+"/site/pastafari/",  shell=True) > 0:
    print('Error, cannot move composer.json')
    exit(1)
else:
    print('Moved composer.json')

#Add dependencies

if call("sudo php /home/"+user+"/site/pastafari/composer.phar -d=/home/"+user+"/site/pastafari/ install",  shell=True) > 0:
    print('Error, cannot update dependencies for phango')
    exit(1)
else:
    print('Updated phango')

#Configure Phango

secret_key=args.secret_key

# Generate random secret_key for pastafari. For this things i hate the python documentation

random_bytes = os.urandom(24)
secret_key_pastafari = b64encode(random_bytes).decode('utf-8').strip()

f=open('tmp/config.php')

config_php=f.read()

f.close()

config_php=config_php.replace('secret_key', secret_key_pastafari)

p = Popen(['php -r "echo password_hash(\''+secret_key_pastafari+'+'+secret_key+'\', PASSWORD_DEFAULT);"'], stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)

out, err = p.communicate()

if p.returncode!=0:
    print('Error, cannot load the new key for pastafari')
    exit(1)

secret_key_hashed=out.decode('utf-8').strip()

config_php=config_php.replace('the_pass', secret_key_hashed)

f=open("tmp/new_config.php", "w")

f.write(config_php)

f.close()

if call("sudo mv tmp/new_config.php /home/"+user+"/site/pastafari/settings/config.php", shell=True) > 0:
    print('Error, cannot install config.php file')
    exit(1)
else:
    print('Added config.php for config pastafari')

#Create certs

ssl_path="/home/"+user+"/ssl"

if call("sudo mkdir "+ssl_path, shell=True) > 0:
    print('Error, cannot create ssl directory')
    exit(1)
else:
    print('Added ssl directory for new certs')

if call("sudo openssl req -nodes -x509 -newkey rsa:4096 -keyout "+ssl_path+"/pastafari.key -out "+ssl_path+"/pastafari.crt -days 356 -subj \""+args.cert+"\"", shell=True)>0:
    print('Error, cannot create the new cert')
    exit(1)

#Add sudo configuration

f=open("tmp/supastafari")

supastafari=f.read()

f.close()

supastafari=supastafari.replace("pastafari ALL = NOPASSWD: /usr/bin/php /home/pastafari/site/pastafari/console.php", user+" ALL = NOPASSWD: /usr/bin/php /home/"+user+"/site/pastafari/console.php")

f=open("tmp/new_supastafari", "w")

f.write(supastafari)

f.close()

if call("sudo mv tmp/new_supastafari /etc/sudoers.d/pastafari", shell=True) > 0:
    print('Error, cannot install sudoers file')
    exit(1)
else:
    print('Added sudoers file for pastafari command')

#Add php-fpm configuration and reload

f=open("tmp/pastafari-fpm.conf")

pastafari_fpm=f.read()

f.close()

pastafari_fpm=pastafari_fpm.replace('user = pastafari', 'user = '+user)
pastafari_fpm=pastafari_fpm.replace('group = pastafari', 'group = '+user)

f=open("tmp/new_pastafari_fpm", "w")

f.write(pastafari_fpm)

f.close()

if call("sudo mv tmp/new_pastafari_fpm /etc/php5/fpm/pool.d/pastafari.conf", shell=True) > 0:
    print('Error, cannot install pastafari php-fpm file')
    exit(1)
else:
    print('Added pastafari php-fpm file')

#Reload php-fpm

#Add nginx configuration and reload

f=open("tmp/pastafari-nginx.conf")

pastafari_nginx=f.read()

f.close()

#listen 2048;
#listen [::]:2048;
#/home/pastafari
# allow 192.168.1.1

pastafari_nginx=pastafari_nginx.replace('listen 2048', 'listen '+args.port)
pastafari_nginx=pastafari_nginx.replace('listen [::]:2048', 'listen [::]:'+args.port)

pastafari_nginx=pastafari_nginx.replace('/home/pastafari', '/home/'+user)

pastafari_nginx=pastafari_nginx.replace('allow 192.168.1.1', 'allow '+args.ip)

f=open("tmp/new_pastafari_nginx", "w")

f.write(pastafari_nginx)

f.close()

if call("sudo mv tmp/new_pastafari_nginx /etc/nginx/sites-enabled/pastafari.conf", shell=True) > 0:
    print('Error, cannot install pastafari nginx file')
    exit(1)
else:
    print('Added pastafari nginx file')

#Fix permissions

if call("sudo chown -R root:root /etc/sudoers.d/pastafari", shell=True) > 0:
    print('Error, cannot update owners of supastafari file')
    exit(1)
else:
    print('Modify supastafari permissions')

if call("sudo chown root:root /home/"+user+"/site/pastafari", shell=True) > 0:
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
    
if call("sudo systemctl restart php5-fpm", shell=True) > 0:
    print('Error, cannot restart php5-fpm')
    exit(1)
else:
    print('Php5-fpm restarted')

print('All things done. Pastafari running...')



