#!/usr/bin/python3

import sys
import os
import argparse
import paramiko
import logging
import getpass
from pathlib import Path
from protozoo.configclass import ConfigClass
from protozoo.configtask import ConfigTask
from collections import OrderedDict
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
        
config_task_reload=None

def make_task(rsa, ssh, task_name, features):
    
    global config_task_reload
    
    server=features['hostname']
    
    #Opening connection with log
    
    logs_path=ConfigClass.logs_path+'/'+server
    
    create_dir(logs_path)
    
    path_log=logs_path+'/'+task_name+'.log'
        
    logging.basicConfig(format='%(levelname)s: %(message)s', filename=path_log,level=logging.INFO)
    
    # Reload config for the task
    
    #Check if exists file with config_task
    
    #Need revision
    
    if config_task_reload==None:
        
        try:
    
            config_task_reload=import_module('settings.config_'+task_name)
            
        except:
            
            #print("Task need a settings.py in "+task_path)
            #exit(1)
            pass
        
    else:
        try:
            
            reload(config_task_reload)
            
        except:
            pass
            
    #       print("Task need a settings.py in "+task_path)
    #       exit(1)
    
    # Load config for this host for this task
    
    if 'config_task_server' not in locals():
        
        try:
    
            config_task_server=import_module('settings.config_'+task_name+'_'+features['name'])
            
        except ImportError as e:
            
            #print("Error, cannot load config for settings.config_"+task_name+'_'+features['name']+": "+str(e))
            #exit(1)
            pass
        
    else:
        try:
            
            config_task_server=import_module('settings.config_'+task_name+'_'+features['name'])
            
        except:
            pass
    
    #Connect to the server
    
    logging.info("Connecting to the server...")
    
    
    try:
    
        ssh.connect(server, port=ConfigClass.port, username=ConfigClass.remote_user, password=None, pkey=rsa, key_filename=ConfigClass.private_key, timeout=None, allow_agent=True, look_for_keys=True, compress=False, sock=None, gss_auth=False, gss_kex=False, gss_deleg_creds=True, gss_host=None, banner_timeout=None)
    
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
    
    if len(ConfigTask.action)==0:
        logging.warning('Error, check your task. The number of actions in task is zero')
        exit(1)
    
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
			#, get_pty=True
            stdin, stdout, stderr = ssh.exec_command(command_to_execute)
            
            """
            while stdout.channel.exit_status_ready()!=True:
                line=stdout.readline()
                logging.info(action.codename+": "+line)
                
                line_err=stderr.readline()
                logging.warning(action.codename+" WARNING: "+line_err)
            """
            
            for line in stdout:
                logging.info(action.codename+": "+line)
                
            for line in stderr:
                logging.warning(action.codename+" WARNING: "+line)
            
            
            if stdout.channel.recv_exit_status()>0:
                #line=stdout.readlines()
                #logging.warning(action.codename+" WARNING: "+line)
                logging.warning("Error executing the task "+action.codename+".Please, view the log for more information: "+path_log)
                exit(1)
            
        except:
        
            e = sys.exc_info()[0]
            v = sys.exc_info()[1]
                
            logging.warning("Error: The server "+server+" show error %s %s" % (e, v))
            
            exit(1)
    
    ssh.close()
    
#def test_process():
#   print("Executing new process...")
#   print('module name:', __name__)
#   if hasattr(os, 'getppid'):  # only available on Unix
#       print('parent process:', os.getppid())
#       print('process id:', os.getpid())

# Method for check the process
# If 
"""
def delete_process(process, process_to_delete):
    
    process_final=dict(process)
    
    for k_p, del_p in enumerate(process_to_delete):
            del process_final[del_p]
            
    return (process_final, [])
"""

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
                    
                    ConfigClass.num_errors+=1
                    
                    if ConfigClass.stop_if_error == True:
                        finish=False
                        finish_processes=True
                        
                else:
                    ConfigClass.num_success+=1
                
                ConfigClass.num_total+=1
                
                process_to_delete.append(k)
                num_forks-=1
                end=finish

        #process, process_to_delete=delete_process(process, process_to_delete)
        for k_p, del_p in enumerate(process_to_delete):
            process.pop(del_p)

        process_to_delete=[]
        
        if(ConfigClass.num_total==ConfigClass.num_servers):
            if percent<100:
                percent=100
                show_progress(percent)
            break
    
    if finish_processes==True:
        print(Style.BRIGHT+Fore.WHITE+Back.RED+"The process have errors and you specified close the operations if fail exists.The pendient processes were finished")
        exit(1)
    
    return (process, num_forks, percent)

