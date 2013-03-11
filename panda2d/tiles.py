# -*- coding: utf-8 -*-
import json

from pandac.PandaModules import Vec4, Vec3, Vec2, Texture
from panda3d.core import SceneGraphAnalyzerMeter

import itertools
import panda2d.sprites

def grouper(iterable, n, fillvalue=None):
	"grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
	args = [iter(iterable)] * n
	return itertools.izip_longest(fillvalue=fillvalue, *args)

class Layer:
	def __init__(self, d, tilemap):
		for at in ('width', 'height', 'x', 'y', 'visible', 'name', 'opacity'):
			setattr(self, at, d[at])
		self.layer_type = d['type']
		self.tilemap = self.layer_type== 'tilelayer'
		self.cam = tilemap.cam
		self.parent = tilemap.parent
		if self.tilemap :
			self.loadTiles(d, tilemap)

	def loadTiles(self, d, tilemap):
		self.tiles_id = list(grouper(d['data'], self.width, 0))
		y = 0
		self.tiles = []
		# tiled orders the array so the firsts items are the one of the top, even it has +Y coords.. which makes it stupid, but visually simpler
		# i could get the map height in tiles and start counting on that and decreasing the Y, but i rather iterate the list inversely

		#create a vector of columns to allow for object culling http://www.panda3d.org/forums/viewtopic.php?p=26819#26819
		#it was easier to use rows, but rows are larger, and the movement will be more likely to be horizontal. so the culling is more efficient this way
		#(we could create groups but i dont feel like it now)
		#this is very inneficient, if we could iterate the columns instead of rows, maybe it will be more efficient
		tw = tilemap.tilewidth
		th = tilemap.tileheight
		col_width = 5
		col_real_width = tw*col_width
		x = 0
		self.texture = None
		for row_id in reversed(self.tiles_id):
			row = []
			for i, tile_id in enumerate(row_id):
				if tile_id:
					pos = Vec3(x, 3, y)
					ts = tilemap.tileSet(tile_id)
					rect = ts.tileRect(tile_id)
					if self.texture is None:
						self.texture = ts.texture
					sp = panda2d.sprites.SimpleSprite(ts.texture, pos, rect, cols[i/col_width])
					row.append(sp)
				x+= tw
			self.tiles.append(list(row))

			y += tilemap.tileheight

		self.tiles = list(self.tiles)


class TileSet():
	def __init__(self, d, dir):
		for at in ('firstgid', 'image', 'imageheight', 'imagewidth', 'margin', 'name', 'spacing',
							 'tileheight', 'tilewidth', 'transparentcolor'):
			setattr(self, at, d[at])
		self.texture = loader.loadTexture(dir+'/'+self.image)
		self.texture.setMinfilter(Texture.FTLinearMipmapLinear)
		self.texture.setMagfilter(Texture.FTLinearMipmapLinear)
		self.width = self.imagewidth / self.tilewidth
		self.height = self.imageheight / self.tileheight
		self.rects = [
			[
				Vec4(j*self.tilewidth, i*self.tileheight, self.tilewidth, self.tileheight)
				for j in range(self.width)
			]
			for i in range(self.height)
		]

	def tileRect(self, idn):
		real_id = idn - self.firstgid
		j = real_id % self.width
		i = int(real_id / self.width)
		return self.rects[i][j]

class TileMap:
	def __init__(self, dir, file, parent, cam):
		self.parent = parent
		self.cam = cam
		self.js = json.load(open(dir+'/'+file, 'r'))
		for at in ('width', 'height', 'tileheight', 'tilewidth'):
			setattr(self, at, self.js[at])

		self.tilesets = { ts['firstgid']:TileSet(ts, dir) for ts in self.js['tilesets'] }
		self.layers = [Layer(l, self) for l in self.js['layers']]


	def tileSet(self, tid):
		ids = sorted(self.tilesets.keys(),reverse = True)
		ts = None
		for k in ids:
			if tid>=k:
				ts = self.tilesets[k]
				break
		return ts

	def tileRect(self, idn):
		ts = self.tileSet(idn)
		if ts:
			return ts.tileRect(idn)
		return None