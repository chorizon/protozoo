#!/usr/bin/python3

import argparse
import subprocess

parser = argparse.ArgumentParser(description='A script for install the scripts')

parser.add_argument('--user', help='The user where save the scripts, need exists...', required=True)

args = parser.parse_args()

user=args.user

if subprocess.call("git clone https://github.com/chorizon/debian-mail-unix /home/"+user+"/virus/scripts/mail/mail_unix",  shell=True) > 0:
    print('Error')
    exit(1)
else:
    print('Mail Unix module installed successfully')

