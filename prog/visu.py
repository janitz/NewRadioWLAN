#import things...
import math
import datetime
import pygame #the graphic engine
from pygame.locals import * #the pygame constants
import threading

class PagesThread(threading.Thread):
	
	#constructor
	def __init__(self, data, lock):
		super().__init__()
		self.data = data
		self.lock = lock	
		
		self.dat = {}
		
		#initialize the gui
		pygame.init()
		pygame.mouse.set_visible(False)
		pygame.mixer.init()
		
		#   colors     R    G    B
		self.white = (255, 255, 255)
		self.green = ( 80, 255,  45)
		self.black = (  0,   0,   0)
		
		#main components for the gui
		fontName = "skin/MachineItcDEE.ttf"
		self.screen = pygame.display.set_mode((320, 240))
		self.background = pygame.image.load("skin/background.png")
		
		#time label
		self.timeFont = pygame.font.Font(fontName, 70)
		self.dateFont = pygame.font.Font(fontName, 30)
		
		#startup
		self.startup = pygame.image.load("skin/startup.png")
		
		#menu1
		self.menu1Line = pygame.image.load("skin/menu1.png")
		self.menu1Font = pygame.font.Font(fontName, 40)
		
		#menu2
		self.menu2Line = pygame.image.load("skin/menu2.png")
		self.menu2Scrollbar = pygame.image.load("skin/scrollbar.png")
		
		self.menu2Fonts = {}
		for x in range(0, 5):
			size = 40 - (7 * x)
			self.menu2Fonts[x] = pygame.font.Font(fontName, size)
		
		#radio
		self.radioFont = pygame.font.Font(fontName, 40)
		self.radioVolPic = pygame.image.load("skin/volume.png")	
		
		self.radioStationLast = ""	
		self.radioStationPos = 10
		self.radioStationWait = 100
		
		self.radioTextLast = ""
		self.radioTextPos = 10
		self.radioTextWait = 100
		
		self.radioVolumeLast = -1
		self.radioVolumeWait = 0
		
		self.radioWlanPics = {}
		for x in range(0, 5):
			picName = "skin/wlan/wlan" + str(x) + ".png"
			self.radioWlanPics[x] = pygame.image.load(picName)

		
	def run(self):
		while True:
			#copy the shared data
			with self.lock:
				self.dat = self.data.copy()
			
			if self.dat["activePage"] == "startupScreen":
				self.startupScreen()
			elif self.dat["activePage"] == "explosion":
				self.explosion()
				with self.lock:
					self.data["activePage"] = self.data["nextPage"]
			elif self.dat["activePage"] == "menu1":
				self.menu1()
			elif self.dat["activePage"] == "menu2":
				self.menu2()
			elif self.dat["activePage"] == "radio":
				self.radio()
			elif self.dat["activePage"] == "usb":
				self.usb()
			elif self.dat["activePage"] == "settings":
				self.settings()
			elif self.dat["activePage"] == "games":
				self.games()
			else:
				self.screen.fill(self.black)
			
			
			#write to screen max 30fps
			pygame.display.flip()
			pygame.time.Clock().tick(30)
		
	#function for adding a time label	
	def timeLabel(self):
		#get time and date
		currentTime = datetime.datetime.now().strftime('%H:%M')
		currentDate = datetime.datetime.now().strftime('%d.%m.%Y')
		#render the strings
		labelTime = self.timeFont.render(currentTime, 1, self.white)
		labelDate = self.dateFont.render(currentDate, 1, self.white)
		#add to screen
		self.screen.blit(labelTime, (315-labelTime.get_width(), -14))
		self.screen.blit(labelDate, (315-labelDate.get_width(), 55))

	#function for startup screen
	def startupScreen(self):
		self.screen.blit(self.startup, (0, 0))
		
	#function for awsome fadings
	def explosion(self):		
		pygame.mixer.music.stop()
		pygame.mixer.music.load("sound/feuerball.mp3")
		pygame.mixer.music.play()
		for pic in range(0,6):
			picName = "skin/explosion/exp" + str(pic) + ".png"
			exp = pygame.image.load(picName)
			self.screen.blit(exp, (0, 0))
			pygame.display.flip()
			pygame.time.Clock().tick(15)	
	
	#first menu page (main menu)		
	def menu1(self):

		menuList = self.dat["menuList"]		
		selectedItem = self.dat["selectedItem"]

		#calculate listlength
		count = len(menuList)
			
		#background, underscore, time and date
		self.screen.blit(self.background, (0, 0))
		self.screen.blit(self.menu1Line, (16, 133))
		self.timeLabel()
		
		#render the items and place them right
		for x in range(-3, 4):
			col = self.green if x==0 else self.white
			if (0 <= (selectedItem + x) < count):
				labelText = menuList[selectedItem + x]
				label = self.menu1Font.render(labelText, 1, col)
				labelMid = label.get_width() / 2
				xPos = 90 - labelMid
				yPos = (x * 38) + 90
				self.screen.blit(label, (xPos, yPos))
		
	
	#second menu page (station select)		
	def menu2(self):
		
		menuList = self.dat["menuList"]		
		selectedItem = self.dat["selectedItem"]
		
		#calculate listlength
		count = len(menuList)
		
		#background, underscore
		self.screen.blit(self.background, (0, 0))
		self.screen.blit(self.menu2Line, (20, 133))
		
		#render the items and place them right
		for x in range(-4, 5):
			col = self.green if x==0 else self.white
			if (0 <= (selectedItem + x) < count):
				labelFont = self.menu2Fonts[math.fabs(x)]
				labelText = menuList[selectedItem + x]
				label = labelFont.render(labelText, 1, col)
				xPos = 40 - (3 * x * x)
				yPos = (x * 37 ) + 90 + math.fabs(5 * x) - (5 * x * math.sqrt(math.fabs(x)))
				self.screen.blit(label, (xPos, yPos))
				
		# (30,0,label.get_width(),label.get_height())
		
		
		#scrollbar
		max_angle = 20
		angle = max_angle - (max_angle * 2 * (selectedItem + 0.5) / count)		
		#there's a problem with 0. it's no exception but looks ugly
		if -0.001 < angle < 0.001:
			angle = 0.001
		#rotozoom uses antialiasing, rotate doesn't'
		bar_angle = pygame.transform.rotozoom(self.menu2Scrollbar, angle, 1)
		xPos = -128 - (bar_angle.get_width() / 2)
		yPos = 120 - (bar_angle.get_height() / 2)
		self.screen.blit(bar_angle, (xPos, yPos))	
		
		
	#radio page
	def radio(self):
		station = self.dat["radioStation"]
		text = self.dat["radioText"]
		volume = self.dat["volume"]
		wlan = self.dat["wlan"]
		
		#background, time and date
		self.screen.blit(self.background, (0, 0))		
		self.timeLabel()
		
		#render the texts
		labelStation = self.radioFont.render(station, 1, self.white)
		labelText = self.radioFont.render(text, 1, self.white)
		
		#calculate the station name position
		if self.radioStationLast == station:
			#don't move if you fully fit on the screen
			if labelStation.get_width() < 300:
				self.radioStationPos = 10
				self.radioStationWait = 100
			#wait
			if self.radioStationWait > 0:
				self.radioStationWait = self.radioStationWait - 1
			else:
				#move
				self.radioStationPos = self.radioStationPos - 2	
				#if text is outside the display
				if (labelStation.get_width() + self.radioStationPos) < 0:
					#set new pos to the middle of the screen
					self.radioStationPos = 160	
				#if text is at the wait position
				elif 9 <= self.radioStationPos <= 11:
					self.radioStationWait = 100
		else:
			#reset the ticker position
			self.radioStationWait = 100
			self.radioStationPos = 10
			self.radioStationLast = station	
		
		
		#calculate the station text position
		if self.radioTextLast == text:
			#don't move if you fully fit on the screen
			if labelText.get_width() < 300:
				self.radioTextPos = 10
				self.radioTextWait = 100
			#wait
			if self.radioTextWait > 0:
				self.radioTextWait = self.radioTextWait - 1
			else:
				#move
				self.radioTextPos = self.radioTextPos - 2	
				#if text is outside the display
				if (labelText.get_width() + self.radioTextPos) < 0:
					#set new pos to the middle of the screen
					self.radioTextPos = 160	
				#if text is at the wait position
				elif 9 <= self.radioTextPos <= 11:
					self.radioTextWait = 100
		else:
			#reset the ticker position
			self.radioTextWait = 100
			self.radioTextPos = 10
			self.radioTextLast = text	
		
		
		#place the labels
		self.screen.blit(labelStation,(self.radioStationPos, 140))
		self.screen.blit(labelText,(self.radioTextPos, 180))
		
		#if only the end of the label is on screen
		if (self.radioStationWait == 0) and ((labelStation.get_width() + self.radioStationPos) < 160):
			#then put the start of the next label behind it
			self.screen.blit(labelStation,(self.radioStationPos + labelStation.get_width() + 162, 140))
		
		#if only the end of the label is on screen
		if (self.radioTextWait == 0) and ((labelText.get_width() + self.radioTextPos) < 160):
			#then put the start of the next label behind it
			self.screen.blit(labelText,(self.radioTextPos + labelText.get_width() + 162, 180))
		
		#first write
		if self.radioVolumeLast == -1:
			self.radioVolumeWait = 0
			self.radioVolumeLast = volume
		
		#volume changed
		if self.radioVolumeLast != volume:
			self.radioVolumeWait = 50
			self.radioVolumeLast = volume
		
		if self.radioVolumeWait > 0:
			self.radioVolumeWait = self.radioVolumeWait - 1
			volLabel = self.radioFont.render(str(volume), 1, self.white)
			pygame.draw.rect(self.screen, self.green, [9, 27, volume * 1.5 , 40])
			self.screen.blit(self.radioVolPic, (7, 25))
			self.screen.blit(volLabel, (105 - (volLabel.get_width() / 2), 20))
		else:
			picNr = math.ceil(wlan/20)
			self.screen.blit(self.radioWlanPics[picNr], (25, 25))
			
		
	#usb page
	def usb(self):
			self.screen.blit(pygame.image.load("skin/usb.png"), (0, 0))	
			
	#settings page
	def settings(self):
			self.screen.blit(pygame.image.load("skin/settings.png"), (0, 0))	
		
	#games page
	def games(self):
			self.screen.blit(pygame.image.load("skin/games.png"), (0, 0))	
		
	
	
	
	
#show the startup screen
def startupScreen():
	with lock:
		data["activePage"] = "startupScreen"

#show the explosion Fade
def explosion(nextPage = ""):
	with lock:
		data["activePage"] = "explosion"
		data["nextPage"] = nextPage

#show menu1
def menu1(menuList, selected):
	with lock:
		data["menuList"] = menuList
		data["selectedItem"] = selected
		data["activePage"] = "menu1"

#show menu2
def menu2(menuList, selected):
	with lock:
		data["menuList"] = menuList
		data["selectedItem"] = selected
		data["activePage"] = "menu2"

#call the radio page
def radio(station, text, volume, wlan):
	with lock:
		data["radioStation"] = station
		data["radioText"] = text
		data["volume"] = volume
		data["wlan"] = wlan
		data["activePage"] = "radio"

#show usb page
def usb():
	with lock:
		data["activePage"] = "usb"

#show settings page
def settings():
	with lock:
		data["activePage"] = "settings"

#show games page
def games():
	with lock:
		data["activePage"] = "games"


		
data = {}
data["activePage"] = "startupScreen"
lock = threading.Lock()	
thread = PagesThread(data, lock)
thread.daemon = True
thread.start()