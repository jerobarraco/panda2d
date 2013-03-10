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
#from direct.showbase.DirectObject import DirectObject
#import direct.directbase.DirectStart #da el render
from pandac.PandaModules import CollisionTraverser
from pandac.PandaModules import NodePath
from pandac.PandaModules import CardMaker
from pandac.PandaModules import Vec4, Vec3, Vec2
from pandac.PandaModules import TextureStage, OccluderNode, Point3
""" para saber si tenemos threads"""
from pandac.PandaModules import Thread
print "threads? ", Thread.isThreadingSupported()
from panda3d.core import SceneGraphAnalyzerMeter, MeshDrawer2D
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
		#t = taskMgr.doMethodLater(3, self.move_cam, 'animation')

		self.meter = SceneGraphAnalyzerMeter('meter', self.aspect2dp.node())
		self.meter.setupWindow(base.win)

	def move_cam(self, task):
		self.cam.setX(self.cam.getX()+20*globalClock.getDt())
		return task.done

	def addSprite(self):
		occluder = OccluderNode('my occluder')
		occluder.setVertices( Point3(0, 0, 0), Point3(320, 0, 0), Point3(320, 0, 480), Point3(0, 0, 480))
		occluder_nodepath = self.node.attachNewNode(occluder)
		self.pixel2d.setOccluder(occluder_nodepath)
		t = loader.loadTexture("data/spritesheet.png")
		"""self.tilemap = panda2d.tiles.TileMap("data/world/level1", "level.json", self.node)


		self.ss = panda2d.sprites.SimpleSprite(t, (50, 1, 50), Vec4(0, 0, 32, 32), self.node)

		self.atlas = panda2d.sprites.Atlas("data", "spritesheet")

		self.ghost = catsu.models.Ghost(self.atlas, self.node)
		#self.ghost = panda2d.sprites.AnimatedSprite(self.atlas, self.node)

		self.gato = catsu.models.Cat(self.atlas, self.node)
		self.blast = catsu.models.Blast(self.atlas, self.node)
		#LerpFunctionInterval(self.blast.setZ, 10, 0, 20)
		ofs = NodePath("offseter")
		ofs.reparentTo(self.gato)
		ofs.setPos(-1.5,0,-1.5)#this is in "cat sprite" coords... too bad.
		self.follow(ofs)

		#os = base.OnScreenDebug() #? how dows this work?
		#os.add("algo", 20)

		self.cam_node.setCullCenter(self.blast)
		"""
		self.md = MeshDrawer2D()
		self.md.setBudget(1000)
		self.md.begin()
		self.md.rectangle(1, 1, 4, 4, 0, 0,0, 0, (0.5,1,1,0))
		self.md.end()
		self.md.getRoot().reparentTo(self.node)
		self.md.getRoot().setTexture(t)
		#http://www.panda3d.org/manual/index.php/MeshDrawer

def runCatsu():
	world = Mundo()
	run()

if __name__=="__main__":
	runCatsu()