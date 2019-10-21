import math
import random
import lightpack
import ConfigParser as configparser
import os
import threading
import time
lits = [0, 4, 8, 13, 17, 21, 25, 30, 34, 38, 42, 47, 51, 55, 59, 64, 68, 72, 76,81, 85, 89, 93, 98, 102, 106, 110, 115, 119, 123, 127, 132, 136, 140, 144,149, 153, 157, 161, 166, 170, 174, 178, 183, 187, 191, 195, 200, 204, 208,212, 217, 221, 225, 229, 234, 238, 242, 246, 251, 255]
#miami colors
miamicolors=[[0, 0, 153],[70,0,70],[102, 0, 102],[200,200,200],[11,211,211]]
pittcolors=[[0,20,148],[255,184,28]]
alert=[[255,0,0],[0,0,0],[0,0,0],[255,0,0],[0,0,0],[0,0,0],[255,0,0],[0,0,0],[0,0,0]]
rainbow=[]
for k in range(0,359):
    if (k%5==0):
        if k < 60:
            rainbow.append([255,lits[k],0])
        elif k<120:
            rainbow.append([lits[120-k],255,0])
        elif k<180:
            rainbow.append([0,255,lits[k-120]])
        elif k<240:
            rainbow.append([0,lits[240-k],255])
        elif k<300:
            rainbow.append([lits[k-240],0,255])
        else:
            rainbow.append([255,0,lits[360-k]])
for k in range(0,359):
    if (k%5==0):
        if k < 60:
            rainbow.append([255,lits[k],0])
        elif k<120:
            rainbow.append([lits[120-k],255,0])
        elif k<180:
            rainbow.append([0,255,lits[k-120]])
        elif k<240:
            rainbow.append([0,lits[240-k],255])
        elif k<300:
            rainbow.append([lits[k-240],0,255])
        else:
            rainbow.append([255,0,lits[360-k]])
strobe=[[0,0,0],[255,255,255]]
cus = [[0,0,0]]

