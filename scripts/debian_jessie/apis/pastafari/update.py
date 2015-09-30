#!/usr/bin/python3 -u

from subprocess import call, Popen, PIPE
import argparse
from os import chdir

parser = argparse.ArgumentParser(description='A script for install pastafari')

parser.add_argument('--user', help='The user for pastafari', required=True)

args = parser.parse_args()

user=args.user

if call("sudo php /home/"+user+"/site/pastafari/composer.phar -d=/home/"+user+"/site/pastafari/ update",  shell=True) > 0:
    print('Error, cannot update dependencies for phango')
    exit(1)
else:
    print('Updated phango')

"""    
chdir("/home/"+user+"/site/pastafari/modules/pastafari")

if call("sudo git pull",  shell=True) > 0:
    print('Error, cannot update dependencies for phango')
    exit(1)
else:
    print('Updated pastafari')
"""
