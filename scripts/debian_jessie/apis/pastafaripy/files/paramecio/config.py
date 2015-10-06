#!/usr/bin/python3

#from cromosoma.webmodel import WebModel

#Host/IP where bind the server

port=8443

debug=False

reloader=False

admin_folder='admin'

host='0.0.0.0'

allowed_ips=[]

#The theme by default

theme='default'

#Base directory for save modules

base_modules="modules"

#Type server used for connect to the internet...

server_used="wsgiref"

#Module showed in index

default_module="pastafari"

#Modules with permissions to access for users

modules=['pastafari']

#Activate sessions?

session_enabled=False

#Variables for beaker sessions

cookie_name = 'paramecio.session'

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': False,
    'session.data_dir': './sessions',
    'session.auto': True
}

cache_session_opts = {
    
}

#The base url 

base_url='/'

#Can be absolute or relative

media_url='/'

#SSL support built in server. You need cherrypy installed for use this.

ssl=False

# Cert file for ssl

cert_pem=''

# Key file for ssl

privkey_pem=''

#WARNING: only use this feature in development, not in production.

yes_static=False

#Database mysql config, if you want anything...

#WebModel.connections={'default': {'name': 'default', 'host': 'localhost', 'user': 'root', 'password': '', 'db': 'example', 'charset': 'utf8mb4', 'set_connection': False} }

#Secret key

SECRET_KEY='secret_key'

SECRET_KEY_HASHED_WITH_PASS='key_hashed'

#User for pastafari

user_pastafari='pastafari'

