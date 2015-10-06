from protozoo.configtask import ConfigAction

uWsgiAction=ConfigAction()
uWsgiAction.codename='uwsgi'
uWsgiAction.name='uWsgi daemon for serve python apps and others'
uWsgiAction.description='Daemon WSGI for server python apps and others'
uWsgiAction.script_path='webservers/python3/uwsgi.py'
uWsgiAction.script_interpreter='python3'
uWsgiAction.parameters=''
uWsgiAction.extra_files=[]

