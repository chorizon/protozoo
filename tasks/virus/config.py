#!/usr/bin/python3

from protozoo.configclass import ConfigClass 
from settings import config
from protozoo.configtask import ConfigTask, ConfigAction
from protozoo.configtasks.prebuildtask import GitAction

VirusAction=ConfigAction()

VirusAction.codename='virus'
VirusAction.name='A set of scripts for execute remote commands via ssh'
VirusAction.description='Install Virus scripts in a server'
VirusAction.script_path='apis/virus/install.py'
VirusAction.script_interpreter='python3'

#You need define secret key and ip --secret_key the_secret_key --ip 192.168.1.1

VirusAction.parameters='--user '+ConfigClass.remote_user
VirusAction.extra_files=['apis/virus/config.py']


ConfigTask.task='Virus API'
ConfigTask.info="Installing Virus api in servers..."
#, VirusAction
ConfigTask.action=[GitAction, VirusAction]

