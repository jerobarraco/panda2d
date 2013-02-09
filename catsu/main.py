# -*- coding: utf-8 -*-
#Set window size
#important to be first
from pandac.PandaModules import loadPrcFileData
size = width, height = 480, 320
loadPrcFileData("", "window-title Catsu on Japan Panda's version")
loadPrcFileData("", "fullscreen 0") # Set to 1 for fullscreen 
loadPrcFileData("", "win-size %s %s" % (width, height)) 
loadPrcFileData("", "win-origin 10 10")
loadPrcFileData("", "textures-power-2 pad")#makes panda pad non-p2-sizes instead of downscaling

from panda3d.core import ConfigVariableString
#Lazy Load
ConfigVariableString('preload-textures', '0')
ConfigVariableString('preload-simple-textures', '1')
ConfigVariableString('texture-compression', '1')
ConfigVariableString('allow-incomplete-render', '1' )
from direct.showbase.DirectObject import DirectObject
import direct.directbase.DirectStart #da el render
from pandac.PandaModules import CollisionTraverser
from pandac.PandaModules import NodePath
from pandac.PandaModules import CardMaker
from pandac.PandaModules import Vec4, Vec3, Vec2
from pandac.PandaModules import TextureStage
""" para saber si tenemos threads"""
from pandac.PandaModules import Thread
print "threads? ", Thread.isThreadingSupported()

import panda2d
import panda2d.sprites
import panda2d.tiles
import catsu.models

class Mundo(panda2d.World):
	def __init__(self):
		panda2d.World.__init__(self, size[0], size[1])
		base.setBackgroundColor(100, 0, 0)        #Set the background color
		base.setFrameRateMeter(True)
		self.addSprite()
		t = taskMgr.doMethodLater(0, self.cam, 'animation')

	def cam(self, task):
		return task.done

	def addSprite(self):
		t = loader.loadTexture("data/spritesheet.png")
		self.ss = panda2d.sprites.SimpleSprite(t, (50, 1, 50), Vec4(0, 0, 32, 32), self.node)

		self.atlas = panda2d.sprites.Atlas("data", "spritesheet")

		#self.ghost = catsu.models.Ghost(self.atlas, self.node)
		self.ghost = panda2d.sprites.AnimatedSprite(self.atlas, self.node)
		f = self.atlas.anims[self.atlas.animIndex("cat_walking")].frames[0]
		print f
		self.ghost.setFrame(f)
		self.ghost.setPos(50, 1, 150)
		#self.gato = catsu.models.Cat(self.atlas, self.node)
		#self.blast = catsu.models.Blast(self.atlas, self.node)
		#self.tilemap = panda2d.tiles.TileMap("data/world/level1", "level.json", self.node)


def runCatsu():
	world = Mundo()
	run()

if __name__=="__main__":
	runCatsu()