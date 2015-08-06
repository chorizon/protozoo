#!/usr/bin/python3

import sys
import os
import argparse
import paramiko
import logging
from pathlib import Path
from protozoo.configclass import ConfigClass
from protozoo.configtask import ConfigTask
from platform import python_version_tuple
from importlib import import_module, reload
from colorama import init, Fore, Back, Style
from multiprocessing import Process

#import resource

def show_progress(percent):
	
	#First clean
	
	sys.stdout.write("\rProgress: %d%%" % (percent))
	sys.stdout.flush()
	
	if percent >= 100:
		
		sys.stdout.write("\rProgress: %d%%" % (100))
		sys.stdout.flush()
		print("\r")
		

def make_task(ssh, task_name, features):
	
	server=features['hostname']
	
	#Opening connection with log
		
	path_log=ConfigClass.logs_path+'/'+server+'_'+task_name+'.log'
		
	logging.basicConfig(format='%(message)s', filename=path_log,level=logging.INFO)
	
	#print(Style.BRIGHT +"Executing tasks with codename "+task_name+" in host "+server+"...")
	#print(Style.BRIGHT+ "Executing tasks with codename "+task_name+" in host "+server+".\nYou can see the progress in this log: "+path_log+"\n")
	
	# Reload config for the task
	
	#Check if exists file with config_task
	
	if 'config_task' not in locals():
		
		try:
	
			import_module('config.config_'+task_name)
			
		except:
			
			#print("Task need a config.py in "+task_path)
			#exit(1)
			pass
		
	else:
		try:
			
			reload('config.config_'+task_name)
			
		except:
			pass
			
	#		print("Task need a config.py in "+task_path)
	#		exit(1)
	
	# Load config for this host for this task
	
	if 'config_task_server' not in locals():
		
		try:
	
			config_task_server=import_module('config.config_'+task_name+'_'+features['name'])
			
		except ImportError as e:
			
			#print("Error, cannot load config for config.config_"+task_name+'_'+features['name']+": "+str(e))
			#exit(1)
			pass
		
	else:
		try:
			
			config_task_server=import_module('config.config_'+task_name+'_'+features['name'])
			
		except:
			pass
	
	#Connect to the server
	
	logging.info("Connecting to the server...")
	
	
	try:
	
		ssh.connect(server, port=ConfigClass.port, username=ConfigClass.remote_user, password=ConfigClass.password_key, pkey=None, key_filename=ConfigClass.private_key, timeout=None, allow_agent=True, look_for_keys=True, compress=False, sock=None, gss_auth=False, gss_kex=False, gss_deleg_creds=True, gss_host=None, banner_timeout=None)
	
	except paramiko.SSHException as e:
		logging.warning("Error: cannot connect to the server "+server+" "+str(e))
		exit(1)
	
	except paramiko.AuthenticationException as e:
		logging.warning("Error: cannot connect to the server "+server+" "+str(e))
		exit(1)
		
	except paramiko.BadHostKeyException as e:
		logging.warning("Error: cannot connect to the server "+server+" "+str(e))
		exit(1)
		
	except OSError as e:
		logging.warning("Error: cannot connect to the server "+server+" "+str(e))
		exit(1)
		
	#Open sftp session
	
	try:
	
		sftp=ssh.open_sftp()
	
	except:

		logging.warning("Error using sftp:"+ str(sys.exc_info()[0]))
		exit(1)
		
	#Create tmp if not exists
	
	tmp_path=ConfigClass.remote_path+'/'+ConfigClass.tmp_sftp_path;
	
	try:
	
		stat_tmp=sftp.stat(tmp_path)
		
	except FileNotFoundError:
		
		#Mkdir directory
		sftp.mkdir(tmp_path)
	
	#check_tmp=Path(tmp_path)
	
	#if not check_tmp.exists():
		#check_tmp.mkdir(0o755, True)
	
	#Clean tmp dir first
	
	
	try:
		
		stdin, stdout, stderr = ssh.exec_command('rm -f -r '+tmp_path+'/*')
		
		if stdout.channel.recv_exit_status()>0:
			logging.warning("Error: cannot clean the tmp path")
			exit(1)
			
	except:
		logging.warning("Error deleting tmp:"+ str(sys.exc_info()[0]))
		exit(1)
	
	#logging.info("Running actions..., you can see the progress in this log: "+path_log)
	
	#Execute the task in the server
	
	for action in ConfigTask.action:
		
		logging.info("Begin task "+action.name+"...")
		
		#Upload files to the server
		
		logging.info("Uploading files for the task")
		
		#prepare paths for files
		
		script_file=os.path.basename(action.script_path)
		
		#Seeking task path

		#This loop need optimization, saving the checked scripts

		for p in ConfigClass.scripts_path:
			
			source_file=p+'/'+features['os_codename']+'/'+action.script_path
			
			#tpath=Path(source_file)
			
			if os.path.isfile(source_file):
				break
		
		#Destiny path in remote server
		
		dest_file=ConfigClass.tmp_sftp_path+'/'+script_file
		
		#Upload script file to execute
		
		try:
		
			sftp.put(source_file, dest_file, callback=None, confirm=True)
			
		except:

			logging.warning("Error uploading files:"+ str(sys.exc_info()[0]))
			exit(1)
		
		logging.info("Uploaded file:"+source_file)
		
		#Upload more files
		
		for extra_file in action.extra_files:
			
			extra_source_file=p+'/'+features['os_codename']+'/'+extra_file
			
			extra_dest_file=ConfigClass.tmp_sftp_path+'/'+os.path.basename(extra_file)
			
			try:
		
				sftp.put(extra_source_file, extra_dest_file, callback=None, confirm=True)
			
			except:

				logging.warning("Error uploading files:"+ str(sys.exc_info()[0]))
				exit(1)
			
			logging.info("Uploaded file:"+extra_source_file)
	
		#Execute the script
		
		command_to_execute=action.script_interpreter+" "+dest_file+" "+action.parameters
		
		try:
	
			stdin, stdout, stderr = ssh.exec_command(command_to_execute)
			
			for line in stdout.readlines():
				logging.info(action.codename+": "+line)
				
			for line in stderr.readlines():
				logging.warning(action.codename+" WARNING: "+line)
			
			if stdout.channel.recv_exit_status()>0:
				logging.warning("Error executing the task "+action.codename+".Please, view the log for more information: "+path_log)
				exit(1)
			
			
		except SSHException as e:
			logging.warning("Error: cannot connect to the server "+server+" "+str(e))
			exit(1)
		except:
			logging.warning("Error: A script show error"+str(sys.exc_info()[0]))
	
	ssh.close()
	