colors=[miamicolors,pittcolors,alert,rainbow]
colorsname = ['Maimi','Pitt','Alert','Custom','rainbow']
class Animate:
    
    def __init__(self):
        self.loadConfig()
        self.ConnectToLightpack()
        self.getLedMap()
        self.getCylonMap()
        
        self.animFunctions = {
            1: self.Animation1,
            2: self.Animation2,
            3: self.SnakeAnimation,
            4: self.CylonAnimation,
            5: self.MiamiAnimation,
            6: self.strobe
        }
        self.i = 0 #init animation index
        random.seed()
        print ('init')
        
    def loadConfig(self):
        self.scriptDir = os.path.dirname(os.path.abspath(__file__))
        self.config = configparser.ConfigParser()
        self.config.read(self.scriptDir + '/Animate.ini')
        self.animType = int(input('Animation Number: '))
        if self.animType == 5:
            print(colorsname)
            self.colorP = int(input('Pallete Number: '))
            if self.colorP==4:
                r = int(input('Red Value: '))
                g = int(input('Green Value: '))
                b = int(input('Blue Value: '))
                cus[0]=[r,g,b]
        elif self.animType ==6:
        	self.strobeS = int(input ('Strobe speed: '))
        #self.animType = self.config.getint('Animation', 'type')
        
        
    def ConnectToLightpack(self):
        try:
            self.host = self.config.get('Lightpack', 'host')
            self.port = self.config.getint('Lightpack', 'port')
            self.lpack = lightpack.lightpack(self.host, self.port)
            self.lpack.connect()
            return True
        except: return False

    def dispose(self):
        self.timeranim.stop()
        del self.timeranim
        self.lpack.unlock()

    def run(self):
        if self.lpack.lock() :
            self.lpack.turnOn()
            self.onAnimationChange()
            while True:
                self.animFunctions[self.animType]()
                time.sleep(self.animInterval)
            print ('run')
        
    def stop(self):
        self.timeranim.stop()
        self.lpack.unlock()
        
    def getCylonMap(self):
        try:
            map = self.config.get('Lightpack', 'cylonmap')
            ledGroups = [group.strip() for group in map.split(';')]
            self.cylonMap = []
            for group in ledGroups:
                self.cylonMap.append([int(n) for n in group.split(',')])
        except configparser.NoOptionError:
            self.cylonMap = [ [1,2,3], [4,5], [6,7], [8,9,10] ]
        
    def getLedMap(self):
        try:
            map = self.config.get('Lightpack', 'ledmap')
            self.ledMap = [int(n) for n in map.split(',')]
        except configparser.NoOptionError:
            self.ledMap = self.defaultMap()

    def defaultMap(self):
        try:
            leds = self.lpack.getCountLeds()
            map = [n for n in range (1, leds+1)]
        except Exception as e:
            print(str(e))
            map = [1,2,3,4,5,6,7,8,9,10]
        return map

    def Animation1(self):
        try:
            self.i = self.i+1
            leds = self.lpack.getCountLeds()
            for k  in range (0, leds):
                t = float(self.i/4 - k*2)/10
                r = int((math.sin(t)+1)*127)
                g = int((math.cos(t*0.7)+1)*127)
                b = int((math.cos(1.3 + t*0.9)+1)*127)
                self.lastFrame[self.ledMap[k]-1]=[r,g,b]
            self.lpack.setFrame(self.lastFrame)
            self.i += 1
        except Exception as e:
            print(str(e))

    def Animation2(self):
        try:
            self.i = self.i+1
            self.lastFrame
            newFrame = self.lastFrame
            leds = self.ledsCount
            att = 0.95
            for k  in range (0, leds):
                if random.randrange(100) < 10 :
                    r = random.randrange(255)
                    g = random.randrange(255)
                    b = random.randrange(255)
                else :
                    r = int(newFrame[k][0] * att)
                    g = int(newFrame[k][1] * att)
                    b = int(newFrame[k][2] * att)

                newFrame[k] = [r,g,b]
            self.lpack.setFrame(newFrame)
            self.lastFrame = newFrame
            self.i += 1
        except Exception as e:
            print(str(e))

    def SnakeAnimation(self):
        for k in range (0, self.ledsCount) :    
            idx = (self.i+k) % self.ledsCount
            if k < 3 :
                self.lastFrame[self.ledMap[idx]-1]=[255,0,0]
            else :
                self.lastFrame[self.ledMap[idx]-1]=[0,0,125]
        self.lpack.setFrame(self.lastFrame)
        self.i += 1

    def CylonAnimation(self):
        for k in self.cylonMap: 
            idx = self.cylonMap.index(k)
            cyclePhase = self.i % self.cylonCycleLength 
            if (cyclePhase > self.cylonWidth-1 and idx == 2*(self.cylonWidth-1) - cyclePhase) or (idx == cyclePhase):
                for i in k:
                    self.lastFrame[i-1]=[255,0,0]
            else:
                for i in k:
                    self.lastFrame[i-1]=[0,0,0]
        self.lpack.setFrame(self.lastFrame)
        self.i += 1
    def MiamiAnimation(self):
        numC=len(colors[self.colorP])
        for k in range (0, self.ledsCount) :    
            idx = (self.i+k) % self.ledsCount
            cRange= self.ledsCount/numC
            for j in range(0,numC) :
                if (k/cRange)==j :
                    self.lastFrame[self.ledMap[idx]-1]=colors[self.colorP][j]
        self.lpack.setFrame(self.lastFrame)
        self.i += 1
    def strobe(self):
        for k in range (0, self.ledsCount) :
            idx = (self.i+k) % self.ledsCount
            if (self.i % 2) == 0:
                self.lastFrame[self.ledMap[idx]-1]=[0,0,0]
            else:
                self.lastFrame[self.ledMap[idx]-1]=[255,255,255]
        self.lpack.setFrame(self.lastFrame)
        self.i += 1

    def onAnimationChange(self):
        self.ledsCount = int(self.lpack.getCountLeds())
        self.lastFrame=[ [0,0,0] for k in range(0, self.ledsCount)]
        if self.animType == 1: #Animation1
            self.animInterval = 0.025
            self.i=self.ledsCount*2 + random.randrange(20000)

        elif self.animType == 2: #Animation2
            self.animInterval = 0.2

        elif self.animType == 3: #SnakeAnimation
            self.animInterval = 0.07
        elif self.animType == 5: #SnakeAnimation
            self.animInterval = 0.05
        elif self.animType == 6: #SnakeAnimation
            self.animInterval = self.strobeS
        elif self.animType == 4: #CylonAnimation
            self.animInterval = 0.2
            self.cylonWidth = len(self.cylonMap)
            self.cylonCycleLength = self.cylonWidth*2 - 2
        """ default function """

animate = Animate()
animate.run()
