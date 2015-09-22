from protozoo.configtask import ConfigAction

Python3Action=ConfigAction()
Python3Action.codename='python3'
Python3Action.name='Python Language'
Python3Action.description='Script language very powerful, very used for spanel for internal tasks'
Python3Action.script_path='languages/install_python.sh'
Python3Action.script_interpreter='sh'
Python3Action.parameters=''
Python3Action.extra_files=[]

ApacheAction=ConfigAction()

ApacheAction.codename='apache'
ApacheAction.name='Apache Webserver'
ApacheAction.description='Script for install the most famous webserver in the world for debian jessie'
ApacheAction.script_path='libraries/install_apache.py'
ApacheAction.script_interpreter='python3'
ApacheAction.parameters=''
ApacheAction.extra_files=['files/spanel.conf']

MariaDBAction=ConfigAction()

MariaDBAction.codename='mariadb'
MariaDBAction.name='MariaDB Database Server'
MariaDBAction.description='Script for install the most famous db server in debian jessie'
MariaDBAction.script_path='db/mariadb/mariadb.py'
MariaDBAction.script_interpreter='python3'
MariaDBAction.parameters=''
MariaDBAction.extra_files=[]

AliveAction=ConfigAction()

AliveAction.codename='Alive'
AliveAction.name='Alive Test'
AliveAction.description='Script for tests if servers are alive'
AliveAction.script_path='libraries/dummy.sh'
AliveAction.script_interpreter='sh'
AliveAction.parameters=''
AliveAction.extra_files=[]

UpdateAction=ConfigAction()

UpdateAction.codename='Update'
UpdateAction.name='Update a server'
UpdateAction.description='Script for update a server'
UpdateAction.script_path='libraries/update.sh'
UpdateAction.script_interpreter='sh'
UpdateAction.parameters=''
UpdateAction.extra_files=[]

NginxAction=ConfigAction()

NginxAction.codename='Nginx'
NginxAction.name='Install Nginx in a server'
NginxAction.description='Script for install nginx in servers'
NginxAction.script_path='webservers/nginx.py'
NginxAction.script_interpreter='python3'
NginxAction.parameters=''
NginxAction.extra_files=[]

PhpFpmAction=ConfigAction()

PhpFpmAction.codename='PhpFpm'
PhpFpmAction.name='Install PhpFpm in a server'
PhpFpmAction.description='Script for install php-fpm in servers'
PhpFpmAction.script_path='languages/php-fpm.py'
PhpFpmAction.script_interpreter='python3'
PhpFpmAction.parameters=''
PhpFpmAction.extra_files=[]

GitAction=ConfigAction()

GitAction.codename='Git'
GitAction.name='Install Git in a server'
GitAction.description='Script for install php-fpm in servers'
GitAction.script_path='cvs/git.py'
GitAction.script_interpreter='python3'
GitAction.parameters=''
GitAction.extra_files=[]
