#!/usr/bin/python3

import os

class ConfigClass:
	
	#Local paths
	
	base_path=os.path.dirname(os.path.dirname(__file__))
	
	tasks_path=['tasks', 'protozoo.tasks']
	
	scripts_path=['scripts', base_path+'/protozoo/scripts']
	
	logs_path='logs'
	
	#Remote paths
	
	remote_path='/home/spanel'
	
	#Relative to remote_path
	
	tmp_sftp_path='tmp'
	
	remote_user='spanel'
	
	#Local home
	
	home=''
	
	#SSH configuration
	
	public_key=''
	
	private_key=''
	
	password_key=None

	port=22
	
	deny_missing_host_key=True
	
	#Internal tasks
	
	num_of_forks=10
	
	stop_if_error=False
	
	num_errors=0
	
	num_success=0
	
	num_total=0
	
	num_servers=0
	
	file_resume=None