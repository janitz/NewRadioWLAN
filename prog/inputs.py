import pygame
from pygame.locals import * #the pygame constants
from queue import Queue
import RPi.GPIO as GPIO
import sys

class inputs:
	
	#constructor
	def __init__(self):
		
		self.pins = {}
		self.pins["power"] = 14
		self.pins["enter"] = 17
		self.pins["back"] = 4
		self.pins["inc1"] = 22
		self.pins["inc2"] = 27
		self.pins["pre1"] = 26
		self.pins["pre2"] = 19
		self.pins["pre3"] = 13
		self.pins["pre4"] = 6
		self.pins["pre5"] = 5
		self.pins["but1"] = 16
		self.pins["but2"] = 20
		self.pins["but3"] = 21
		
		#for save Last GPIO states
		self.encoder = 0
		self.actions = Queue()
		
		pygame.init()
		
		#init the GPIOs
		GPIO.setmode(GPIO.BCM) #use the pin names printed on the board
		for key in self.pins:	
			GPIO.setup(self.pins[key], GPIO.IN, pull_up_down=GPIO.PUD_UP)
			GPIO.add_event_detect(self.pins[key], GPIO.BOTH, callback=self.gpioEvent)		
	
	def gpioEvent(self, channel):
		if channel == self.pins["enter"] and GPIO.input(channel):
			self.actions.put("enter")
		if channel == self.pins["back"] and GPIO.input(channel):
			self.actions.put("back")
		if channel == self.pins["inc1"] or channel == self.pins["inc2"]:
			temp = self.getRotaryEncoder()
			if temp != "none":
				self.actions.put(temp)
		
		
		
	
	def getInput(self):
		if self.actions.empty():
			ret = self.getKeyboard()
		else:
			ret = self.actions.get()
		return ret
	
	
	#function for checking rotary encoder					
	def getRotaryEncoder(self):
		encoderLast = self.encoder
		self.encoder = 0 if GPIO.input(self.pins["inc1"]) else 1
		self.encoder += 0 if GPIO.input(self.pins["inc2"]) else 2
		if self.encoder == 0:
			if encoderLast == 1:
				return "down"
			elif encoderLast == 2:
				return "up"
		elif self.encoder == 3:
			if encoderLast == 1:
				return "up"
			elif encoderLast == 2:
				return "down"
		else:
			return "none"
	
	#function for checking the keyboard
	def getKeyboard(self):
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()
				elif event.key == K_UP:
					return("up")	
					
				elif event.key == K_DOWN:
					return("down")
					
				elif event.key == K_RETURN:
					return("enter")
					
				elif event.key == K_BACKSPACE:
					return("back")
				
				elif event.key == K_1:
					return("pre1")
				
				elif event.key == K_2:
					return("pre2")
				
				elif event.key == K_3:
					return("pre3")
				
				elif event.key == K_4:
					return("pre4")
				
				elif event.key == K_5:
					return("pre5")
				
				elif event.key == K_F1:
					return("but1")
				
				elif event.key == K_F2:
					return("but2")
				
				elif event.key == K_F3:
					return("but3")
				
				elif event.key == K_ESCAPE:
					return("power")
		return "none"


