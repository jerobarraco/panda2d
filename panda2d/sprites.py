# -*- coding: utf-8 -*-

from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import CollisionTraverser
from pandac.PandaModules import NodePath
from pandac.PandaModules import CardMaker
from pandac.PandaModules import Vec4, Vec3, Vec2
from pandac.PandaModules import TextureStage

class SimpleSprite(NodePath):
	def __init__(self, texture, pos, rect, parent = pixel2d):
		self.cm = CardMaker('spritesMaker')
		self.cm.setFrame(-0.5, 0.5, -0.5, 0.5)
		#self.cm.setHasUvs(True)
		NodePath.__init__(self, self.cm.generate())

		self.setTexture(texture, 1)
		self.setPos(pos)
		self.setScale(rect[2], 1.0, rect[3])
		ts = TextureStage.getDefault()
		tx, ty = texture.getXSize(), texture.getYSize()
		self.setTexScale(ts, rect[2]/tx, rect[3]/ty)

		ofx = rect[0]/tx
		ofy = rect[1]/ty
		self.setTexOffset(ts, ofx, -ofy)
		self.reparentTo(parent)
		self.setTransparency(True)

class SpriteDef():
	def __init__(self, lines):
		self.name = lines.pop(0)
		self.rotate = lines.pop(0) == True
		self.pos = Vec2(*map(float, lines.pop(0).split(":")[1].split(",")))
		self.size = Vec2(*map(float, lines.pop(0).split(":")[1].split(",")))
		self.rect = Vec4(self.pos[0], self.pos[1], self.size[0], self.size[1])
		self.orig = Vec2(*map(float, lines.pop(0).split(":")[1].split(",")))
		self.offset = Vec2(*map(float, lines.pop(0).split(":")[1].split(",")))
		self.index = int(lines.pop(0).split(":")[1])

class Animation():
	def __init__(self, lines):
		self.name = lines.pop(0)
		lines.pop(0) #{
		self.looping = lines.pop(0).split(":")[1].strip().lower() == "true"
		self.frames = [Frame(line) for line in lines if line.startswith("frame:")]

class Frame():
	def __init__(self, line):
		its = line.split(":")[1].split(",")
		self.name = its.pop(0).strip()
		self.delay = int(its.pop())/1000.0
		self.offset = Vec2(*map(float, its))

class Atlas():
	def __init__(self, dir, name):
		self.parse(dir, name+".sprites")
		self.parseAnims(dir+'/'+name+".animations")

	def parse(self, dir, filename):
		f = open(dir+'/'+filename, "r")
		text = f.readline().strip()
		self.texture = loader.loadTexture(dir+'/'+text)
		self.sprites = {}
		format = f.readline().strip()
		filter = f.readline().strip()
		repeat = f.readline().strip()
		lines = []
		for line in f:
			lines.append(line.strip())
			if len(lines)== 7:
				sd = SpriteDef(lines)
				self.sprites[sd.name] = sd
				lines = [] #not necessary

	def parseAnims(self, filename):
		self.anims = []
		try:
			f = open(filename, 'r')
			lines = []
			for line in f:
				line = line.strip()
				lines.append(line)
				if line == "}":
					anim = Animation(lines)
					self.anims.append(anim)
					lines = []#necessary
		except:
			print ("No animations for this spritesheet")
		pass

	def createSprite(self, spriteName, parent):
		an = AnimatedSprite(self, parent)
		#self.anims.append(Animation([spriteName, "{", "looping: false", "frame: %s,0,0,0"%spriteName, "}"]))
		#an.play(len(self.anims)-1)
		an.setFrame(Frame("frame: %s,0,0,0"%spriteName))
		return an

	def animIndex(self, name):
		for i, a in enumerate(self.anims):
			if a.name == name:
				return i
		return -1

class AnimatedSprite(NodePath):
	state = -1
	task = None
	def __init__(self, atlas, parent):
		self.atlas = atlas
		self.cm = CardMaker('spritesMaker')
		self.cm.setFrame(-0.5, 0.5, -0.5, 0.5)
		#self.cm.setHasUvs(True)
		NodePath.__init__(self, self.cm.generate())

		self.setTexture(atlas.texture, 1)
		self.tx, self.ty = atlas.texture.getXSize(), atlas.texture.getYSize()
		self.ts = TextureStage.getDefault()
		self.reparentTo(parent)
		self.setTransparency(True)

	def play(self, i):
		self.anim = self.atlas.anims[i]
		self.state = i
		self.current = 0
		if self.task :
			taskMgr.remove(self.task)
		self.task = taskMgr.doMethodLater(0, self.animate, 'animation')

	def stop(self):
		if self.task:
			taskMgr.remove(self.task)
			self.task = None

	def animate(self, task):
		frame = self.anim.frames[self.current]
		task.delayTime = frame.delay
		self.setFrame(frame)

		self.current += 1
		if self.current >= len(self.anim.frames):
			self.current = 0
			if not self.anim.looping:
				return task.done
		return task.again

	def setFrame(self, frame):
		sp = self.atlas.sprites[frame.name]
		rect = sp.rect
		self.setScale(rect[2], 1.0, rect[3])
		self.setTexScale(self.ts, rect[2]/self.tx, rect[3]/self.ty)

		ofx = rect[0]/self.tx
		ofy = rect[1]/self.ty
		self.setTexOffset(self.ts, -ofx, -ofy)

