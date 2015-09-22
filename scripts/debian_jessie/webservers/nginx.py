#!/usr/bin/python3

import subprocess

if subprocess.call("sudo apt-get -y install nginx",  shell=True) > 0:
	print('Error')
	exit(1)
else:
	print('Nginx installed successfully')
	exit(0)


