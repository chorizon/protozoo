#!/usr/bin/python3

import sys
import subprocess
import argparse
import platform

pyv=platform.python_version_tuple()

if pyv[0]!='3':
	print('Need python 3 for execute this script')
	sys.exit(1)

parser = argparse.ArgumentParser(description='Script for download chorizon.')

parser.add_argument('--path', help='The path of directory where chorizon based is insalled', required=True)

args = parser.parse_args()


if subprocess.call("sudo git clone https://github.com/chorizon/libraries.git "+args.path+"/chorizon/libraries ",  shell=True) > 0:
	print('Error')
	sys.exit(1)
else:
	print('Chorizon base installed successfully')
	sys.exit(0)

