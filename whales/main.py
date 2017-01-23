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
		@ irc.freenode.net/#panda3d
			ThomasEgi
			rdb
			Schwarzbaer

		StackOverflow :)

		Tileset :
			http://manuxd789.deviantart.com/art/Free-use-Underwater-Tiles-RPG-Maker-XP-477146613
		Sounds:
			http://soundbible.com/tags-whale.html
		Ship:
			http://opengameart.org/content/ships-with-ripple-effect
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

	After "Hatoful Boyfriend" heres comes the best animal love simulator ever
"""
from whales.config import VOLUME, MAX_FREQ


# TODO everything
# DONE get mic input
# DONE get fft level or something
# TODO sprites
# TODO sound for whales
# DONE whale die
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
panda2d.setUp(size[0], size[1], "Whales", False, (100, 100), txfilter=2, ani=0, keep_ar=True, wantTK=DEBUG)

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
		self.last_whale = frameTime
		self.whales.append(whales.models.Whale(self.atlas, self.node, self, wi))

	def remWhale(self, w):
		try:
			self.whales.remove(w)
		except: pass #away

	def spawnWhale(self, task):
		#cwhales = len(whales.models.WHALES)
		#i = int(tf[0] / MAX_FREQ * cwhales) % cwhales
		#print(i)
		self.addWhale()
		task.delayTime = 0.7+(rd.random()*4)
		return task.again

	def startPlaying(self):
		self.state = self.S_GAME
		if self.screen:
			self.screen.remove()
			self.screen = None
		self._tspawn = taskMgr.doMethodLater(2, self.spawnWhale, "spawnWhale")

	def lose(self):
		self.state = self.S_END
		self.ship.show()
		self.ship.go()
		for w in self.whales[:]

	def act(self, tf):
		if(self.state == self.S_INTRO):
			self.startPlaying()
		elif self.state == self.S_GAME:
			cwhales = len(whales.models.WHALES)
			i = int(tf[0] / MAX_FREQ * cwhales) % cwhales
			v = tf[1]/VOLUME
			for w in self.whales:
				w.hear(i, v)
			self.ship.hear(i, tf[1])


	def update(self, task):
		tf = mic.tell()
		self.mic.show(tf)
		#sys.stdout.write("\rFreq= %f Hz Vol= %f." % tf)
		#sys.stdout.write(".")
		if tf[1] > VOLUME:
			self.act(tf)

		return task.again

	def addSprites(self):
		self.atlas = panda2d.sprites.Atlas()
		self.atlas.loadXml("whales/data", fsprites="sps.sprites")
		self.shatlas = panda2d.sprites.Atlas("whales/data", fanim="aship.anim")
		self.tilemap = panda2d.tiles.loadTMX("whales/data", "l1.tmx", self.node)
		self.pd = 1.0/(self.tilemap.ph or 1.0)
		self.floor_y = -self.tilemap.layers['ipj'].i

		#print "pixel density", self.pd
		self.screen = whales.models.Screen(self.atlas, self.node)
		self.screen.setY(self.floor_y+1)
		self.mic = whales.models.Mic(self.atlas, self.node, self)
		self.ship = whales.models.Ship(self.shatlas, self.node, self)
		self.ship.hide()
		#self.screen.debug("Hello, please configure the volume, then do like a whale")

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
