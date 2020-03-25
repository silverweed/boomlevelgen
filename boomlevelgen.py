#!/usr/bin/env python3
# Copyright (C) 2017 Giacomo Parolini (silverweed)
# BOOM random level generator
# Generate a plist of BOOM levels.
#
# boomlevelgen.py
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from random import randint, random, sample
from sys import stderr, stdout
from math import exp
from optparse import OptionParser
from datetime import datetime

def printHeader():
	print("""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
 <key>LevelDescription</key>
 <array>""")


def printHeaderLifish():
  print('''{
\t"name": "Autogenerated Lifish levels",
\t"author": "boomlevelgen",
\t"difficulty": "unknown",
\t"created": "''' + str(datetime.now()) + '''",
\t"comment": "Created with boomlevelgen",
\t"tracks": [
\t\t{
\t\t\t"name": "Go For It",
\t\t\t"author": "George E. Kouba, Jr.",
\t\t\t"loop": {
\t\t\t\t"start": 0.0,
\t\t\t\t"length": 0.0
\t\t\t}
\t\t},
\t\t{
\t\t\t"name": "What Goes Around",
\t\t\t"author": "George E. Kouba, Jr.",
\t\t\t"loop": {
\t\t\t\t"start": 0.0,
\t\t\t\t"length": 0.0
\t\t\t}
\t\t},
\t\t{
\t\t\t"name": "Bomber Boy",
\t\t\t"author": "George E. Kouba, Jr.",
\t\t\t"loop": {
\t\t\t\t"start": 0.0,
\t\t\t\t"length": 0.0
\t\t\t}
\t\t},
\t\t{
\t\t\t"name": "Smoak Et",
\t\t\t"author": "George E. Kouba, Jr.",
\t\t\t"loop": {
\t\t\t\t"start": 0.0,
\t\t\t\t"length": 0.0
\t\t\t}
\t\t},
\t\t{
\t\t\t"name": "Terminate",
\t\t\t"author": "George E. Kouba, Jr.",
\t\t\t"loop": {
\t\t\t\t"start": 0.0,
\t\t\t\t"length": 0.0
\t\t\t}
\t\t},
\t\t{
\t\t\t"name": "Fused",
\t\t\t"author": "George E. Kouba, Jr.",
\t\t\t"loop": {
\t\t\t\t"start": 0.0,
\t\t\t\t"length": 0.0
\t\t\t}
\t\t},
\t\t{
\t\t\t"name": "BoomRunner",
\t\t\t"author": "George E. Kouba, Jr.",
\t\t\t"loop": {
\t\t\t\t"start": 0.0,
\t\t\t\t"length": 0.0
\t\t\t}
\t\t},
\t\t{
\t\t\t"name": "Boom Forever",
\t\t\t"author": "George E. Kouba, Jr.",
\t\t\t"loop": {
\t\t\t\t"start": 0.0,
\t\t\t\t"length": 0.0
\t\t\t}
\t\t}
\t],
\t"enemies": [
\t\t{
\t\t\t"name": "soldier",
\t\t\t"ai": 0,
\t\t\t"speed": 1.0,
\t\t\t"attack": {
\t\t\t\t"type": [
\t\t\t\t\t"simple",
\t\t\t\t\t"blocking"
\t\t\t\t],
\t\t\t\t"id": 1,
\t\t\t\t"fireRate": 1.0,
\t\t\t\t"blockTime": 180.0
\t\t\t}
\t\t},
\t\t{
\t\t\t"name": "sgt. cool",
\t\t\t"ai": 0,
\t\t\t"speed": 1.0,
\t\t\t"attack": {
\t\t\t\t"type": [
\t\t\t\t\t"simple",
\t\t\t\t\t"blocking"
\t\t\t\t],
\t\t\t\t"id": 1,
\t\t\t\t"fireRate": 1.5,
\t\t\t\t"blockTime": 180.0
\t\t\t}
\t\t},
\t\t{
\t\t\t"name": "thick lizzy",
\t\t\t"ai": 1,
\t\t\t"speed": 1.0,
\t\t\t"attack": {
\t\t\t\t"type": [
\t\t\t\t\t"simple",
\t\t\t\t\t"blocking"
\t\t\t\t],
\t\t\t\t"id": 2,
\t\t\t\t"fireRate": 1.0,
\t\t\t\t"blockTime": 200.0
\t\t\t}
\t\t},
\t\t{
\t\t\t"name": "mean-o-taur",
\t\t\t"ai": 2,
\t\t\t"speed": 2.0,
\t\t\t"attack": {
\t\t\t\t"type": [
\t\t\t\t\t"contact"
\t\t\t\t],
\t\t\t\t"contactDamage": 2,
\t\t\t\t"fireRate": 5.0
\t\t\t}
\t\t},
\t\t{
\t\t\t"name": "gunner",
\t\t\t"ai": 1,
\t\t\t"speed": 1.0,
\t\t\t"attack": {
\t\t\t\t"type": [
\t\t\t\t\t"blocking"
\t\t\t\t],
\t\t\t\t"id": 3,
\t\t\t\t"fireRate": 7.0,
\t\t\t\t"blockTime": 200.0
\t\t\t}
\t\t},
\t\t{
\t\t\t"name": "thing",
\t\t\t"ai": 3,
\t\t\t"speed": 1.0,
\t\t\t"attack": {
\t\t\t\t"type": [
\t\t\t\t\t"simple",
\t\t\t\t\t"blocking"
\t\t\t\t],
\t\t\t\t"id": 4,
\t\t\t\t"fireRate": 1.0,
\t\t\t\t"blockTime": 250.0
\t\t\t}
\t\t},
\t\t{
\t\t\t"name": "ghost",
\t\t\t"ai": 4,
\t\t\t"speed": 1.0,
\t\t\t"attack": {
\t\t\t\t"type": [
\t\t\t\t\t"contact",
\t\t\t\t\t"ranged"
\t\t\t\t],
\t\t\t\t"fireRate": 2.0
\t\t\t}
\t\t},
\t\t{
\t\t\t"name": "smoulder",
\t\t\t"ai": 3,
\t\t\t"speed": 1.0,
\t\t\t"attack": {
\t\t\t\t"type": [
\t\t\t\t\t"blocking",
\t\t\t\t\t"ranged"
\t\t\t\t],
\t\t\t\t"id": 5,
\t\t\t\t"fireRate": 4.0,
\t\t\t\t"blockTime": 260.0,
\t\t\t\t"tileRange": 4
\t\t\t}
\t\t},
\t\t{
\t\t\t"name": "skully",
\t\t\t"ai": 3,
\t\t\t"speed": 1.0,
\t\t\t"attack": {
\t\t\t\t"type": [
\t\t\t\t\t"blocking"
\t\t\t\t],
\t\t\t\t"id": 6,
\t\t\t\t"fireRate": 6.0,
\t\t\t\t"blockTime": 200.0
\t\t\t}
\t\t},
\t\t{
\t\t\t"name": "h.r. giggler",
\t\t\t"ai": 3,
\t\t\t"speed": 2.0,
\t\t\t"attack": {
\t\t\t\t"type": [
\t\t\t\t\t"simple",
\t\t\t\t\t"blocking"
\t\t\t\t],
\t\t\t\t"id": 7,
\t\t\t\t"fireRate": 0.7,
\t\t\t\t"blockTime": 650.0
\t\t\t}
\t\t}
\t],
\t"levels": [''')