# Prepare keys for ssh connection
def prepare_ssh_keys(password, num_tries=0):
    
    try:
        
        rsa=paramiko.RSAKey.from_private_key_file(ConfigClass.private_key, password)
        
    except (paramiko.ssh_exception.PasswordRequiredException, paramiko.ssh_exception.SSHException):
    
        num_tries+=1
    
        if num_tries<4:
        
            p=getpass.getpass('Password for your ssh key:')
            
            rsa=prepare_ssh_keys(p, num_tries)
        
        else:
        
            print(Style.BRIGHT+Fore.WHITE+Back.RED+"This private key need a password if you want execute the tasks...")
        
            return None
    
    return rsa

def create_dir(path, permissions=0o755):

    p=Path(path)
    
    if not p.exists():
        p.mkdir(permissions, True)
        
    if p.exists() and p.is_dir()==False:
        print("Error: exists a file with the same path of directory to create: "+path)
        exit(1)

def start():
    
    pyv=python_version_tuple()

    if pyv[0]!='3':
        print('Need python 3 for execute this script')
        sys.exit(1)
    
    parser = argparse.ArgumentParser(description='An IT tool for make tasks in servers. Is used for SPanel for add new modules to the servers and others tasks')

    parser.add_argument('--task', help='The task to execute', required=True)
    parser.add_argument('--profile', help='The profile used for make tasks', required=False)
    parser.add_argument('--resume', help='If error, begin the tasks in the server where the fail ', required=False, nargs='?', const='1')
    parser.add_argument('--json', help='Save the progress in an file in json format', required=False, nargs='?', const='1')
    
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
    
    ConfigClass.password_key=None

    task_name=os.path.basename(args.task)
    
    task=args.task.replace('.','_')
    
    task=args.task.replace('/','.')
    
    # Load Profile, you can put custom configclass configs in it
    
    try:
        
        profile=import_module('settings.'+args.profile)
        
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
        print("Error: cannot load the task, exists "+task_path+" file?")
        exit(1)
    # Load settings.py
    
    try:
        
        config=import_module('settings.config')
        
    except SyntaxError as e:
        
        print("Error: "+str(e))
        exit(1)
    except:
        pass
    
    #Check logs folder
    
    create_dir(ConfigClass.logs_path)
    
    #Prepare sftp and ssh
    
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    
    #Check if the unknown host keys are rejected or not
    
    if ConfigClass.deny_missing_host_key == False:
        
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
    #Prepare ssh keys
    
    rsa=prepare_ssh_keys(ConfigClass.password_key)
    
    if rsa==None:
        exit(1)
    
    #Make a trial with tmp path in remote server. Need this check because i don't want delete neccesary files from the server. 
    
    delete_tmp_files=ConfigClass.remote_path+'/'+ConfigClass.tmp_sftp_path+'/*'
            
    if delete_tmp_files == "//*":
        print("Error: your remote paths are bad defined")
        exit(1)
        
    
    # Iterate profile.
    
    #for (server, features) in profile.servers.items()
    
    num_forks=0
    
    p_server=OrderedDict()
    
    if __name__ == 'protozoo.main':
        
        ConfigClass.num_servers=len(profile.servers)
        
        c_servers=round(100/ConfigClass.num_servers)
        
        p_count=0
        
        #Open file where save servers failed and last server executed fine.
        
        file_resume=open(".resume.py", "w+")
        
        print(Fore.WHITE+Style.BRIGHT +"Welcome to Protozoo!!")
        print(Fore.YELLOW +"Executing task <"+task_name+"> in "+str(ConfigClass.num_servers)+" machines")
        print(Fore.WHITE+Style.BRIGHT +ConfigTask.info)
    
        show_progress(p_count)
    
        for features in profile.servers:
            
            p_server[features['hostname']] = Process(target=make_task, args=(rsa, client, task_name, features))
            p_server[features['hostname']].start()
            #p_server[features['hostname']].join()
            num_forks+=1
            
            #Check forks if error or stop, if stop num_forks-=1 and clean dictionary
            #If error, wait to the all process finish
            
            #Make checking 
            
            if num_forks >= ConfigClass.num_of_forks:
                p_server, num_forks, p_count=check_process(p_server, num_forks, True, p_count, c_servers)
            
        p_server, num_forks, p_count=check_process(p_server, num_forks, False, p_count, c_servers)
    
    print(Fore.YELLOW+Style.BRIGHT +"Results: success:"+str(ConfigClass.num_success)+', fails:'+str(ConfigClass.num_errors))
    
    print(Style.BRIGHT +"All tasks executed")
    
    #print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000)

