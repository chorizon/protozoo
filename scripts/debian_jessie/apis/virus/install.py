#!/usr/bin/python3

from subprocess import call, Popen, PIPE
import argparse
import os

parser = argparse.ArgumentParser(description='A script for install the scripts')

parser.add_argument('--user', help='The user where save the scripts, need exists...', required=True)

args = parser.parse_args()

user=args.user

if call("git clone https://github.com/chorizon/virus.git /home/"+user+"/virus/",  shell=True) > 0:
    print('Error, cannot install Virus scripts')
    exit(1)
else:
    print('Installed Virus...')

f=open('tmp/config.py')

file_config=f.read()

file_config=file_config.replace('user_pastafari="spanel"', 'user_pastafari="'+user+'"')

f.close()

f=open("/home/"+user+"/virus/settings/config.py", 'w')

f.write(file_config)

f.close()

exit(0)

