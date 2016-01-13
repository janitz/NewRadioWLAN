#import things...
import subprocess
import threading

class PlayerThread(threading.Thread):
	
	def __init__(self, data, lock):
		super().__init__()
		self.data = data
		self.lock = lock

	def findBetween(self, s, first, last ):
		try:
			start = s.index( first ) + len( first )
			end = s.index( last, start )
			return s[start:end]
		except ValueError:
			return ""
		
	def run(self):
		while True:
			try:
				info = subprocess.check_output('mpc', timeout=0.5).decode('utf-8')	
			except:
				info = ""
				
			lines = info.splitlines()
			
			''' playing case'''
			#DASDING: /// DASDING MIT DOMINIK ///
			#[playing] #1/1 2:53/0:00 (0%)
			#volume: 85%   repeat: off   random: off   single: off   consume: off
			#
			
			''' not playing case'''
			#volume: 85%   repeat: off   random: off   single: off   consume: off
			#
				
			if lines[0].startswith("volume:"):
				#nothing playing
				station = ""
				text = ""
				volLine = 0
				playing = False
				
			else:
				try:
					splitIndex = lines[0].index(": ")
					station = lines[0][:splitIndex]
					text = lines[0][splitIndex + 2:]
				except:
					station = ""
					text = ""
				volLine = 2
				playing = True
			
			try:
				volume = int(self.findBetween(lines[volLine], "volume:", "%"))
			except:
				volume = 0
				
			
			try:
				wlanInfo = subprocess.check_output('iwconfig wlan0', shell=True, timeout=0.5).decode('utf-8')
				wlan = int(self.findBetween(wlanInfo, "Signal level=", "/100 "))
			except:
				wlan = 0
					
			with self.lock:
				data["Station"] = station
				data["Text"] = text
				data["Volume"] = volume
				data["WLAN"] = wlan
				data["Playing"] = playing
								
				

def getInformation():
	with lock:
		ret = data
	return ret
	
def play(url=""):
	if url != "":	
		subprocess.call('mpc clear' , shell=True)
		subprocess.call('mpc add ' + url  , shell=True)				
	subprocess.call('mpc play' , shell=True)

def volume(inc):	
	if inc >= 0:
		subprocess.call('mpc volume +' + str(inc)  , shell=True)				
	else:
		subprocess.call('mpc volume ' + str(inc)  , shell=True)
	
data = {}
lock = threading.Lock()	
thread = PlayerThread(data, lock)
thread.daemon = True
thread.start()