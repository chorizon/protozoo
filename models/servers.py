#!/usr/bin/python3

from cromosoma.webmodel import WebModel
from cromosoma import corefields

#servers.append({'hostname': 'beta.toolapps.es', 'os_codename': 'ubuntu_trusty', 'ip': '82.223.253.160', 'name': 'beta_toolapps_es'})

server=WebModel('server')

server.register(corefields.CharField('hostname'))

server.register(corefields.CharField('os_codename'))

server.register(corefields.CharField('ip'))

server.register(corefields.CharField('name'))

server.register(corefields.CharField('type'))

server.register(corefields.CharField('profile'))

server.register(corefields.BooleanField('status'))

server.fields['ip'].index=True
