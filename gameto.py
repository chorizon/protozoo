#!/usr/bin/python3

import argparse
import ipaddress
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

	args = parser.parse_args()

	if args.ip_range==None and args.ip_list==None:
		
		parser.error('You need --ip_range or --ip_list options')
	
	#print(args.ip_range)
	
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
		
		print("My new ip is "+str(arr_ip[0]))

		"""
		if len(range_ips)>2:
			parser.error('Sorry, the format of ip\s is for example: 192.168.1.5-192.168.2.33')

		if range_ips[0]<range_ips[1]:
			parser.error('Sorry, the range of ip\'s is not correct')
		"""
		"""
		if range_ips[1]>'255.255.255.255':
			parser.error('Sorry, the range of ip\'s is not correct.')
		"""
		"""
		try:
			

		comp_ip1=range_ips[0].split('.')
		comp_ip2=range_ips[1].split('.')
		
		if len(comp_ip1)<4 or len(comp_ip1)>4:
			parser.error('Sorry, the range of ip\'s is not correct')
			

		if len(comp_ip2)<4 or len(comp_ip2)>4:
			parser.error('Sorry, the range of ip\'s is not correct')
		"""
		"""
		calc_first=0
		calc_second=0
		calc_third=0
		calc_fourth=0
		"""
		#for x in range(0, 4):
		"""
		for first in range(int(comp_ip1[0]), int(comp_ip2[0])):
			calc_first+=1

		for second in range(int(comp_ip1[1]), int(comp_ip2[1])):
			calc_second+=1
				
		for third in range(int(comp_ip1[2]), int(comp_ip2[2])):
			calc_third+=1
		
		for fourth in range(int(comp_ip1[3]), int(comp_ip2[3])):
			calc_fourth+=1

		print(calc_fourth)
		"""
		"""
		calculate=True
		
		ip_new=[int(comp_ip1[0]), int(comp_ip1[1]), int(comp_ip1[2]), int(comp_ip1[3])]
		
		while(calculate):
			
			new_ip=str(ip_new[0])+'.'+str(ip_new[1])+'.'+str(ip_new[2])+'.'+str(ip_new[3])
			
			print(new_ip)
			
			ip_new[3]+=1
			if ip_new[3]>255:
				ip_new[3]=0
				ip_new[2]+=1
				if ip_new[2]>255:
					ip_new[2]=0
					ip_new[1]+=1
					if ip_new[1]>255:
						ip_new[1]=0
						ip_new[0]+=1			
						if ip_new[0]>255:
							raise NameError('Sorry, cannot create an ip with a range > 255')

			#print(ip_new[0], ip_new[1], ip_new[2], ip_new[3])
			
			
			
			if new_ip==range_ips[1]:
				break
			
			pass
			"""

		#192.168.1.1 192.168.1.5
		#Need the num of ips and simply sum checking 255 value
		#192.168.0.1 - 192.168.1.1
		#       0   0  1 255
		
