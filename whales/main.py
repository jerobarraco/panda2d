# -*- coding: utf-8 -*-

#Copyright 2017 GPLv3
"""
	Example game made in <1 day for the global game jam 2017.
	It is rushed, hacky and not academic.
	Credits goes to :
		Tomas Gutierrez -> Graphics
		Jeronimo Barraco Marmol -> coding
		Nicholas Oliveira -> coding and awesomeness

	Thanks to:
		ThomasEgi @ irc.freenode.net/#panda3d
		StackOverflow :)
		Tileset :
			http://manuxd789.deviantart.com/art/Free-use-Underwater-Tiles-RPG-Maker-XP-477146613
		Sounds:
			http://soundbible.com/tags-whale.html
		Icons :
			Icon made by http://www.flaticon.com/authors/prosymbols from www.flaticon.com
			http://www.flaticon.com/authors/flat-icons

	Yes this is full of dirty hacks :)

	requires pyaudio
	requires numpy

	install them with pip install pyaudio and pip install numpy

	to use pip with panda (on windows) get the "get_pip.py" and run it with
	"ppython".

	Being a whale is not easy, please help protecting them http://www.internationalwhaleprotection.org

"""
from whales.config import VOLUME, MAX_FREQ


# TODO everything
# DONE get mic input
# DONE get fft level or something
# TODO sprites
# TODO sound for whales (wanna do this ryo?)
# TODO whale die
# DONE do something with the fft
# TODO do the world
# TODO do the scenes

#requires pyaudio
#requires numpy
#can require alsaaudio

import sys
DEBUG = "debug" in sys.argv
print (DEBUG)


import random as rd
rd.seed()

#from pandac.PandaModules import loadPrcFileData
from panda3d.core import TextNode
size = width, height = 640, 480

import panda2d
#Before importing the world we need to set up stuff. 
panda2d.setUp(size[0], size[1], "Whales", False, (100, 100), txfilter=1, ani=1, keep_ar=True, wantTK=DEBUG)

import panda2d.world
import panda2d.sprites
import panda2d.tiles

import whales.models

import mic

from direct.showbase.ShowBase import ShowBase

