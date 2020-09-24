# This program intend to scan network and have record of network connections
# and a record of network traffic on a Data base. It has to follow
# the nect steps
"""
1) scan current devices on network 
2) Save data about time of connection, Mac address, ip addrss, 
3) If there is a new device not stored on db, going to be added to db with its data
4) Start capturing data about network traffic.(ips address, services, time of data collection, etc)
5) Take time about connection to network
6) Need to find a way of kicking people from wifi
7) Have a record when the system was shuted down or turned on
8) Flask app to present data
9) Find a way to add name to the ips addrss
"""
import sqlite3
import nmap
from getmac import get_mac_address
from datetime import datetime
import sqlite3
from sqlite3 import Error
import json
import requests

class MainCode(object):
	def __init__(self):
		ip = input(" Enter default IP Address (default ip addrss will be set if no input): ")
		self.ip = ip
		self.conn = None

	def db_connection(self):
		try :
			self.conn = sqlite3.connect('network_db.db')
			self.c = self.conn.cursor()
		except Error as e:
			print(e)

	def __Get_Mac(self, IP='192.168.1.1'):
		mac = get_mac_address(ip=IP)
		return mac

	# Function for getting the mac address vendor(recognizing the company)
	def mac_vendor(self, MAC_ADD = 'BC:92:6B:A0:00:01'):
		try:
			MAC_URL = 'http://macvendors.co/api/%s'
			r = requests.get(MAC_URL % MAC_ADD ) #Here hoes the mac address
			res = r.json()
			macvend = res['result']['company']
			return macvend
		except:
			print('Unable to get mac vendors')
			pass

	def print_database(self):
		try : 
			print('Data in database')
			self.c.execute('SELECT * FROM thehosts')
			rows = self.c.fetchall()
			for row in rows:
				print(row)

		except:
			print('No previous data ... continue to scan the network')

	def networkscanner(self):
		if len(self.ip) == 0:
			network = '192.168.100.1/24'
		else:
			network = self.ip + '/24'
		print('Initializing Scan....')
		print('.... W A I T ....')


		# Nmap Scanning
		nm = nmap.PortScanner()

		# Loop for continue scanning

		while True:
			nm.scan(hosts = network, arguments = '-sn')
			hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]

			for host, status in hosts_list:
				# Check if exists previous record, if not, add the data to db
				self.c.execute('''SELECT ip_address FROM thehosts WHERE ip_address=?''', (host,))
				result = self.c.fetchone()
				if  result:
					pass
				else:
					mac = self.__Get_Mac(IP=host)
					macvend = self.mac_vendor(MAC_ADD = mac)
					self.c.execute('''INSERT INTO thehosts(ip_address, mac_address, mac_vendor) VALUES (?, ?, ?)''',(host, mac, macvend))
					self.conn.commit()
					print("Host\t{} : \t{} : \t{}".format(host, mac, macvend))


if __name__ == "__main__":
	D = MainCode()
	D.db_connection()
	D.print_database()
	D.networkscanner()