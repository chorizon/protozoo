from protozoo.configtask import ConfigAction

Python3Action=ConfigAction()
Python3Action.codename='python3'
Python3Action.name='Python Language'
Python3Action.description='Script language very powerful, very used for spanel for internal tasks'
Python3Action.script_path='libraries/install_python.sh'
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
MariaDBAction.script_path='libraries/install_mariadb.py'
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
