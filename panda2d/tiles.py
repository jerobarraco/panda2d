# -*- coding: utf-8 -*-
import json

from pandac.PandaModules import Vec4, Vec3, Vec2

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
		if self.tilemap :
			self.loadTiles(d, tilemap)

	def loadTiles(self, d, tilemap):
		self.tiles_id = list(grouper(d['data'], self.width, 0))
		y = 0
		self.tiles = []
		for row_id in self.tiles_id:
			row = []
			x = 0
			for tile_id in row_id:
				if tile_id:
					pos = Vec3(x, -3, y)
					ts = tilemap.tileSet(tile_id)
					rect = ts.tileRect(tile_id)
					sp = panda2d.sprites.SimpleSprite(ts.texture, pos, rect, tilemap.parent)
					row.append(sp)
				x+= tilemap.tilewidth
			self.tiles.append(list(row))
			y += tilemap.tileheight

class TileSet():
	def __init__(self, d, dir):
		for at in ('firstgid', 'image', 'imageheight', 'imagewidth', 'margin', 'name', 'spacing',
							 'tileheight', 'tilewidth', 'transparentcolor'):
			setattr(self, at, d[at])
		self.texture = loader.loadTexture(dir+'/'+self.image)
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
	def __init__(self, dir, file, parent):
		self.parent = parent
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
		ts = tileSet(idn)
		if ts:
			return ts.tileRect(idn)
		return None