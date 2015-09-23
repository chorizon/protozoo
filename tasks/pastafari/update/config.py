#!/usr/bin/python3

from protozoo.configtask import ConfigTask, ConfigAction

#from protozoo.configtasks.prebuildtask import NginxAction, PhpFpmAction, Python3Action, GitAction

UpdateAction=ConfigAction()

UpdateAction.codename='pastafari_update'
UpdateAction.name='Pastafari Update'
UpdateAction.description='Update pastafari API in a server'
UpdateAction.script_path='apis/pastafari/update.py'
UpdateAction.script_interpreter='python3'

UpdateAction.parameters='--user pastafari'

ConfigTask.task='pastafari'
ConfigTask.info="Updating pastafari api in servers..."
#, UpdateAction
ConfigTask.action=[UpdateAction]

