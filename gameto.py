#!/usr/bin/python3
import sys, traceback
import argparse
import ipaddress
from importlib import import_module
from platform import python_version_tuple

def start():
	
	pyv=python_version_tuple()

	if pyv[0]!='3':
		print('Need python 3 for execute this script')
		sys.exit(1)

	parser = argparse.ArgumentParser(description='An Tool for add new servers config to your protozoo setup. In future versions you can create servers using this tool')

	parser.add_argument('--ip_range', help='A range of ip\'s for the servers in format 192.168.1.5-192.168.1.33.')
	
	parser.add_argument('--ip_list', help='A list of ip\'s of new servers separed by ,')
	
	parser.add_argument('--remove_ip', help='If true, the ip list is used for delete servers', required=False, nargs='?', const='1')
	
	parser.add_argument('--os', help='The operating system of new servers', required=True)
	
	parser.add_argument('--domainname', help='The domain name of new servers', required=True)
	
	parser.add_argument('--type', help='The type of servers', required=True)
	
	parser.add_argument('--save_in_db', help='Save in a database (you need special config)', required=False, nargs='?', const='1')
	
	parser.add_argument('--profile', help='The profile where the servers are saved', required=True)

	args = parser.parse_args()
	
	if args.ip_range==None and args.ip_list==None:
		
		parser.error('You need --ip_range or --ip_list options')
	
	arr_ip=[]
	
	if args.ip_range is not None:
		range_ips=args.ip_range.split('-')
		
		try:
		
			ipaddress.ip_address(range_ips[0])

		except:
			parser.error('First element of ip range is not valid IPv4 or IPv6')
		
		try:
		
			ipaddress.ip_address(range_ips[1])

		except:
			parser.error('Second element of ip range is not valid IPv4 or IPv6')		
		
		for ipaddr in ipaddress.summarize_address_range( ipaddress.ip_address(range_ips[0]), ipaddress.ip_address(range_ips[1])):
			for ip in ipaddr:
				arr_ip.append(ip)
	
	elif args.ip_list is not None:
		ip_list=args.ip_list.split(',')
		
		for ip in ip_list:
			arr_ip.append(ipaddress.ip_address(ip))

	if len(arr_ip)>0:
		
		#Save
		if args.save_in_db==None:
			print('Saving new servers in file...')
			
			old_servers={}
			
			check_old=0
			
			try:
			
				servers=import_module('settings.'+args.profile)

				for k, server in enumerate(servers.servers):
					old_servers[server['ip']]=1

				check_old=1

			except:

				pass
			
			new_file='settings/'+args.profile+'.py'
			
			file_txt="#!/usr/bin/python3\n"
			file_txt+="servers=[]\n"
			
			for ip in arr_ip:
				prefix=''
				
				if args.type!=None:
					prefix="-"+args.type.replace('.', '-')
				
				old_servers[str(ip)]=old_servers.get(str(ip), 0)
				
				if old_servers[str(ip)]==0:
				
					hostname=str(ip).replace('.','')+prefix+'.'+args.domainname
					
					file_txt+="servers.append({'hostname': '"+hostname+"', 'os_codename': '"+str(args.os)+"', 'ip': '"+str(ip)+"', 'name': '"+str(hostname).replace('.', '_')+"'})\n"
				elif args.remove_ip=='1':
					
					old_servers[str(ip)]=0
					
					pass

			#Add old servers
			
			if check_old==1:
			
				for server in servers.servers:
					
					if old_servers[server['ip']]==1:
						
						file_txt+="servers.append({'hostname': '"+server['hostname']+"', 'os_codename': '"+server['os_codename']+"', 'ip': '"+server['ip']+"', 'name': '"+server['name']+"'})\n"
		
			#Save file

			file=open(new_file, 'w+')
			
			file.write(file_txt)
			
			file.close()
		else:
			#Import settings for db
			
			print('Saving new servers in database...')
			
			new_file='settings/'+args.profile+'.py'
			
			try:
			
				config_db=import_module('settings.config_db')
				
			except:
				
				print('You need a configuration file called config_db.py for use a database for save servers data. Also you need cromosoma module installed')
				
				print("Exception in user code:")
				print("-"*60)
				traceback.print_exc(file=sys.stdout)
				print("-"*60)
				
				exit(1)
			
			pass

			#Load model
			
			model=import_module('protozoo.models.servers')
			
			if args.remove_ip=='1':
			
				for ip in arr_ip:
					
					model.server.conditions='WHERE ip="'+str(ip)+'"'

					model.server.delete()
					
			else:
				
				for ip in arr_ip:
					
					#file_txt+="servers.append({'hostname': '"+hostname+"', 'os_codename': '"+str(args.os)+"', 'ip': '"+str(ip)+"', 'name': '"+str(hostname).replace('.', '_')+"'})\n"
					
					#Check if server exists in this profile
					
					model.server.conditions='WHERE ip="'+str(ip)+'" and profile="'+args.profile+'"'
					
					num_server=model.server.select_count()
					
					if num_server==0:
				
						if args.type!=None:
							type_server="-"+args.type.replace('.', '-')
						
						hostname=str(ip).replace('.','')+type_server+'.'+args.domainname

						arr_server={'hostname': hostname, 'os_codename': str(args.os), 'ip': str(ip), 'name': str(hostname).replace('.', '_'), 'type': args.type, 'profile': args.profile}
						
						model.server.insert(arr_server)
			#Save file
			
			file_txt="#!/usr/bin/python3\n\n"
			
			file_txt+="from protozoo.models.servers import server\n\n"
			file_txt+="from settings import config_db\n\n"
			
			file_txt+="servers=[]\n\n"
			
			file_txt+="server.conditions='where type=\""+args.type+"\" and profile=\""+args.profile+"\"'\n\n"
			
			file_txt+="cur=server.select()\n\n"
			
			file_txt+="for row in cur:\n"
			
			file_txt+="    servers.append(row)\n"

			file=open(new_file, 'w+')
			
			file.write(file_txt)
			
			file.close()
			