class Mundo(panda2d.world.World):
	floor_y = -1
	S_INTRO = 0
	S_GAME = 1
	S_END = 2
	state = 0
	def __init__(self):
		panda2d.world.World.__init__(self, size[0], size[1], bgColor=(100, 0, 100), debug=DEBUG)
		self.addSprites()
		"""self.pkevs =  (
			('arrow_up', self.m.up),
			('arrow_left', self.m.left),
			('arrow_right', self.m.right),
			('arrow_down', self.m.down),
		)
		self.evs = self.pkevs + tuple()
		self.setKeys()
		self._tfood = taskMgr.doMethodLater(1+(rd.random()*2), self.addFood, 'wfood')
		self.setCollissions()"""

		mic.open()
		self.whales = []

		self._tspawn = None
		self._tupdate = taskMgr.add(self.update, "main_update")# taskMgr.doMethodLater(0.0001, self.update, "update")

	last_whale = 0
	def addWhale(self, wi=-11):
		#dt = globalClock.getDt()#silly nande D is for DIfferential
		frameTime = globalClock.getFrameTime()
		if frameTime - self.last_whale < 2:
			return
		#print("new whale on the block", wi)
		self.last_whale = frameTime
		self.whales.append(whales.models.Whale(self.atlas, self.node, self, wi))

	def spawnWhale(self, task):
		#cwhales = len(whales.models.WHALES)
		#i = int(tf[0] / MAX_FREQ * cwhales) % cwhales
		#print(i)
		self.addWhale()
		task.delayTime = 0.7+(rd.random()*3)
		return task.again

	def startPlaying(self):
		self.state = self.S_GAME
		if self.screen:
			self.screen.remove()
			self.screen = None
		self._tspawn = taskMgr.doMethodLater(2, self.spawnWhale, "spawnWhale")

	def act(self, tf):
		if(self.state == self.S_INTRO):
			self.startPlaying()
		elif self.state == self.S_GAME:
			cwhales = len(whales.models.WHALES)
			i = int(tf[0] / MAX_FREQ * cwhales) % cwhales
			v = tf[1]/VOLUME
			for w in self.whales:
				w.hear(i, v)
				#sys.stdout.write(str(i))#print(i)


	def update(self, task):
		tf = mic.tell()
		self.mic.show(tf)
		#sys.stdout.write("\rFreq= %f Hz Vol= %f." % tf)
		#sys.stdout.write(".")
		if tf[1] > VOLUME:
			self.act(tf)

		return task.again

		
	def setCollissions(self):
		self.setColls(with_again=True)
		self.ctrav.addCollider(self.m.cnodep, self.ch)
		self.accept('into-CNfood', self.hColFood)
		self.accept('into-CNb', self.hColb)
		self.accept('again-CNb', self.hColb)
		return 
		
	def hColFood(self, data):
		food = data.getIntoNode().getPythonTag('owner')
		if self.m.getFood(food):
			food.removeNode()
	
	def hColb(self, data):
		b = data.getIntoNode().getPythonTag('owner')
		self.m.giveFood(b)
		
	def addFood(self, task):
		nf = m.models.Food(self.atlas, self.node)
		x, y, w, h = self.zone_food
		nfx = x+(rd.random()*w)
		nfy = y-(rd.random()*h)
		z = self.fakeZ(nfy, self.floor_y)
		nf.setPos(nfx, z, nfy)
		task.delayTime = 0.7+(rd.random()*1)
		return task.again
	
	def setKeys(self):
		for k, f in self.evs:
			self.accept(k, f, [True,])
			self.accept(k+'-up', f, [False,])
			
	def unsetPKeys(self):
		for k,f in self.pkevs:
			self.ignore(k)
			self.ignore(k+'-up')

	def died(self):
		self.unsetPKeys()
		if self._tfood:
			taskMgr.remove(self._tfood)
			self._tfood = None
		text = TextNode('node name')
		text.setText("Game Over?")
		text.setTextColor(1, 0.5, 0.5, 1)
		#text.setShadow(0.05, 0.05)
		#text.setShadowColor(0, 0, 0, 1.0)
		textNodePath = self.node.attachNewNode(text)
		textNodePath.colorScaleInterval(3, (1.0, 1.0, 1.0, 1.0), (1.0, 1.0, 1.0, 0.0)).start()
		textNodePath.setPos(10, -200, 10)
		textNodePath.setScale(70)
		for b in self.bs:
			b.onMDead(self.m)

	def addSprites(self):
		self.atlas = panda2d.sprites.Atlas()
		self.atlas.loadXml("whales/data", fsprites="sps.sprites")
		self.tilemap = panda2d.tiles.loadTMX("whales/data", "l1.tmx", self.node)
		self.pd = 1.0/(self.tilemap.ph or 1.0)
		self.floor_y = -self.tilemap.layers['ipj'].i

		#print "pixel density", self.pd
		self.screen = whales.models.Screen(self.atlas, self.node)
		self.screen.setY(self.floor_y+1)
		self.mic = whales.models.Mic(self.atlas, self.node, self)
		#self.screen.debug("Hello, please configure the volume, then do like a whale")
		return
		lob = self.tilemap.olayers['pjs']
		#self.floor_y = -lob.i
		#self.floor_y = -1
		for i, o in enumerate(lob.objs):
			pos = (o.x, -lob.i, o.y)
			if o.type == 'M':
				self.m = m.models.M(self.atlas, self.node, self)
				self.m.setPos(*pos)
				#print pos
			elif o.type == 'b':
				b = m.models.B(self.atlas, self.node, self)
				b.setPos(*pos)
				self.bs.append(b)
			elif o.type == 'zone_food':
				self.zone_food = (o.x, o.y, o.width, o.height)

	def nY(self, ny):
		return self.fakeZ(ny, self.floor_y)

def runWorld():
	if not mic.CAN :
		print(
		"""
		Sorry but you have no mic input, you must install numpy and at least
		pyAudio, or AlsaAudio (not implemented) or panda3d audio on windows (not implemented)
		or openal (not implemented and not exposed to python (you can submit a patch to panda3d))
		or implement your own using ctypes which are always fun
		"""
	)
		return "lol"
	world = Mundo()
	#lol this appears inside the debug windows anyway if DEBUG: taskMgr.popupControls() #schwarts says he has them empty too
	world.run()
	mic.die()