#def test_process():
#	print("Executing new process...")
#	print('module name:', __name__)
#	if hasattr(os, 'getppid'):  # only available on Unix
#		print('parent process:', os.getppid())
#		print('process id:', os.getpid())

# Method for check the process
# If 
		
def check_process(process, num_forks, finish=True, percent=0, c_servers=0):
	
	finish_processes=False
	
	end=False
	
	process_to_delete=[]
	
	while (end==False):
		for k, p in process.items():
			
			#Check if process live
			
			if not p.is_alive():
				
				percent+=c_servers
				
				show_progress(percent)
			
				#Check if error
				if p.exitcode>0:
					print("\r"+Style.BRIGHT+Fore.WHITE+Back.RED+"Error: server "+k+" report an error. Please, see in the log the fail.")
					if ConfigClass.stop_if_error == True:
						finish=False
						finish_processes=True
						
				
				process_to_delete.append(k)
				num_forks-=1
				end=finish
		
		for k_p, del_p in enumerate(process_to_delete):
			del process[del_p]
			del process_to_delete[k_p]
		
		if(len(process)==0):
			break
	
	if finish_processes==True:
		print(Style.BRIGHT+Fore.WHITE+Back.RED+"The process have errors and you specified close the operations if fail exists.The pendient processes were finished")
		exit(1)
	
	return (process, num_forks, percent)
	

