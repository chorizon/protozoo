#!/usr/bin/python3

from subprocess import call, Popen, PIPE
import argparse

parser = argparse.ArgumentParser(description='A script for install the scripts')

parser.add_argument('--user', help='The user where save the scripts, need exists...', required=True)

args = parser.parse_args()

user=args.user

if call("sudo git clone https://github.com/chorizon/virus.git /home/"+user+"/virus/",  shell=True) > 0:
    print('Error, cannot install Paramecio Framework')
    exit(1)
else:
    print('Installed Virus...')

exit(0)

