# -*- coding: utf-8 -*-
import direct.directbase.DirectStart #da el render
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import TextureStage

class World(DirectObject):
	def __init__(self, width, height, parent=pixel2d):
		self.width , self.height = width, height
		self.node = self.origin = self.parent = parent
		self.ar = parent.getScale()[0]
		base.cam2d.setZ(2)
		print "AR", self.ar
		# test some points
		#   points = [(0,0), (screenWidth, 0), (screenWidth, screenHeight), (screenWidth/2.0, screenHeight/2.0), (0, screenHeight)]
		#   for pt in points:
		#      print '%s -> %s' % (pt, str(parent.getRelativePoint(screenNode, Vec3(pt[0], 0, pt[1]))))

		#return [self.node, self.origin]
		return parent, parent

def setNode(self):
	self.origin = parent.attachNewNode('screen_origin')
	self.node = self.origin.attachNewNode('screen_node')

	self.origin.setPos(-1.0/self.ar , 0.0, 1.0)
	self.origin.setScale(2.0, 1.0, -2.0)

	self.node.setPos(0, 0, 0)

	self.node.setScale(1.0/(self.ar *width), 1.0, 1.0/height)
	self.node.setTexScale(TextureStage.getDefault(), 1.0, -1.0)

def CreateCamLayout(self):
	self.cameras = [ base.cam2dp, base.cam, base.cam2d]
	self.cam = base.cam2dp
	self.cam.node().getLens().setFilmSize(width, height)
	self.cam.setPos(240, 0, 160)

def setCam():
	base.cam2d.node().getLens().setFilmSize(width, height)
	base.cam2d.setPos(width/2.0, 1, height/2.0)
	base.cam2d.node().getLens().setAspectRatio(1.0)
	base.setTexScale(TextureStage.getDefault(), 1.0, -1.0)