def start():
	
	pyv=python_version_tuple()

	if pyv[0]!='3':
		print('Need python 3 for execute this script')
		sys.exit(1)
	
	parser = argparse.ArgumentParser(description='An IT tool for make tasks in servers. Is used for SPanel for add new modules to the servers and others tasks')

	parser.add_argument('--task', help='The task to execute', required=True)
	parser.add_argument('--profile', help='The profile used for make tasks', required=False)
	parser.add_argument('--resume', help='If error, begin the tasks in the server where the fail ', required=False)
	
	args = parser.parse_args()
	
	home=os.getenv("HOME")
	
	#Init colored terminal
	
	init(autoreset=True)
	
	#Prepare variables
	
	if args.profile == None:
		args.profile='servers'
	
	#Prepare routes for scripts and logs
	
	ConfigClass.scripts_path=['scripts', 'protozoo/scripts']
	
	ConfigClass.logs_path='logs'
	
	ConfigClass.public_key=home+'/.ssh/id_rsa.pub'
	
	ConfigClass.private_key=home+'/.ssh/id_rsa'
	
	ConfigClass.password_key=''

	task_name=os.path.basename(args.task)
	
	task=args.task.replace('.','_')
	
	task=args.task.replace('/','.')
	
	# Load Profile, you can put custom configclass configs in it
	
	try:
		
		profile=import_module('config.'+args.profile)
		
	except ImportError as e:
		
		print("Error, cannot find "+args.profile+" profile: "+str(e))
		exit(1)
	
	#Seeking task path
	
	for p in ConfigClass.tasks_path:
		
		task_path=p+'.'+task+'.config'
		
		task_path_route=task_path.replace('.','/')+'.py'
		
		#tpath=Path(task_path_route)
		
		if os.path.isfile(task_path_route):
			break
	
	# Load config for the task
	
	try:
		
		config_task=import_module(task_path)
		
	except SyntaxError as e:
		
		print("Error: "+str(e))
		exit(1)
	except:
		pass
	
	# Load config.py
	
	try:
		
		config=import_module('config.config')
		
	except SyntaxError as e:
		
		print("Error: "+str(e))
		exit(1)
	except:
		pass
	
	#Check logs folder
	
	p_logs=Path(ConfigClass.logs_path)
	
	if not p_logs.exists():
		p_logs.mkdir(0o755, True)
		
	if p_logs.exists() and p_logs.is_dir()==False:
		print("Error: exists a file with the same path of logs. Delete the file or change ConfigClass.logs_path ")
		exit(1)
	
	#Prepare sftp and ssh
	
	client = paramiko.SSHClient()
	client.load_system_host_keys()
	
	#Check if the unknown host keys are rejected or not
	
	if ConfigClass.deny_missing_host_key == False:
		
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	
	#Make a trial with tmp path in remote server. Need this check because i don't want delete neccesary files from the server. 
	
	delete_tmp_files=ConfigClass.remote_path+'/'+ConfigClass.tmp_sftp_path+'/*'
			
	if delete_tmp_files == "//*":
		print("Error: your remote paths are bad defined")
		exit(1)
	
	# Prepare keys for ssh connection
	
	#try:
	
		#rsa=paramiko.rsakey.RSAKey(msg=None, data=None, filename=ConfigClass.private_key, password=ConfigClass.password_key, vals=None, file_obj=None)
	#	rsa=paramiko.RSAKey.from_private_key_file(ConfigClass.private_key, ConfigClass.password_key)
		
	#except paramiko.ssh_exception.PasswordRequiredException:
		
	#	print("This private key need a password")
	#	exit(1)
		
	
	# Iterate profile.
	
	#for (server, features) in profile.servers.items()
	
	num_forks=0
	
	p_server={}
	
	if __name__ == 'protozoo.main':
		
		c_servers=round(100/len(profile.servers))
		
		p_count=0
		
		print(Fore.YELLOW +"Executing tasks...")
	
		show_progress(p_count)
	
		for features in profile.servers:
			
			p_server[features['hostname']] = Process(target=make_task, args=(client, task_name, features))
			p_server[features['hostname']].start()
			#p_server[features['hostname']].join()
			num_forks+=1
			
			#Check forks if error or stop, if stop num_forks-=1 and clean dictionary
			#If error, wait to the all process finish
			
			#Make checking 
			
			if num_forks >= ConfigClass.num_of_forks:
				p_server, num_forks, p_count=check_process(p_server, num_forks, True, p_count, c_servers)
			
		p_server, num_forks, p_count=check_process(p_server, num_forks, False, p_count, c_servers)
	
	print(Style.BRIGHT +"All tasks executed")
	
	#print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000)

