'''
Paspberry Pi 2 Internet Radio...
Richtig behinderter Name: T2_3100
Janis Dreischke, Lars Reimann, New Kids Junge!
'''

#import things...
import sys
import os

#use the LCD framebuffer
os.environ["SDL_FBDEV"] = "/dev/fb1"	

#own modules
import visu
import player
import radioTime
import inputs

#presets file
presetFile = "data/presets.list"
presets = []
	
#main function
def main():
	print((sys.version))
	
	#get presets
	getPresets()
	writePresets()
	
	
	inp = inputs.inputs()	
	stations = radioTime.Stations()
	
	menuList = ("Radio", "USB", "Settings")
	menuListSel = "Radio"
	stationListSel = ""
	activeStation = player.getInformation()["Station"]
	activePage = "Menu"
	activePageLast = "Menu"
	
	
	#init done, fade to main prog
	visu.explosion()
	
	#update screen and handle events
	running = True
	while running:
		action = inp.getInput()
	
		
		#Menu ----------------------------------------------------------------
		if activePage == "Menu":
			activeItem = menuList.index(menuListSel)
			if action == "up":
				activeItem -= 1
				if activeItem < 0: activeItem = 0
			elif action == "down":
				activeItem += 1
				if activeItem >= len(menuList): activeItem = len(menuList) - 1
			elif action == "enter":
				if menuListSel == "Radio":
					activePage = "StationSelect" if activeStation == "" else "Radio"
				else:
					activePage = menuListSel
			elif action == "back":
				activePage = activePageLast
			
			menuListSel = menuList[activeItem]

			visu.menu1(menuList, activeItem)

		
		#Radio ---------------------------------------------------------------
		elif activePage == "Radio":
			if action == "up":
				player.volume(2)
			elif action == "down":
				player.volume(-2)
			elif action == "enter":
				activePage = "StationSelect"
			elif action == "back":
				activePage = "Menu"
			
			info = player.getInformation()
			
			if info["Station"] == "":
					info["Station"] = activeStation
			if info["Station"] != activeStation:
				try:
					url = stations.stations[activeStation]
					del stations.stations[activeStation]
					stations.stations[info["Station"]] = url
					activeStation = info["Station"]
					stationListSel = activeStation
				except:
					pass
			
			visu.radio(activeStation, info["Text"], info["Volume"], info["WLAN"])
		
		#StationSelect -------------------------------------------------------
		elif activePage == "StationSelect":
			nameList = list(stations.stations.keys())
			nameList.sort(key=lambda x: x.lower()) #Case In-sensitive
			
			try:
				activeItem = nameList.index(stationListSel)
			except:
				activeItem = 0

			if action == "up":
				activeItem -= 1
				if activeItem < 0: activeItem = 0
			elif action == "down":
				activeItem += 1
				if activeItem >= len(stations.stations): activeItem = len(stations.stations) - 1
			elif action == "enter":
				if activeStation != stationListSel:			
					activeStation = stationListSel			
					stations.updateUrl(activeStation)
					player.play(stations.stations[activeStation])
				activePage = "Radio"	
			elif action == "back":
				activePage = "Menu" if activeStation == "" else "Radio"
			
			stationListSel = nameList[activeItem]
			
			visu.menu2(nameList, activeItem)

		
		#USB -----------------------------------------------------------------
		elif activePage == "USB":
			if action == "up":
				x = 0
				#volume up
			elif action == "down":
				x = 0
				#volume down
			elif action == "enter":
				activePage = "SongSelect"
			elif action == "back":
				activePage = "Menu"
				
			if action == "none":
				visu.usb()
			
		#Settings ------------------------------------------------------------
		elif activePage == "Settings":
			if action == "up":
				x = 0
				#foo
			elif action == "down":
				x = 0
				#foo
			elif action == "enter":
				x = 0
				#foo
			elif action == "back":
				activePage = "Menu"
			
			if action == "none":
				visu.settings()	
						
			

def getPresets():
	if os.path.isfile(presetFile):
		f = open(presetFile)
		lines = f.read().splitlines()
		for x in range(5):
			presets.insert(x, lines[x+1])
		f.close()
	else:
		for x in range(5):
			presets.insert(x, "")
			
	
def writePresets():
	open(presetFile, 'a').close()
	f = open(presetFile, 'w')
	f.truncate()
	f.write("Presets (don't erase the next 5 lines)\n")
	for x in range(5):
		f.write(presets[x])
		f.write('\n')
	f.close()
		

				
#start the script					
main()
	
		