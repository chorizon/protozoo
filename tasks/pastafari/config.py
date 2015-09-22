#!/usr/bin/python3

from protozoo.configtask import ConfigTask, ConfigAction

from protozoo.configtasks.prebuildtask import NginxAction, PhpFpmAction, Python3Action, GitAction

PastafariAction=ConfigAction()

PastafariAction.codename='pastafari'
PastafariAction.name='Pastafari'
PastafariAction.description='Install pastafari API in a server'
PastafariAction.script_path='apis/pastafari/install.py'
PastafariAction.script_interpreter='python3'

#You need define secret key and ip --secret_key the_secret_key --ip 192.168.1.1

PastafariAction.parameters='--user pastafari --port 2048'
PastafariAction.extra_files=['apis/pastafari/files/php-fpm/pastafari-fpm.conf', 'apis/pastafari/files/nginx/pastafari-nginx.conf', 'apis/pastafari/files/sudo/supastafari', 'apis/pastafari/files/phango/config.php', 'apis/pastafari/files/phango/composer.json']


ConfigTask.task='pastafari'
ConfigTask.info="Installing pastafari api in servers..."
#, PastafariAction
ConfigTask.action=[Python3Action, NginxAction, PhpFpmAction, GitAction, PastafariAction]

