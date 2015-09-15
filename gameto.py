#!/usr/bin/python3

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
	
	parser.add_argument('--prefix', help='A prefix used for define things in the hostname')
	
	#parser.add_argument('--save_in_db', help='Save in a database (you need special config)', required=False, nargs='?', const='1')
	
	parser.add_argument('--file', help='The domain name of new servers', required=True)

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
		#if args.save_in_db==None:
		print('Saving new servers in file...')
		
		old_servers={}
		
		check_old=0
		
		try:
		
			servers=import_module('config.'+args.file)

			for k, server in enumerate(servers.servers):
				old_servers[server['ip']]=1

			check_old=1

		except:

			pass
		
		new_file='config/'+args.file+'.py'
		
		file_txt="#!/usr/bin/python3\n"
		file_txt+="servers=[]\n"
		
		for ip in arr_ip:
			prefix=''
			
			if args.prefix!=None:
				prefix="-"+args.prefix.replace('.', '-')
			
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

