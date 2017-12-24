import os
import time
import requests
import json
from bs4 import BeautifulSoup

mc_filename = 'start_MC.bat'
mc_miner_filename = 'EthDcrMiner64.exe'

ZEN_STATS_URL = 'https://zen-tw.gpumine.org/stats'
zen_filename = 'start_ZEN.bat'
zen_miner_filename = 'miner.exe'
MODE = '' # 'ZEN' or 'MC'

def start_mining(filename):
	try:
		os.startfile(filename)
	except Exception as e:
		print(str(e))
		
		
def stop_mining(filename):
	try:
		os.system('TASKKILL /F /IM ' + filename)
	except Exception as e:
		print(str(e))

	
def has_block():
	r = requests.get(ZEN_STATS_URL)
	soup = BeautifulSoup(r.text, 'html.parser')
	tags = soup.find_all('span', {'style':'float:right; color: red;'})
	for tag in tags:
		if 'of' in tag.text:
			return True
	return False


def main():
	global MODE	
	while True:
		valid_zen = has_block()
		print('live: MODE=' + MODE + ", valid_zen=" + str(valid_zen) + ",  " + time.ctime())
		if valid_zen and MODE != 'ZEN':
			stop_mining(mc_miner_filename)
			start_mining(zen_filename)
			MODE = 'ZEN'
			print('start ZEN')
		elif not valid_zen and MODE != 'MC':
			stop_mining(zen_miner_filename)
			start_mining(mc_filename)
			MODE = 'MC'
			print('start MC')
		elif valid_zen and MODE == 'ZEN':
			pass
		elif not valid_zen and MODE == 'MC':
			pass
		else:
			print('WHF')
		time.sleep(30)
		
		
main()