#!/usr/bin/env python

#Structure of the data sent by the Zum

#end: Type, milis (for position calculation), orientation, sonarleft (L), sonarfront (F), sonarright (R). 
#ex:  '1 200 1 130 0 0 \n'
    #We are sending data having pass 200 seconds fro the last message we are turn 90 degrees 
    #and there is an object at left (wich is the original front if not accounting rotation.

#orientation:	-1 (-90)			0 (0)			1 (90)			2 (180)

#Type: 0(END), 1(DATA), 2(TURN).	

#Library imports
import time
import numpy as np
import matplotlib.pyplot as plt
import serial


#Variable declaration

port = '/dev/ttyUSB0'  #Adrees of the Zum. TODO: Can this be automatic?.
bauds = 19200          #Default of serial communication with the Zum BT-328(http://diwo.bq.com/product/placa-zum-bt-328)

mssInfo = {'END' : 0, 'DATA' : 1, 'TURN' : 2}     #Definition of the type of message that can be recive

x = -150                  #Starting (x,y) of the robot
y = 0

mssType =''            #Some variable inicialization for the loops
initial = True

speed = 0.01              #TODO: Transmited by the Zum
                          #Testing speed for now

roomWidth  = 3*100        #Some inicialization for mathplot library
roomHeight = 3*100        #TODO: DECISION: Introduce by the user?

#Functions

def connect(port, bauds):
	"Setting up the serial library"	
	while True:
		try:
			ser = serial.Serial(port, bauds)            #Cheking for the Zum being connected
			break
		except serial.serialutil.SerialException:       #Informing in case it isnt connected
			print("Zum not connected")
	return ser

def initialize(ser):
	"Initialize comuncation, eliminating the posible initial garbage"
	for i in range(10):                                 #In case we start the program with the Zum already connected
		data = ser.readline()[:-2]                      #we drop 10 lines, in order to ensure the first line read is complete

def read(ser):
	"Reading one string of data"					
	mss = ser.readline()[:-2]        #We read until an \n, wich menas endind in the Zum with a Serial.println(), 
	return mss                       #we use [:-2] to get rid od the last two characters, the \n

def endConnect():
	"Ending the communications"		
	ser.close()       #Closing the serial communication

#classes
class dot(object):
	def __init__(self, x, y):          #Data for the dot to be represented on the plot
		self.x = x
		self.y = y

class room(object):
	def __init__(self, width, height):                   #Height and width of the scaning room.
		self.width = width
		self.height = height

ser = connect(port, bauds)
initialize(ser)

r = room(roomWidth, roomHeight)
plt.axis([-1*r.width/2 +0.1, r.width/2+0.1, -1*r.height/2+0.1,r.height/2+0.1])    #Defining axis width and height
plt.ion()                                                                         #Activates interactive mode, allowing to plot while running
plt.show()                                                                        

while mssType != mssInfo['END']:
	#Reading the data
	mss = read(ser)
	print(mss)

	msplit = mss.split()	          #We split the message based on white space sparation, its important then to do this on the Zum

	mssType  = int(msplit[0])   #What kind of message is this
	mssMilis = int(msplit[1])   #The time since the Zum program began
	if mssType == mssInfo['DATA']:        #Only in case we are sending data we want to process it
		mssOrientation  = int(msplit[2])   #The current orientation of the Zum
		mssSonarLeft    = int(msplit[3])   #The messurment of each of he three sonars
		mssSonarFront   = int(msplit[4])
		mssSonarRight   = int(msplit[5])

	if initial == True:
		prevMilis = mssMilis
		initial = False

	#Analizing the data
	if mssType == mssInfo['DATA']:             #Redundant if, use for clarity
		deltaMilis = mssMilis - prevMilis 
		spaceTraverse = deltaMilis * speed;	#x is moving forward n the origianl position, y is moving forward having turn 90

		if mssOrientation == 0:
			#rotation = 0
			x += spaceTraverse                  #in wich axis have we move
			y += 0
			if mssSonarLeft  >  0:				#Defining what is going to be shown. One posible dot for each sensor.
				d1 = dot(x, y + mssSonarLeft)
				plt.scatter(d1.x, d1.y)
				print(d1.x) #Testing use only
				print(",")  #Testing use only
				print(d1.y) #Testing use only
			if mssSonarFront >  0:
				d2 = dot(x  + mssSonarFront, y)
				plt.scatter(d2.x, d2.y)
			if mssSonarRight >  0:
				d3 = dot(x, y - msssonarRight)
				plt.scatter(d3.x, d3.y)

		if mssOrientation == 2:
			#rotation = 2
			x -= spaceTraverse
			y += 0

		if mssOrientation == 1:
			#rotation = 1
			x += 0
			y += spaceTraverse

		if mssOrientation == -1:
			#rotation = -1
			x += 0
			y -= spaceTraverse

		#Wraping up the analyzing
		prevMilis = mssMilis

		plt.draw()
		time.sleep(0.05)

	#In case we are turning.
	if mssType == mssInfo['TURN']:
		prevMilis = mssMilis    #When turning we dont want to analize data, just take into a count the time


endConnect()
time.sleep(30)