def printFooter():
	print(""" </array>
</dict>
</plist>""")


def printFooterLifish():
	print("\t]\r\n}")


def log_err(string, end='\n'):
	global quiet
	if not quiet:
		stderr.write(string + end)

N_LEVELS = 80

tiles = {
	'player1': 'X',
	'player2': 'Y',
	'blank': '0',
	'fixed': '1',
	'breakable': '2',
	'teleport': '+',
	'enemy': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
	'boss': '*',
	'lifish_lastboss': '/',
	'coin': '3',
}

tilecolors = {
	'fixed': 0,
	'player1': 33,
	'player2': 33,
	'breakable': 35,
	'enemy': 34,
	'boss': 36,
}
nocol = "\033[;0m"

SYM_NONE = 0
SYM_AXIAL_X = 1
SYM_AXIAL_Y = 2
SYM_CENTRAL = 3

def color(n):
	if type(n) == int:
		return "\033[;{}m".format(n)
	else:
		return color(tilecolors[n])

class BOOMLevel:
	WIDTH = 15
	HEIGHT = 13

	def __init__(self, level, faithfulThemes = False, faithfulEnemies = False, difficulty = 'normal'):
		self.level = level
		self.bgPatternID = 1
		self.borderID = 1
		self.breakableBlockID = 1
		self.fixedBlockID = 1
		self.time = 1
		self.wallsAlg = None
		self.symmetry = SYM_NONE
		self.faithfulThemes = faithfulThemes
		self.faithfulEnemies = faithfulEnemies
		self.difficulty = difficulty
		self.grid = [['0' for x in range(BOOMLevel.WIDTH)] for y in range(BOOMLevel.HEIGHT)]

	def setParameters(self):
		if self.faithfulThemes:
			self.bgPatternID = self.level // 10 + 1
			self.borderID = self.level // 10
			self.breakableBlockID = 4 * self.level // 10
			self.fixedBlockID = self.level // 10
		else:
			self.bgPatternID = randint(1, 8)
			self.borderID = randint(0, 7)
			self.breakableBlockID = 4 * randint(0, 7)
			self.fixedBlockID = randint(0, 7)
		self.time = 60 + randint(0, 60 * (self.level // 10 + 1))

	def probEnemy(self):
		if self.difficulty == 'easy':
			return 1/30. + (self.level)**0.3 / 40.
		else:
			return 1/25. + (self.level)**0.5 / 40.
	
	def probCoin(self):
		return 1 / 8.
	
	def probBreakable(self):
		if self.wallsAlg == 'regular':
			return 1 / 5.
		elif self.wallsAlg == 'random':
			return 1 / 6.
		else:
			return 1 / BOOMLevel.WIDTH

	def spawnEnemy(self):
		enemies = tiles['enemy']
		if self.faithfulEnemies:
			return enemies[randint(0, min(len(enemies)-1, 2 + self.level // 10))]
		else:
			return enemies[randint(0, len(enemies)-1)]

	@staticmethod
	def symmetrize(px, py, sym):
		'Returns (px, py) symmetric to given (px, py) according to sym'
		return (BOOMLevel.WIDTH-1-px if sym in (SYM_AXIAL_Y, SYM_CENTRAL) else px, \
			BOOMLevel.HEIGHT-1-py if sym in (SYM_AXIAL_X, SYM_CENTRAL) else py)

	@staticmethod
	def getRangesBasedOnSym(sym):
		'Returns the ranges to iterate based on symmetry (yrange, xrange)'
		return (range(BOOMLevel.HEIGHT // 2 + 1) if sym in (SYM_AXIAL_X, SYM_CENTRAL) else range(BOOMLevel.HEIGHT), \
			range(BOOMLevel.WIDTH // 2 + 1) if sym == SYM_AXIAL_Y else range(BOOMLevel.WIDTH))


	def spawnPlayers(self):
		xs = set(range(BOOMLevel.WIDTH))
		ys = set(range(BOOMLevel.HEIGHT))
		if self.symmetry in {SYM_AXIAL_X, SYM_CENTRAL}:
			ys -= {BOOMLevel.HEIGHT // 2}
		else:
			xs -= {BOOMLevel.WIDTH // 2}
		px = sample(xs, 1)[0]
		py = sample(ys, 1)[0]
		self.grid[py][px] = tiles['player1']
		log_err("Spawned player 1 in x, y = {}, {}".format(px, py))

		if self.symmetry in (SYM_AXIAL_X, SYM_AXIAL_Y, SYM_CENTRAL):
			px, py = self.symmetrize(px, py, self.symmetry)
		else:
			rand = random()
			px, py = self.symmetrize(px, py, 

				SYM_AXIAL_Y if rand < 0.45 and px != BOOMLevel.WIDTH // 2 else
				SYM_AXIAL_X if rand < 0.55 and py != BOOMLevel.HEIGHT // 2 else
				SYM_CENTRAL)

		self.grid[py][px] = tiles['player2']
		log_err("Spawned player 2 in x, y = {}, {}".format(px, py))

	def spawnBosses(self, numBosses):
		positions = []

		for i in range(numBosses):
			bx = randint(0, BOOMLevel.WIDTH - 4)
			by = randint(0, BOOMLevel.HEIGHT - 4)

			occupied = lambda x, y: any(self.grid[j][i] in (tiles['player1'], tiles['player2']) \
							for i in range(x, x + 3) for j in range(y, y + 3))

			while occupied(bx, by):
				bx = randint(0, BOOMLevel.WIDTH - 4)
				by = randint(0, BOOMLevel.HEIGHT - 4)
			
			self.grid[by][bx] = tiles['boss']
			# fill 3x3 square required by this boss with P1 tokens. This ensures
			# the next spawnBosses and similar will not occupy one of these cells.
			# These placeholders will be converted to BLANK during post-processing.
			for i in range(by, by+3):
				for j in range(bx, bx+3):
					if i == by and j == bx: continue
					self.grid[i][j] = tiles['player1']

			positions.append((bx, by))

		return positions
		

	def neighbours(self, y, x):
		# FIXME: refactor this crap
		if y == 0:
			if x == 0:
				down = left = -1
				up = +(self.grid[y+1][x] == tiles['fixed'])
				right = +(self.grid[y][x+1] == tiles['fixed'])
			elif x == BOOMLevel.WIDTH - 1:
				down = right = -1
				up = +(self.grid[y+1][x] == tiles['fixed'])
				left = +(self.grid[y][x-1] == tiles['fixed'])
			else:
				down = -1
				up = +(self.grid[y+1][x] == tiles['fixed'])
				right = +(self.grid[y][x+1] == tiles['fixed'])
				left = +(self.grid[y][x-1] == tiles['fixed'])
		elif y == BOOMLevel.HEIGHT - 1:
			if x == 0:
				up = left = -1
				down = +(self.grid[y-1][x] == tiles['fixed'])
				right = +(self.grid[y][x+1] == tiles['fixed'])
			elif x == BOOMLevel.WIDTH - 1:
				up = right = -1
				down = +(self.grid[y-1][x] == tiles['fixed'])
				left = +(self.grid[y][x-1] == tiles['fixed'])
			else:
				up = -1
				down = +(self.grid[y-1][x] == tiles['fixed'])
				right = +(self.grid[y][x+1] == tiles['fixed'])
				left = +(self.grid[y][x-1] == tiles['fixed'])
		else:
			if x == 0:
				left = -1
				up = +(self.grid[y+1][x] == tiles['fixed'])
				down = +(self.grid[y-1][x] == tiles['fixed'])
				right = +(self.grid[y][x+1] == tiles['fixed'])
			elif x == BOOMLevel.WIDTH - 1:
				right = -1
				up = +(self.grid[y+1][x] == tiles['fixed'])
				down = +(self.grid[y-1][x] == tiles['fixed'])
				left = +(self.grid[y][x-1] == tiles['fixed'])
			else:
				up = +(self.grid[y+1][x] == tiles['fixed'])
				down = +(self.grid[y-1][x] == tiles['fixed'])
				right = +(self.grid[y][x+1] == tiles['fixed'])
				left = +(self.grid[y][x-1] == tiles['fixed'])

		return up, right, down, left

	
	def findRegions(self):
		tmpregions = []
		# Collect temporary list of regions (may count the same region several times)
		for i in range(BOOMLevel.HEIGHT):
			for j in range(BOOMLevel.WIDTH):
				if self.grid[i][j] != tiles['fixed']:
					for region in tmpregions:
						if region.isContiguous(j, i):
							region.add(j, i)
							break
					else:
						r = Region()
						r.add(j, i)
						tmpregions.append(r)
	
		# Merge connected regions
		for i in range(len(tmpregions)):
			for j in range(i, len(tmpregions)):
				if i != j and tmpregions[i].connectedWith(tmpregions[j]):
					tmpregions[i].mergeWith(tmpregions[j])
					tmpregions[j].clear()

		regions = [r for r in tmpregions if not r.isEmpty()]
		log_err("[findRegion] found {} regions.".format(len(regions)))
		return regions

	def printLevelGrid(self, coloredRegions=False):
		regions = self.findRegions()
		for i in range(BOOMLevel.HEIGHT):
			for j in range(BOOMLevel.WIDTH):
				g = self.grid[i][j]
				k = [k for k, v in tiles.items() if v == g or any(e in g for e in v)][0]
				if k in tilecolors:
					log_err("{}{}{}".format(color(k), g, nocol), end=' ')
				elif coloredRegions:
					for r in range(len(regions)):
						if regions[r].contains(j, i):
							log_err("{}{}{}".format(color(31+r), g, nocol), end=' ')
							break
					else:
						log_err(self.grid[i][j], end=' ')
				else:
					log_err(self.grid[i][j], end=' ')
			log_err(nocol)
	
	# given a region, cycles on the blocks surrounding its external boundaries and
	# changes the first fixed block it finds to a breakable one.
	def openBoundaries(self, region):
		upm = region.upmost()
		downm = region.downmost()
		leftm = region.leftmost()
		rightm = region.rightmost()
		if upm > 0:
			for x in range(BOOMLevel.WIDTH):
				if self.grid[upm-1][x] == tiles['fixed']:
					self.grid[upm-1][x] = tiles['breakable']
					break
		if downm < BOOMLevel.HEIGHT - 1:
			for x in range(BOOMLevel.WIDTH):
				if self.grid[downm+1][x] == tiles['fixed']:
					self.grid[downm+1][x] = tiles['breakable']
					break
		if leftm > 0:
			for y in range(BOOMLevel.HEIGHT):
				if self.grid[y][leftm-1] == tiles['fixed']:
					self.grid[y][leftm-1] = tiles['breakable']
					break
		if rightm < BOOMLevel.WIDTH - 1:
			for y in range(BOOMLevel.HEIGHT):
				if self.grid[y][rightm+1] == tiles['fixed']:
					self.grid[y][rightm+1] = tiles['breakable']
					break
	
	# given a pair of player coordinates, ensure it's in a "safe enough" spot.
	# At the moment, doesn't take bosses into account.
	def securePlayer(self, coords):
		px, py = coords
		replacement = lambda: tiles['blank'] if random() < 0.8 else tiles['coin']
		# check the immediate surroundings and delete enemies
		for i in range(max(0, py - 1), min(BOOMLevel.HEIGHT, py + 2)):
			for j in range(max(0, px - 1), min(BOOMLevel.WIDTH, px + 2)):
				if self.grid[i][j] in tiles['enemy']:
					self.grid[i][j] = replacement()

		# check if any enemy is too nearby in a direct line (at distance
		# <= 4 from a player with no wall in between)
		def dangerousUpLeft(enemy, wall):
			if enemy == None: return False
			if wall == None: return True
			return enemy > wall
		def dangerousDownRight(enemy, wall):
			if enemy == None: return False
			if wall == None: return True
			return enemy < wall

		# Up
		nearestEnemyY = None
		nearestWallY = None
		for i in range(max(0, py - 4), py):
			if self.grid[i][px] in tiles['enemy']:
				nearestEnemyY = i
			elif self.grid[i][px] in {tiles['breakable'], tiles['fixed']}:
				nearestWallY = i
		if dangerousUpLeft(nearestEnemyY, nearestWallY):
			self.grid[nearestEnemyY][px] = replacement()
		# Down
		nearestEnemyY = None
		nearestWallY = None
		for i in range(py + 1, min(BOOMLevel.HEIGHT, py + 4)):
			if self.grid[i][px] in tiles['enemy']:
				nearestEnemyY = i
			elif self.grid[i][px] in {tiles['breakable'], tiles['fixed']}:
				nearestWallY = i
		if dangerousDownRight(nearestEnemyY, nearestWallY):
			self.grid[nearestEnemyY][px] = replacement()
		# Left
		nearestEnemyX = None
		nearestWallX = None
		for i in range(max(0, px - 4), px):
			if self.grid[py][i] in tiles['enemy']:
				nearestEnemyX = i
			elif self.grid[py][i] in {tiles['breakable'], tiles['fixed']}:
				nearestWallX = i
		if dangerousUpLeft(nearestEnemyX, nearestWallX):
			self.grid[py][nearestEnemyX] = replacement()
		# Right
		nearestEnemyX = None
		nearestWallX = None
		for i in range(px + 1, min(BOOMLevel.WIDTH, px + 4)):
			if self.grid[py][i] in tiles['enemy']:
				nearestEnemyX = i
			elif self.grid[py][i] in {tiles['breakable'], tiles['fixed']}:
				nearestWallX = i
		if dangerousDownRight(nearestEnemyX, nearestWallX):
			self.grid[py][nearestEnemyX] = replacement()

			
	def genWallsWithWalkers(self):
		# choose a starting point for the "random walk" that generates walls.
		# probability is higher for central squares.
		#probx = lambda n: (1/64. * min(n+1, BOOMLevel.WIDTH-n) - 1/64.) * 1./(1 - BOOMLevel.WIDTH./64.)
		#proby = lambda n: 1/49. * min(n+1, BOOMLevel.HEIGHT-n)
		probx = lambda n: 1./BOOMLevel.HEIGHT * (0 if n == 0 or n == BOOMLevel.WIDTH else 1)
		proby = lambda n: 1./BOOMLevel.HEIGHT
		
		def runWalker(probx, proby):
			x = y = -1
			while x == -1 or y == -1 or self.grid[y][x] in (tiles['player1'], tiles['player2']):
				rand = random()
				for i in range(BOOMLevel.WIDTH):
					if rand <= sum(probx(m) for m in range(i+1)):
						x = i
						break
				else:
					raise Exception("x was not set!")

				for i in range(BOOMLevel.HEIGHT):
					if rand <= sum(proby(m) for m in range(i+1)):
						y = i
						break
				else:
					raise Exception("y was not set!")
				
				log_err("x = {}, y = {}".format(x, y))

			# acknowledge if we're starting near a border; in that case, bias the
			# initial direction towards the opposite direction as the border.
			chuck = Walker(self, x, y)
			while chuck.routine():
				pass

		# populate grid with walls
		for _ in range(10):
			runWalker(probx, proby)
	
	def genWallsRegularGrid(self):
		if self.symmetry == SYM_CENTRAL:
			for i in range(1, BOOMLevel.HEIGHT // 2, 2):
				for j in range(1, BOOMLevel.WIDTH // 2, 2):
					if self.grid[i][j] == tiles['blank']:
						self.grid[i][j] = tiles['fixed']
					if self.grid[BOOMLevel.HEIGHT - 1-i][j] == tiles['blank']:
						self.grid[BOOMLevel.HEIGHT - 1-i][j] = tiles['fixed']
					if self.grid[i][BOOMLevel.WIDTH - 1-j] == tiles['blank']:
						self.grid[i][BOOMLevel.WIDTH - 1-j] = tiles['fixed']
					if self.grid[BOOMLevel.HEIGHT - 1-i][BOOMLevel.WIDTH - 1-j] == tiles['blank']:
						self.grid[BOOMLevel.HEIGHT - 1-i][BOOMLevel.WIDTH - 1-j] = tiles['fixed']
		else:
			for i in range(1, BOOMLevel.HEIGHT - 1, 2):
				for j in range(1, BOOMLevel.WIDTH - 1, 2):
					if self.grid[i][j] == tiles['blank']:
						self.grid[i][j] = tiles['fixed']
	
	def genWallsRandom(self, density = None):
		if density == None:
			density = 1/BOOMLevel.HEIGHT // 2.
		ranges = self.getRangesBasedOnSym(self.symmetry)
		for i in ranges[0]:
			for j in ranges[1]:
				if self.grid[i][j] != tiles['blank'] or random() >= density:
					continue
				self.grid[i][j] = tiles['fixed']
				if self.symmetry != SYM_NONE:
					jj, ii = self.symmetrize(j, i, self.symmetry)
					if self.grid[ii][jj] == tiles['blank']:
						self.grid[ii][jj] = tiles['fixed']

	# generic method to generate coins, breakable or enemies
	def generate(self, what):
		if what == 'coins':
			block = tiles['coin']
			prob = self.probCoin()
		elif what == 'breakable':
			block = tiles['breakable']
			prob = self.probBreakable()
		elif what == 'enemies':
			prob = self.probEnemy()
		else:
			log_err("[generate()] unknown: {}".format(what))
			return

		ranges = self.getRangesBasedOnSym(self.symmetry)
		for i in ranges[0]:
			for j in ranges[1]:
				if random() >= prob:
					continue
				if what == 'enemies':
					block = self.spawnEnemy()
				if self.grid[i][j] == tiles['blank']:
					self.grid[i][j] = block
				if self.symmetry != SYM_NONE:
					jj, ii = self.symmetrize(j, i, self.symmetry)
					if self.grid[ii][jj] == tiles['blank']:
						self.grid[ii][jj] = block

	def checkUnreachable(self):
		for i in range(BOOMLevel.HEIGHT):
			for j in range(BOOMLevel.WIDTH):
				if self.grid[i][j] == tiles['fixed']:
					continue
				neigh =  self.neighbours(i, j)
				if not 0 in neigh:
					log_err("spot x, y = {}, {} is unreachable!".format(j, i))
					self.printLevelGrid()
					k = randint(0, 3)
					while neigh[k] != 1:
						k = randint(0, 3)
					if k == 0:
						self.grid[i+1][j] = tiles['breakable']
					elif k == 1:
						self.grid[i][j+1] = tiles['breakable']
					elif k == 2:
						self.grid[i-1][j] = tiles['breakable']
					elif k == 3:
						self.grid[i][j-1] = tiles['breakable']
					log_err("Fixed:\n")
					self.printLevelGrid()


	def genGridDescString(self):
		# choose a symmetry
		rand = random()
		if rand > 0.75:
			self.symmetry = SYM_AXIAL_X
		elif rand > 0.5:
			self.symmetry = SYM_AXIAL_Y
		elif rand > 0.25:
			self.symmetry = SYM_CENTRAL
		else:
			self.symmetry = SYM_NONE

		# spawn players
		self.spawnPlayers()
		
		# spawn bosses if necessary
		posBosses = None
		if self.level % 10 == 0:
			posBosses = self.spawnBosses(self.level // 10)
			log_err("posBosses = {}".format(posBosses))

		# populate grid with teleports (at least 2 if any)
		rand = random()
		numTeleport = 0
		if rand > 0.333:
			rand = random()
			p = lambda n: .118519 * (19/16. - 3*n/32.)
			for i in range(2, 10):
				if rand <= sum(p(n) for n in range(2, i+1)):
					numTeleport = i
					break

		# TODO: use level symmetry
		for i in range(numTeleport):
			x = randint(0, BOOMLevel.WIDTH - 1)
			y = randint(0, BOOMLevel.HEIGHT - 1)
			while self.grid[y][x] != tiles['blank']:
				x = randint(0, BOOMLevel.WIDTH - 1)
				y = randint(0, BOOMLevel.HEIGHT - 1)
			self.grid[y][x] = tiles['teleport']


		# generate walls with a randomly choosen algorithm
		rand = random()
		if rand > 0.4:
			self.wallsAlg = 'walkers'
			self.genWallsWithWalkers()
		elif rand > 0.1:
			self.wallsAlg = 'regular'
			self.genWallsRegularGrid()
		else:
			self.wallsAlg = 'random'
			self.genWallsRandom()

		log_err("Chosen symmetry: {}".format(self.symmetry))
		log_err("Chosen algorithm: {}".format(self.wallsAlg))
		
		# ensure all spots are reachable
		regions = self.findRegions()
		while len(regions) > 1:
			for region in regions:
				self.openBoundaries(region)
			regions = self.findRegions()

		# populate grid with enemies
		self.generate('enemies')

		# populate grid with money
		self.generate('coins')

		# populate grid with breakable walls
		self.generate('breakable')

		# POST PROCESSING: ensure level is resolvable
		# if bosses were generated, replace placeholder p1 tokens with 0's
		if posBosses:
			for bx, by in posBosses:
				for i in range(by, by+3):
					for j in range(bx, bx+3):
						if i == by and j == bx: continue
						else:
							self.grid[i][j] = tiles['blank']
			
		# recheck that both players exist.
		p1found = p2found = False
		p1Coords = p2Coords = (None, None)
		for i in range(BOOMLevel.HEIGHT):
			for j in range(BOOMLevel.WIDTH):
				if self.grid[i][j] == tiles['player1']:
					p1found = True
					p1Coords = j, i
				elif self.grid[i][j] == tiles['player2']:
					p2found = True
					p2Coords = j, i
				if p1found and p2found:
					break

		if not (p1found and p2found):
			self.printLevelGrid()
		assert p1found and p2found # make it crash

		# TODO: ensure players are in a safe starting place
		self.securePlayer(p1Coords)
		self.securePlayer(p2Coords)

		# (re-)check no spot is unreachable
		self.checkUnreachable()
		
		# final step: convert grid to string
		string = ''.join(self.grid[i][j] for i in range(BOOMLevel.HEIGHT) for j in range(BOOMLevel.WIDTH))
		return string
		
	def genLastLevel(self, lifish = False):
		string = ''
		# put p1 in first line
		rand = randint(0, BOOMLevel.WIDTH)
		string += ''.join(tiles['blank'] for i in range(rand)) + tiles['player1'] + \
				''.join(tiles['blank'] for i in range(rand+1, BOOMLevel.WIDTH))
		# line 1 is a wall separating the Big Alien Boss from p1
		chooseWall = lambda x: tiles['fixed'] if random() < x else tiles['breakable']
		string += tiles['breakable']*2 + ''.join(chooseWall(0.2) for i in range(BOOMLevel.WIDTH - 4)) + tiles['breakable']*2
		# lines 2-10 are 'reserved' for containing the Boss, so we only generate side walls
		# line 2 is fixed
		string += tiles['blank'] + tiles['breakable'] + tiles['blank']*11 + tiles['breakable'] + tiles['blank']
		# choose line where to spawn boss
		bossline = randint(4, 7)
		bosstile = tiles['boss'] if not lifish else tiles['lifish_lastboss']
		for i in range(3, 10):
			middle = tiles['blank']*11 if i != bossline else tiles['blank']*4 + bosstile + tiles['blank']*6
			string += (tiles['blank'] if random() < 0.6 else chooseWall(0.3)) + chooseWall(0.3) + \
				middle + chooseWall(0.3) + (tiles['blank'] if random() < 0.6 else chooseWall(0.3))
		# now, mirror 
		string += tiles['blank'] + tiles['breakable'] + tiles['blank']*(BOOMLevel.WIDTH - 4) + tiles['breakable'] + tiles['blank']
		string += tiles['breakable']*2 + ''.join([chooseWall(0.2) for i in range(11)]) + tiles['breakable']*2
		rand = randint(0, BOOMLevel.WIDTH)
		string += ''.join(tiles['blank'] for i in range(rand)) + tiles['player2'] + \
				''.join(tiles['blank'] for i in range(rand+1, BOOMLevel.WIDTH))
		# fill out grid for log's sake
		for i in range(BOOMLevel.HEIGHT):
			for j in range(BOOMLevel.WIDTH):
				self.grid[i][j] = string[i*BOOMLevel.WIDTH+j]
		return string

	def genLevel(self):
		self.setParameters()
		print("  <dict>")
		print("   <key>BGPatternID</key>")
		print("   <integer>{}</integer>".format(self.bgPatternID))
		print("   <key>BorderID</key>")
		print("   <integer>{}</integer>".format(self.borderID))
		print("   <key>BreakableBlockID</key>")
		print("   <integer>{}</integer>".format(self.breakableBlockID))
		print("   <key>FixedBlockID</key>")
		print("   <integer>{}</integer>".format(self.fixedBlockID))
		print("   <key>GridDescString</key>")
		print("   <string>{}</string>".format(self.genLastLevel() if self.level == N_LEVELS else self.genGridDescString()))
		print("   <key>Time</key>")
		print("   <integer>{}</integer>".format(self.time))
		print("  </dict>")

	def genLevelLifish(self):
		self.setParameters()
		print("""\t\t{""")
		print("""\t\t\t"time": {},""".format(self.time))
		print("""\t\t\t"num": {},""".format(self.level))
		print("""\t\t\t"music": {},""".format(min(8, self.level // 10 + 1)))
		print("""\t\t\t"width": {},""".format(BOOMLevel.WIDTH))
		print("""\t\t\t"height": {},""".format(BOOMLevel.HEIGHT))
		print("""\t\t\t"tileIDs": {""")
		print("""\t\t\t\t"bg": {},""".format(self.bgPatternID))
		print("""\t\t\t\t"border": {},""".format(self.borderID + 1))
		print("""\t\t\t\t"fixed": {},""".format(self.fixedBlockID + 1))
		print("""\t\t\t\t"breakable": {}""".format(self.breakableBlockID // 4 + 1))
		print("""\t\t\t},""")
		print("""\t\t\t"tilemap": "{}",""".format(self.genLastLevel(lifish=True) if self.level == N_LEVELS else self.genGridDescString()))
		print("""\t\t\t"effects": []""")
		print("""\t\t}""" + (',' if self.level < N_LEVELS else ''))

class Walker:
	def __init__(self, level, x, y):
		self.level = level
		self.x = x
		self.y = y
		self.up, self.right, self.down, self.left = 0, 1, 2, 3
		self.direction = self.chooseStartingDirection()
		self.cw, self.ccw = 1, -1
		self.lastTurn = self.cw
		self.nTurn = 1000
		self.nStep = 0
		log_err("initial direction: "+self.dirtostr(self.direction)+"\n")

	def dirtostr(self, direct):
		if direct == self.up: return 'up'
		elif direct == self.right: return 'right'
		elif direct == self.down: return 'down'
		elif direct == self.left: return 'left'
		else: return '?'

	def relativeTurn(self, direction, turn):
		return (direction + turn) % 4

	def opposite(self, direction):
		if direction == self.up: return self.down
		elif direction == self.down: return self.up
		elif direction == self.right: return self.left
		elif direction == self.left: return self.right
		else: raise Exception('direction is unset!')

	def chooseStartingDirection(self):
		if self.y == 0: return self.up
		elif self.y == BOOMLevel.HEIGHT - 1: return self.down
		else:
			if self.x < 3:
				if self.y < 3:
					rand = randint(1, 20)
					if rand == 1: return self.left
					elif rand == 2: return self.down
					elif rand < BOOMLevel.HEIGHT - 1: return self.up
					else: return self.right
				elif self.y > BOOMLevel.HEIGHT - 4:
					rand = randint(1, 20)
					if rand == 1: return self.left
					elif rand == 2: return self.up
					elif rand < BOOMLevel.HEIGHT - 1: return self.down
					else: return self.right
			elif self.x > BOOMLevel.WIDTH - 4:
				if self.y < 3:
					rand = randint(1, 20)
					if rand == 1: return self.right
					elif rand == 2: return self.down
					elif rand < BOOMLevel.HEIGHT - 1: return self.up
					else: return self.left
				elif self.y > BOOMLevel.HEIGHT - 4:
					rand = randint(1, 20)
					if rand == 1: return self.right
					elif rand == 2: return self.up
					elif rand < BOOMLevel.HEIGHT - 1: return self.down
					else: return self.left
			else: return randint(0, 3)
	
	def nextBlock(self, direction):
		if direction == self.up: 
			return self.x, self.y + 1
		elif direction == self.down:
			return self.x, self.y - 1
		elif direction == self.right:
			return self.x + 1, self.y
		elif direction == self.left:
			return self.x - 1, self.y
		else:
			raise Exception('direction is unset!')
		
	def nextIsBlank(self):
		x, y = self.nextBlock(self.direction)
		return self.level.grid[y][x] == tiles['blank'] 
	
	def onBorder(self):
		return self.x == 0 or self.x == BOOMLevel.WIDTH - 1 or self.y == 0 or self.y == BOOMLevel.HEIGHT - 1

	def move(self):
		self.x, self.y = self.nextBlock(self.direction)
		self.nStep += 1
	
	def spawnBlock(self):
		if self.level.grid[self.y][self.x] in {tiles['player1'], tiles['player2']}:
			return
		rand = randint(1, 10)
		if rand > 3:
			self.placeBlockWithSym(self.x, self.y, tiles['fixed'], {tiles['blank'], tiles['breakable']})
		else:
			self.placeBlockWithSym(self.x, self.y, tiles['breakable'], {tiles['blank'], tiles['fixed']})

	def chooseDirection(self):		
		pStraight = (1. / (1 + self.nTurn))**0.43
		q = 1 - exp(-2. * self.nTurn / 3)
		pLast = q / (1 + q) * (1 - pStraight)
		
		rand = random()
		
		if rand < pLast:
			self.nTurn = 0
			return self.relativeTurn(self.direction, self.lastTurn)
		elif rand > 1 - pStraight:
			self.nTurn += 1
			return self.direction
		else:
			self.nTurn = 0
			self.lastTurn = -self.lastTurn
			return self.relativeTurn(self.direction, self.lastTurn)

	# prevent newly born walkers to die too soon
	def walkOn(self):
		x, y = self.nextBlock(self.direction)
		return self.level.grid[y][x] != tiles['player1'] and \
			self.level.grid[y][x] != tiles['player2'] and \
			random() < 1. / (1 + self.nStep)**2

	def endWalk(self):
		self.placeBlockWithSym(self.x, self.y,
			tiles['breakable'] if randint(1, 5) > 1 else tiles['blank'],
			{tiles['fixed'], tiles['blank']})

	
	def placeBlockWithSym(self, x, y, block, filterset):
		self.level.grid[y][x] = block

		symx = BOOMLevel.WIDTH - 1 - x
		symy = BOOMLevel.HEIGHT - 1 - y

		if self.level.grid[symy][self.x] in filterset:
			if self.level.symmetry == SYM_AXIAL_X:
				self.level.grid[symy][self.x] = block
			elif self.level.symmetry == SYM_AXIAL_Y:
				self.level.grid[self.y][symx] = block
			elif self.level.symmetry == SYM_CENTRAL:
				self.level.grid[symy][symx] = block

	def routine(self):
		self.spawnBlock()
		if self.nStep > 0:
			self.direction = self.chooseDirection()

		if not self.onBorder() and (self.nextIsBlank() or self.walkOn()):
			self.move()
			return True
		else:
			self.endWalk()
			log_err("Walker made {} steps.".format(self.nStep))
			return False
			

class Region:
	def __init__(self):
		self.pairs = []

	def add(self, x, y):
		self.pairs.append((x, y))

	def contains(self, x, y):
		return (x, y) in self.pairs

	def isContiguous(self, x, y):
		return any(
			(x == i and (y == j-1 or y == j+1)) or
			(y == j and (x == i-1 or x == i+1))
			for i, j in self.pairs)
	
	def connectedWith(self, region):
		return any(self.isContiguous(i, j) for i, j in region.pairs)
	
	def mergeWith(self, region):
		self.pairs = list(set(self.pairs + region.pairs))
	
	def clear(self):
		self.pairs = []
	
	def isEmpty(self):
		return len(self.pairs) == 0
	
	def leftmost(self):
		return min(BOOMLevel.WIDTH - 1, min(self.pairs, key=lambda p: p[0])[0])
	
	def rightmost(self):
		return max(0, max(self.pairs, key=lambda p: p[0])[0])

	def upmost(self):
		return min(BOOMLevel.HEIGHT - 1, min(self.pairs, key=lambda p: p[1])[1])
	
	def downmost(self):
		return max(0, max(self.pairs, key=lambda p: p[1])[1])


if __name__ == '__main__':
	# parse options
	parser = OptionParser()
	parser.add_option("-t", "--faithfulThemes", action="store_true", default=False, help="Use the original themes for the levels")
	parser.add_option("-e", "--faithfulEnemies", action="store_true", default=False, help="Put enemies according to the original levels")
	parser.add_option("-v", "--verbose", action="store_false", dest="quiet", default=True, help="Be more verbose (on the stderr)")
	parser.add_option("-d", "--difficulty", default='normal', help="Difficulty (easy, normal)")
	parser.add_option("-l", "--lifish", action="store_true", default=False, help="Emit levels in Lifish format (required for BOOM: Remake)")
	options, args = parser.parse_args()
	quiet = options.quiet

	if options.lifish:
		printHeaderLifish()
		for i in range(1, N_LEVELS + 1):
			levelGen = BOOMLevel(
					level = i, 
					faithfulThemes = options.faithfulThemes, 
					faithfulEnemies = options.faithfulEnemies,
					difficulty = options.difficulty
					)
			levelGen.genLevelLifish()
			levelGen.printLevelGrid(coloredRegions=True)
		printFooterLifish()
	else:
		printHeader()
		for i in range(1, N_LEVELS + 1):
			levelGen = BOOMLevel(
					level = i, 
					faithfulThemes = options.faithfulThemes, 
					faithfulEnemies = options.faithfulEnemies,
					difficulty = options.difficulty
					)
			levelGen.genLevel()
			levelGen.printLevelGrid(coloredRegions=True)
		printFooter()
