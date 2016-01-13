import requests
import os
import time

#for search and deleting:
#print("---///--- Request: "
class Stations:
	
	def __init__(self):
		self.stationsFile = "data/station.list"
		self.stations = {}
		self.lastUpdate = 0
		self.getOffline(self.stationsFile)
		if time.time() - self.lastUpdate > 86400:
			self.downloadStations()
	
	def getOffline(self, filePath):
		self.stations["Empty..."] = "es_gayt_nicht"
		if os.path.isfile(filePath):
			f = open(filePath)
			lines = f.read().splitlines()
			f.close()

			try:
				self.lastUpdate = int(self.findBetween(lines[0], '"', '"'))
			except:
				self.lastUpdate  = 0
			
			count = int((len(lines) - 1) / 2)
			for x in range(count):
				nam = lines[x * 2 + 1]
				url = lines[x * 2 + 2]
				if url.startswith("http"):
					self.stations[nam] = url
			if len(self.stations) == 1 :
				self.lastUpdate = 0
			else:
				self.stations.pop("Empty...", None)
			
	def writeList(self, filePath):
		open(filePath, 'a').close()
		f = open(filePath, 'w')
		f.truncate()
		f.write('Last Update: "' + str(int(time.time())) + '" (unix time)\n')
		for key in self.stations:
			f.write(key)
			f.write('\n')
			f.write(self.stations[key])
			f.write('\n')
		f.close()
	
	def findBetween(self, s, first, last ):
		try:
			start = s.index( first ) + len( first )
			end = s.index( last, start )
			return s[start:end]
		except ValueError:
			return ""
			
			
	def downloadStations(self):
		url = "http://opml.radiotime.com/Browse.ashx?id=r100346&filter=s:popular&offset="
		newStations = {}
		for count in range(0, 4):
			try:
				print(("---///--- Request: " + url[:40]))
				r = requests.get(url + str(count * 25))
				content = self.findBetween(r.text, '<body>', '</body>')
		
				listRows = content.split('<outline')
				for row in listRows:
					#<outline type="audio" text="NAME" URL="URL" bitrate="128" reliability="93" guide_id="s25260" subtext="TEXT" genre_id="g141" formats="mp3" show_id="p260675" item="station" image="IMG_URL" current_track="TITLE" now_playing_id="s25260" preset_id="s25260"/>
					if self.findBetween(row, 'type="', '"') == "audio":
						stationName = self.findBetween(row, 'text="', '"')
						betweenParentheses = self.findBetween(stationName[::-1], ")" , "(")[::-1]
						stationName = stationName.replace( "(" + betweenParentheses + ")", "")
						newStations[stationName] = self.findBetween(row, 'URL="', '"')
				if len(newStations) > 0:
					self.stations = newStations
			except:
				print("something failed, probably this request " + url[:40])
				
				
				
	def updateUrl(self, name):
		url = self.stations[name]
		if url.startswith("http://opml.radiotime.com/Tune.ashx"):
			print(("---///--- Request: " + url[:40]))
			r = requests.get(url)
			link = r.text.splitlines()[0]
		else:
			link = url
			
		if link.startswith("http://") and link.endswith(".mp3"):
			self.stations[name] = link
		elif link.endswith(".m3u") or link.endswith(".wmx"):
			print(("---///--- Request: " + link[:40]))
			r = requests.get(link)
			for line in r.text.splitlines():
				if line.startswith("http://"):
					self.stations[name] = line
		elif link.endswith(".pls"):
			print(("---///--- Request: " + link[:40]))
			r = requests.get(link)
			for line in r.text.splitlines():
				if line.find("File1=") != -1:
					self.stations[name] = line.replace("File1=", "")
		else:
			self.stations[name] = link
		
		self.writeList(self.stationsFile)
