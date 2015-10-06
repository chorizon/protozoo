#!/usr/bin/python3

from protozoo.configtask import ConfigTask, ConfigAction

from protozoo.configtasks.prebuildtask import NginxAction, PhpFpmAction, Python3Action, GitAction

from protozoo.configtasks.uwsgi import uWsgiAction

from protozoo.configtasks.bottlepy import BottlePyAction

PastafariAction=ConfigAction()

PastafariAction.codename='pastafari'
PastafariAction.name='Pastafari'
PastafariAction.description='Install pastafari API in a server'
PastafariAction.script_path='apis/pastafaripy/install.py'
PastafariAction.script_interpreter='python3'

#You need define secret key and ip --secret_key the_secret_key --ip 192.168.1.1

PastafariAction.parameters='--user pastafari --port 2048'
PastafariAction.extra_files=['apis/pastafaripy/files/uwsgi/pastafari-uwsgi.ini', 'apis/pastafaripy/files/nginx/pastafari-nginx.conf', 'apis/pastafaripy/files/sudo/supastafari', 'apis/pastafaripy/files/paramecio/config.py', 'apis/pastafaripy/files/cacert/ca.crt', 'apis/pastafaripy/files/cacert/ca.key']


ConfigTask.task='pastafari'
ConfigTask.info="Installing pastafari api in servers..."
#, PastafariAction
ConfigTask.action=[Python3Action, GitAction, NginxAction, uWsgiAction, BottlePyAction, PastafariAction]

