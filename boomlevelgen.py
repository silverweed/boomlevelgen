#!/usr/bin/env python
# BOOM random level generator
# silverweed91 && FiMvisibl3, 2014
# Generate a plist of BOOM levels.
#
# boomlevelgen.py
# Copyright (C) 2014 Silverweed91
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

import random
from random import randint
from sys import stderr
from sys import stdout
from math import exp
from optparse import OptionParser

def printHeader():
	print """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
 <key>LevelDescription</key>
 <array>"""

def printFooter():
	print """ </array>
</dict>
</plist>"""

def log_err(string):
	global quiet
	if not quiet:
		stderr.write(string)

class BOOMLevel:

	PLAYER1 = 'X'
	PLAYER2 = 'Y'
	BLANK = '0'
	FIXED = '1'
	BREAKABLE = '2'
	TELEPORT = '+'
	ENEMY = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
	BOSS = '*'
	COIN = '3'

	def __init__(self, level, faithfulThemes = False, faithfulEnemies = False, difficulty = 'normal'):
		self.level = level
		self.bgPatternID = 1
		self.borderID = 1
		self.breakableBlockID = 1
		self.fixedBlockID = 1
		self.time = 1
		self.wallsAlg = None
		self.symmetry = 'none'
		self.faithfulThemes = faithfulThemes
		self.faithfulEnemies = faithfulEnemies
		self.difficulty = difficulty
		self.grid = [['0' for x in range(0,15)] for y in range(0,13)]

	def setParameters(self):
		if self.faithfulThemes:
			self.bgPatternID = int(self.level / 10) + 1 
			self.borderID = int(self.level / 10) 
			self.breakableBlockID = 4*int(self.level / 10)
			self.fixedBlockID = int(self.level / 10)
			self.time = 60+randint(0,240)
		else:
			self.bgPatternID = randint(1,8)
			self.borderID = randint(0,7)
			self.breakableBlockID = 4*randint(0,7)
			self.fixedBlockID = randint(0,7)
			self.time = 60+randint(0,240)

	def probEnemy(self):
		if self.difficulty == 'easy':
			return (1/30. + (self.level)**0.3 / 40.) 
		else:
			return (1/25. + (self.level)**0.5 / 40.) 
	
	def probCoin(self):
		return 1/8.
	
	def probBreakable(self):
		if self.wallsAlg == 'regular':
			return 1/5.
		elif self.wallsAlg == 'random':
			return 1/6.
		else:
			return 1/15.

	def spawnEnemy(self):
		if self.faithfulEnemies:
			return self.ENEMY[randint(0,min(9, 2 + int(self.level / 10)))]
		else:
			return self.ENEMY[randint(0,9)]

	def spawnPlayers(self):
		px = randint(0,14)
		py = randint(0,12)
		if self.symmetry == 'axial-x' or self.symmetry == 'central':
			while py == 6:
				py = randint(0,12)
		else:
			while px == 7:
				px = randint(0,14)
		self.grid[py][px] = self.PLAYER1
		log_err("Spawned player 1 in x,y = "+str(px)+","+str(py)+"\n")

		if self.symmetry == 'axial-x':
			self.grid[12-py][px] = self.PLAYER2
			log_err("Spawned player 2 in x,y = "+str(px)+","+str(12-py)+"\n")
		elif self.symmetry == 'axial-y':
			self.grid[py][14-px] = self.PLAYER2
			log_err("Spawned player 2 in x,y = "+str(14-px)+","+str(py)+"\n")
		elif self.symmetry == 'central':
			self.grid[12-py][14-px] = self.PLAYER2
			log_err("Spawned player 2 in x,y = "+str(14-px)+","+str(12-py)+"\n")
		else:
			rand = random.random()
			if rand < 0.45 and px != 7:
				# axial symmetry
				self.grid[py][14-px] = self.PLAYER2
				log_err("Spawned player 2 in x,y = "+str(14-px)+","+str(py)+"\n")
			elif rand < 0.55 and py != 6:
				# axial symmetry (along x axis)
				self.grid[12-py][px] = self.PLAYER2
				log_err("Spawned player 2 in x,y = "+str(px)+","+str(12-py)+"\n")
			else:
				# central symmetry
				self.grid[12-py][14-px] = self.PLAYER2
				log_err("Spawned player 2 in x,y = "+str(14-px)+","+str(12-py)+"\n")

	def spawnBosses(self, numBosses):
		positions = []

		for i in range(0,numBosses):
			bx = randint(0,11)
			by = randint(0,9)

			def occupied(x,y):
				for i in range(x,x+3):
					for j in range(y,y+3):
						if self.grid[j][i] == self.PLAYER1 or self.grid[j][i] == self.PLAYER2:
							return True
				return False

			while occupied(bx,by):
				bx = randint(0,11)
				by = randint(0,9)
			
			self.grid[by][bx] = self.BOSS
			# fill 3x3 square required by this boss with P1 tokens. This ensures
			# the next spawnBosses and similar will not occupy one of these cells.
			# These placeholders will be converted to BLANK during post-processing.
			for i in range(by,by+3):
				for j in range(bx,bx+3):
					if i == by and j == bx: continue
					self.grid[i][j] = self.PLAYER1

			positions.append((bx,by))

		return positions
		

	def neighbours(self,y,x):
		if y == 0:
			if x == 0:
				down = left = -1
				up = 1 if self.grid[y+1][x] == self.FIXED else 0	
				right = 1 if self.grid[y][x+1] == self.FIXED else 0
			elif x == 14:
				down = right = -1
				up = 1 if self.grid[y+1][x] == self.FIXED else 0	
				left = 1 if self.grid[y][x-1] == self.FIXED else 0
			else:
				down = -1
				up = 1 if self.grid[y+1][x] == self.FIXED else 0	
				right = 1 if self.grid[y][x+1] == self.FIXED else 0
				left = 1 if self.grid[y][x-1] == self.FIXED else 0
		elif y == 12:
			if x == 0:
				up = left = -1
				down = 1 if self.grid[y-1][x] == self.FIXED else 0	
				right = 1 if self.grid[y][x+1] == self.FIXED else 0
			elif x == 14:
				up = right = -1
				down = 1 if self.grid[y-1][x] == self.FIXED else 0	
				left = 1 if self.grid[y][x-1] == self.FIXED else 0
			else:
				up = -1
				down = 1 if self.grid[y-1][x] == self.FIXED else 0	
				right = 1 if self.grid[y][x+1] == self.FIXED else 0
				left = 1 if self.grid[y][x-1] == self.FIXED else 0
		else:
			if x == 0:
				left = -1
				up = 1 if self.grid[y+1][x] == self.FIXED else 0	
				down = 1 if self.grid[y-1][x] == self.FIXED else 0	
				right = 1 if self.grid[y][x+1] == self.FIXED else 0
			elif x == 14:
				right = -1
				up = 1 if self.grid[y+1][x] == self.FIXED else 0	
				down = 1 if self.grid[y-1][x] == self.FIXED else 0	
				left = 1 if self.grid[y][x-1] == self.FIXED else 0
			else:
				up = 1 if self.grid[y+1][x] == self.FIXED else 0	
				down = 1 if self.grid[y-1][x] == self.FIXED else 0	
				right = 1 if self.grid[y][x+1] == self.FIXED else 0
				left = 1 if self.grid[y][x-1] == self.FIXED else 0

		return [up, right, down, left]
	
	def findRegions(self):
		tmpregions = []
		for i in range(0,13):
			for j in range(0,15):
				if self.grid[i][j] != self.FIXED:
					for region in tmpregions:
						if region.isContiguous(j,i):
							region.add(j,i)
							break
					else:
						#log_err("Non contiguous: x,y = "+str(j)+","+str(i)+"\n")
						r = Region()
						r.add(j,i)
						tmpregions.append(r)
	
		#log_err("[findRegion] TEMP: found "+str(len(tmpregions))+" regions.\n")
		regions = []
		for i in range(0,len(tmpregions)):
			for j in range(i,len(tmpregions)):
				if i != j and tmpregions[i].connectedWith(tmpregions[j]):
					#log_err("region #"+str(i)+" is connected with #"+str(j)+"\n")
					tmpregions[i].mergeWith(tmpregions[j])
					tmpregions[j].clear()

		for i in range(0,len(tmpregions)):
			if not tmpregions[i].isEmpty():
				regions.append(tmpregions[i])

		log_err("[findRegion] found "+str(len(regions))+" regions.\n")
		return regions

	def printRegions(self):
		regions = self.findRegions()
		string = "\033[;%dm"
		for i in range(0,13):
			for j in range(0,15):
				g = self.grid[i][j]
				if g == self.FIXED:
					log_err((string % 0) + self.grid[i][j] + " ")
				elif g == self.PLAYER1 or g == self.PLAYER2:
					log_err((string % 33) + self.grid[i][j] + "\033[;0m ")
				elif g == self.BREAKABLE:
					log_err((string % 35) + self.grid[i][j] + "\033[;0m ")
				elif g == self.BOSS:
					log_err((string % 36) + self.grid[i][j] + "\033[;0m ")
				else:
					color = 31
					for r in range(0,len(regions)):
						if regions[r].contains(j,i):
							log_err((string % (31+r)) + self.grid[i][j] + "\033[;0m ")
							break
					else:
						log_err(self.grid[i][j]+" ")
			log_err("\n")
	
	# given a region, cycles on the blocks surrounding its external boundaries and
	# changes the first fixed block it finds to a breakable one.
	def openBoundaries(self,region):
		upm = region.upmost()
		downm = region.downmost()
		leftm = region.leftmost()
		rightm = region.rightmost()
		if upm > 0:
			for x in range(0,15):
				if self.grid[upm-1][x] == self.FIXED:
					self.grid[upm-1][x] = self.BREAKABLE
					break
		if downm < 12:
			for x in range(0,15):
				if self.grid[downm+1][x] == self.FIXED:
					self.grid[downm+1][x] = self.BREAKABLE
					break
		if leftm > 0:
			for y in range(0,13):
				if self.grid[y][leftm-1] == self.FIXED:
					self.grid[y][leftm-1] = self.BREAKABLE
					break
		if rightm < 14:
			for y in range(0,13):
				if self.grid[y][rightm+1] == self.FIXED:
					self.grid[y][rightm+1] = self.BREAKABLE
					break
	
	# given a pair of player coordinates, ensure it's in a "safe enough" spot.
	# At the moment, doesn't take bosses into account.
	def securePlayer(self, coords):
		(px, py) = coords
		replacement = lambda: self.BLANK if random.random() < 0.8 else self.COIN
		# check the immediate surroundings and delete enemies
		for i in range(max(0, py - 1), min(13, py + 2)):
			for j in range(max(0, px - 1), min(15, px + 2)):
				if self.grid[i][j] in self.ENEMY:
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
			if self.grid[i][px] in self.ENEMY:
				nearestEnemyY = i
			elif self.grid[i][px] == self.BREAKABLE or self.grid[i][px] == self.FIXED:
				nearestWallY = i
		if dangerousUpLeft(nearestEnemyY, nearestWallY):
			self.grid[nearestEnemyY][px] = replacement()
		# Down
		nearestEnemyY = None
		nearestWallY = None
		for i in range(py + 1, min(13, py + 4)):
			if self.grid[i][px] in self.ENEMY:
				nearestEnemyY = i
			elif self.grid[i][px] == self.BREAKABLE or self.grid[i][px] == self.FIXED:
				nearestWallY = i
		if dangerousDownRight(nearestEnemyY, nearestWallY):
			self.grid[nearestEnemyY][px] = replacement()
		# Left
		nearestEnemyX = None
		nearestWallX = None
		for i in range(max(0, px - 4), px):
			if self.grid[py][i] in self.ENEMY:
				nearestEnemyX = i
			elif self.grid[py][i] == self.BREAKABLE or self.grid[py][i] == self.FIXED:
				nearestWallX = i
		if dangerousUpLeft(nearestEnemyX, nearestWallX):
			self.grid[py][nearestEnemyX] = replacement()
		# Right
		nearestEnemyX = None
		nearestWallX = None
		for i in range(px + 1, min(15, px + 4)):
			if self.grid[py][i] in self.ENEMY:
				nearestEnemyX = i
			elif self.grid[py][i] == self.BREAKABLE or self.grid[py][i] == self.FIXED:
				nearestWallX = i
		if dangerousDownRight(nearestEnemyX, nearestWallX):
			self.grid[py][nearestEnemyX] = replacement()

			
	def genWallsWithWalkers(self):
		# choose a starting point for the "random walk" that generates walls.
		# probability is higher for central squares.
		#probx = lambda n: (1/64. * min(n+1,15-n) - 1/64.) * 1./(1 - 15./64.)
		#proby = lambda n: 1/49. * min(n+1,13-n)
		probx = lambda n: 1/13. * (0 if n == 0 or n == 15 else 1)
		proby = lambda n: 1/13.
		
		def runWalker(probx,proby):
			x = y = -1
			while x == -1 or y == -1 or self.grid[y][x] == self.PLAYER1 or self.grid[y][x] == self.PLAYER2:
				rand = random.random()
				for i in range(0,15):
					if rand <= sum([probx(m) for m in range(0,i+1)]):
						x = i
						break
				else:
					raise Exception("x was not set!")

				for i in range(0,13):
					if rand <= sum([proby(m) for m in range(0,i+1)]):
						y = i
						break
				else:
					raise Exception("y was not set!")
				
				log_err("x = "+str(x)+", y = "+str(y)+"\n")

			# acknowledge if we're starting near a border; in that case, bias the
			# initial direction towards the opposite direction as the border.
			chuck = Walker(self,x,y)
			while chuck.routine():
				pass

		# populate grid with walls
		for i in range(0,10):
			runWalker(probx,proby)
	
	def genWallsRegularGrid(self):
		if self.symmetry == 'central':
			for i in range(1,6,2):
				for j in range(1,7,2):
					if self.grid[i][j] == self.BLANK:
						self.grid[i][j] = self.FIXED
					if self.grid[12-i][j] == self.BLANK:
						self.grid[12-i][j] = self.FIXED
					if self.grid[i][14-j] == self.BLANK:
						self.grid[i][14-j] = self.FIXED
					if self.grid[12-i][14-j] == self.BLANK:
						self.grid[12-i][14-j] = self.FIXED
		else:
			for i in range(1,12,2):
				for j in range(1,14,2):
					if self.grid[i][j] == self.BLANK:
						self.grid[i][j] = self.FIXED
	
	def genWallsRandom(self, density = 1/6.):
		if self.symmetry == 'axial-x':
			for i in range(0,7):
				for j in range(0,15):
					if self.grid[i][j] == self.BLANK and random.random() < density:
						self.grid[i][j] = self.FIXED
						if self.grid[12-i][j] == self.BLANK:
							self.grid[12-i][j] = self.FIXED
		elif self.symmetry == 'axial-y':
			for i in range(0,13):
				for j in range(0,8):
					if self.grid[i][j] == self.BLANK and random.random() < density:
						self.grid[i][j] = self.FIXED
						if self.grid[i][14-j] == self.BLANK:
							self.grid[i][14-j] = self.FIXED
		elif self.symmetry == 'central':
			for i in range(0,7):
				for j in range(0,15):
					if self.grid[i][j] == self.BLANK and random.random() < density:
						self.grid[i][j] = self.FIXED
						if self.grid[12-i][14-j] == self.BLANK:
							self.grid[12-i][14-j] = self.BLANK
		else:
			for i in range(0,13):
				for j in range(0,15):
					if self.grid[i][j] == self.BLANK and random.random() < density:
						self.grid[i][j] = self.FIXED

	# generic method to generate coins, breakable or enemies
	def generate(self, what):
		if what == 'coins':
			block = self.COIN
			prob = self.probCoin()
		elif what == 'breakable':
			block = self.BREAKABLE
			prob = self.probBreakable()
		elif what == 'enemies':
			prob = self.probEnemy()
		else:
			log_err("[generate()] unknown: "+what+"\n")
			return

		if self.symmetry == 'axial-x':
			for i in range(0,7):
				for j in range(0,15):
					if random.random() < prob:
						if what == 'enemies':
							block = self.spawnEnemy()
						if self.grid[i][j] == self.BLANK:
							self.grid[i][j] = block
						if self.grid[12-i][j] == self.BLANK:
							self.grid[12-i][j] = block
		elif self.symmetry == 'axial-y':
			for i in range(0,13):
				for j in range(0,8):
					if random.random() < prob:
						if what == 'enemies':
							block = self.spawnEnemy()
						if self.grid[i][j] == self.BLANK:
							self.grid[i][j] = block
						if self.grid[i][14-j] == self.BLANK:
							self.grid[i][14-j] = block
		elif self.symmetry == 'central':
			for i in range(0,7):
				for j in range(0,15):
					if random.random() < prob:
						if what == 'enemies':
							block = self.spawnEnemy()
						if self.grid[i][j] == self.BLANK:
							self.grid[i][j] = block
						if self.grid[12-i][14-j] == self.BLANK:
							self.grid[12-i][14-j] = block
		else:
			for i in range(0,13):
				for j in range(0,15):
					if random.random() < prob:
						if what == 'enemies':
							block = self.spawnEnemy()
						if self.grid[i][j] == self.BLANK:
							self.grid[i][j] = block

	def genGridDescString(self):
		# choose a symmetry
		rand = random.random()
		if rand > 0.75:
			self.symmetry = 'axial-x'
		elif rand > 0.5:
			self.symmetry = 'axial-y'
		elif rand > 0.25:
			self.symmetry = 'central'
		else:
			self.symmetry = 'none'

		# spawn players
		self.spawnPlayers()
		
		# spawn bosses if necessary
		posBosses = None
		if self.level % 10 == 0:
			posBosses = self.spawnBosses(self.level/10)
			log_err("posBosses = "+str(posBosses)+"\n")

		# populate grid with teleports (at least 2 if any)
		rand = random.random()
		numTeleport = 0
		if rand > 0.333:
			rand = random.random()
			def p(n):
				return .118519 * (19/16. - 3*n/32.)
			for i in range(2,10):
				if rand <= sum([p(n) for n in range(2,i+1)]):
					numTeleport = i
					break

		# TODO: use level symmetry
		for i in range(0, numTeleport):
			x = randint(0,14)
			y = randint(0,12)
			while self.grid[y][x] != self.BLANK:
				x = randint(0,14)
				y = randint(0,12)
			self.grid[y][x] = self.TELEPORT


		# generate walls with a randomly choosen algorithm
		rand = random.random()
		if rand > 0.4:
			self.wallsAlg = 'walkers'
			self.genWallsWithWalkers()
		elif rand > 0.1:
			self.wallsAlg = 'regular'
			self.genWallsRegularGrid()
		else:
			self.wallsAlg = 'random'
			self.genWallsRandom()

		log_err("Chosen symmetry: "+self.symmetry+"\n")
		log_err("Chosen algorithm: "+self.wallsAlg+"\n")
		
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
			for (bx,by) in posBosses:
				for i in range(by,by+3):
					for j in range(bx,bx+3):
						if i == by and j == bx: continue
						else:
							self.grid[i][j] = self.BLANK
			
		# recheck that both players exist.
		p1found = p2found = False
		p1Coords = p2Coords = (None, None)
		for i in range(0,13):
			for j in range(0,15):
				if self.grid[i][j] == self.PLAYER1:
					p1found = True
					p1Coords = (j, i)
				elif self.grid[i][j] == self.PLAYER2:
					p2found = True
					p2Coords = (j, i)
				if p1found and p2found:
					break

		if not (p1found and p2found):
			self.printLevelGrid()
		assert p1found and p2found

		# TODO: ensure players are in a safe starting place
		self.securePlayer(p1Coords)
		self.securePlayer(p2Coords)

		# (re-)check no spot is unreachable
		for i in range(0,13):
			for j in range(0,15):
				if self.grid[i][j] == self.FIXED:
					continue
				neigh =  self.neighbours(i,j)
				if not 0 in neigh:
					log_err("spot x,y="+str(j)+","+str(i)+" is unreachable!\n")
					self.printLevelGrid()
					k = randint(0,3)
					while neigh[k] != 1:
						k = randint(0,3)
					if k == 0:
						self.grid[i+1][j] = self.BREAKABLE
					elif k == 1:
						self.grid[i][j+1] = self.BREAKABLE
					elif k == 2:
						self.grid[i-1][j] = self.BREAKABLE
					elif k == 3:
						self.grid[i][j-1] = self.BREAKABLE
					log_err("Fixed:\n")
					self.printLevelGrid()
		
		# final step: convert grid to string
		string = ''
		for i in range(0,13):
			for j in range(0,15):
				string += self.grid[i][j]
		return string
		
	def genLastLevel(self):
		string = ''
		# put p1 in first line
		rand = random.randint(0,15)
		string += ''.join([self.BLANK for i in range(0, rand)]) + self.PLAYER1 + ''.join([self.BLANK for i in range(rand+1, 15)])
		# line 1 is a wall separating the Big Alien Boss from p1
		chooseWall = lambda x: self.FIXED if random.random() < x else self.BREAKABLE
		string += self.BREAKABLE*2 + ''.join([chooseWall(0.2) for i in range(0, 11)]) + self.BREAKABLE*2
		# lines 2-10 are 'reserved' for containing the Boss, so we only generate side walls
		# line 2 is fixed
		string += self.BLANK + self.BREAKABLE + self.BLANK*11 + self.BREAKABLE + self.BLANK
		# choose line where to spawn boss
		bossline = random.randint(4, 7)
		for i in range(3,10):
			middle = self.BLANK*11 if i != bossline else self.BLANK*4 + self.BOSS + self.BLANK*6
			string += (self.BLANK if random.random() < 0.6 else chooseWall(0.3)) + chooseWall(0.3) + \
				middle + chooseWall(0.3) + (self.BLANK if random.random() < 0.6 else chooseWall(0.3))
		# now, mirror 
		string += self.BLANK + self.BREAKABLE + self.BLANK*11 + self.BREAKABLE + self.BLANK
		string += self.BREAKABLE*2 + ''.join([chooseWall(0.2) for i in range(0, 11)]) + self.BREAKABLE*2
		rand = random.randint(0,15)
		string += ''.join([self.BLANK for i in range(0, rand)]) + self.PLAYER2 + ''.join([self.BLANK for i in range(rand+1, 15)])
		# fill out grid for log's sake
		for i in range(0,13):
			for j in range(0,15):
				self.grid[i][j] = string[i*15+j]
		return string

	def genLevel(self):
		self.setParameters()
		print "  <dict>"
		print "   <key>BGPatternID</key>"
		print "   <integer>"+str(self.bgPatternID)+"</integer>"
		print "   <key>BorderID</key>"
		print "   <integer>"+str(self.borderID)+"</integer>"
		print "   <key>BreakableBlockID</key>"
		print "   <integer>"+str(self.breakableBlockID)+"</integer>"
		print "   <key>FixedBlockID</key>"
		print "   <integer>"+str(self.fixedBlockID)+"</integer>"
		print "   <key>GridDescString</key>"
		if self.level == 80: # last level is special 
			print "   <string>"+self.genLastLevel()+"</string>"
		else:
			print "   <string>"+self.genGridDescString()+"</string>"
		print "   <key>Time</key>"
		print "   <integer>"+str(self.time)+"</integer>"
		print "  </dict>"

	def printLevelGrid(self):
		for i in range(0,13):
			for j in range(0,15):
				if self.grid[i][j] == self.FIXED:
					log_err("\033[;32m"+self.grid[i][j]+"\033[;0m ")
				else:
					log_err(self.grid[i][j]+' ')
			log_err("\n")
class Walker:
	def __init__(self,level,x,y):
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

	def dirtostr(self,direct):
		if direct == self.up: return 'up'
		elif direct == self.right: return 'right'
		elif direct == self.down: return 'down'
		elif direct == self.left: return 'left'
		else: return '?'

	def relativeTurn(self,direction,turn):
		return (direction + turn) % 4

	def opposite(self,direction):
		if direction == self.up: return self.down
		elif direction == self.down: return self.up
		elif direction == self.right: return self.left
		elif direction == self.left: return self.right
		else: raise Exception('direction is unset!')

	def chooseStartingDirection(self):
		if self.y == 0: return self.up
		elif self.y == 12: return self.down
		else:
			if self.x < 3:
				if self.y < 3:
					rand = randint(1,20)
					if rand == 1: return self.left
					elif rand == 2: return self.down
					elif rand < 12: return self.up
					else: return self.right
				elif self.y > 9:
					rand = randint(1,20)
					if rand == 1: return self.left
					elif rand == 2: return self.up
					elif rand < 12: return self.down
					else: return self.right
			elif self.x > 11:
				if self.y < 3:
					rand = randint(1,20)
					if rand == 1: return self.right
					elif rand == 2: return self.down
					elif rand < 12: return self.up
					else: return self.left
				elif self.y > 9:
					rand = randint(1,20)
					if rand == 1: return self.right
					elif rand == 2: return self.up
					elif rand < 12: return self.down
					else: return self.left
			else: return randint(0,3)
	
	def nextBlock(self,direction):
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
		return self.level.grid[y][x] == BOOMLevel.BLANK 
	
	def onBorder(self):
		return self.x == 0 or self.x == 14 or self.y == 0 or self.y == 12

	def move(self):
		self.x, self.y = self.nextBlock(self.direction)
		self.nStep += 1
	
	def spawnBlock(self):
		if self.level.grid[self.y][self.x] == BOOMLevel.PLAYER1 or self.level.grid[self.y][self.x] == BOOMLevel.PLAYER2:
			return
		rand = randint(1,10)
		if rand > 3:
			self.level.grid[self.y][self.x] = BOOMLevel.FIXED
			if self.level.symmetry == 'axial-x':
				if self.level.grid[12-self.y][self.x] == BOOMLevel.BLANK or self.level.grid[12-self.y][self.x] == BOOMLevel.BREAKABLE:
					self.level.grid[12-self.y][self.x] = BOOMLevel.FIXED
			elif self.level.symmetry == 'axial-y':
				if self.level.grid[self.y][14-self.x] == BOOMLevel.BLANK or self.level.grid[self.y][14-self.x] == BOOMLevel.BREAKABLE:
					self.level.grid[self.y][14-self.x] = BOOMLevel.FIXED
			elif self.level.symmetry == 'central':
				if self.level.grid[12-self.y][14-self.x] == BOOMLevel.BLANK or self.level.grid[12-self.y][14-self.x] == BOOMLevel.BREAKABLE:
					self.level.grid[12-self.y][14-self.x] = BOOMLevel.FIXED

		else:
		#elif rand > 1:
			self.level.grid[self.y][self.x] = BOOMLevel.BREAKABLE
			if self.level.symmetry == 'axial-x':
				if self.level.grid[12-self.y][self.x] == BOOMLevel.BLANK or self.level.grid[12-self.y][self.x] == BOOMLevel.FIXED:
					self.level.grid[12-self.y][self.x] = BOOMLevel.BREAKABLE
			elif self.level.symmetry == 'axial-y':
				if self.level.grid[self.y][14-self.x] == BOOMLevel.BLANK or self.level.grid[self.y][14-self.x] == BOOMLevel.FIXED:
					self.level.grid[self.y][14-self.x] = BOOMLevel.BREAKABLE
			elif self.level.symmetry == 'central':
				if self.level.grid[12-self.y][14-self.x] == BOOMLevel.BLANK or self.level.grid[12-self.y][14-self.x] == BOOMLevel.FIXED:
					self.level.grid[12-self.y][14-self.x] = BOOMLevel.BREAKABLE
		#else:
		#	pass	# leave blank

	def chooseDirection(self):		
		pStraight = (1./(1+self.nTurn))**0.43
		q = 1-exp(-2./3*self.nTurn)
		pLast = q/(1+q) * (1 - pStraight)
		
		rand = random.random()
		
		if rand < pLast: 
			self.nTurn = 0
			return self.relativeTurn(self.direction,self.lastTurn)
		elif rand > 1 - pStraight:
			self.nTurn += 1
			return self.direction
		else:
			self.nTurn = 0
			self.lastTurn = -self.lastTurn
			return self.relativeTurn(self.direction,self.lastTurn)

	# prevent newly born walkers to die too soon
	def walkOn(self):
		x, y = self.nextBlock(self.direction)
		return self.level.grid[y][x] != BOOMLevel.PLAYER1 and self.level.grid[y][x] != BOOMLevel.PLAYER2 and random.random() < 1./((1+self.nStep)**2)

	def endWalk(self):
		if randint(1,5) > 1:
			chosenblock = BOOMLevel.BREAKABLE
		else:
			chosenblock = BOOMLevel.BLANK

		self.level.grid[self.y][self.x] = chosenblock

		if self.level.symmetry == 'axis-x':
			if self.level.grid[12-self.y][self.x] == BOOMLevel.BLANK or self.level.grid[12-self.y][self.x] == BOOMLevel.FIXED:
				self.level.grid[12-self.y][self.x] = chosenblock
		elif self.level.symmetry == 'axis-y':
			if self.level.grid[self.y][14-self.x] == BOOMLevel.BLANK or self.level.grid[self.y][14-self.x] == BOOMLevel.FIXED:
				self.level.grid[self.y][14-self.x] = chosenblock
		elif self.level.symmetry == 'central':
			if self.level.grid[12-self.y][14-self.x] == BOOMLevel.BLANK or self.level.grid[12-self.y][14-self.x] == BOOMLevel.FIXED:
				self.level.grid[12-self.y][14-self.x] = chosenblock

	def routine(self):
		self.spawnBlock()
		if self.nStep > 0:
			self.direction = self.chooseDirection()

		if not self.onBorder() and (self.nextIsBlank() or self.walkOn()) :
			self.move()
			return True
		else:
			self.endWalk()	
			log_err("Walker made "+str(self.nStep)+" steps.\n")
			return False
			

class Region:
	def __init__(self):
		self.pairs = []

	def add(self,x,y):
		self.pairs.append((x,y))

	def contains(self,x,y):
		return (x,y) in self.pairs

	def isContiguous(self,x,y):
		for i,j in self.pairs:
			if x == i and (y == j-1 or y == j+1) or y == j and (x == i-1 or x == i+1):
				return True
		return False
	
	def connectedWith(self,region):
		for i,j in region.pairs:
			if self.isContiguous(i,j):
				return True
		return False
	
	def mergeWith(self,region):
		self.pairs = list(set(self.pairs + region.pairs))			
		return self
	
	def clear(self):
		self.pairs = []
	
	def isEmpty(self):
		return len(self.pairs) == 0
	
	def leftmost(self):
		leftm = 14
		for x,y in self.pairs:
			if x < leftm:
				leftm = x
		return leftm
	
	def rightmost(self):
		rightm = 0
		for x,y in self.pairs:
			if x > rightm:
				rightm = x
		return rightm

	def upmost(self):
		upm = 12
		for x,y in self.pairs:
			if y < upm:
				upm = y
		return upm
	
	def downmost(self):
		downm = 0
		for x,y in self.pairs:
			if y > downm:
				downm = y
		return downm

##### MAIN #####
# parse options
parser = OptionParser()
parser.add_option("-t", "--faithfulThemes", action="store_true", default=False, help="Use the original themes for the levels")
parser.add_option("-e", "--faithfulEnemies", action="store_true", default=False, help="Put enemies according to the original levels")
parser.add_option("-v", "--verbose", action="store_false", dest="quiet", default=True, help="Be more verbose (on the stderr)")
parser.add_option("-d", "--difficulty", default='normal', help="Difficulty (easy, normal)")
options, args = parser.parse_args()
quiet = options.quiet

printHeader()
for i in range(1,81):
	levelGen = BOOMLevel(
			level = i, 
			faithfulThemes = options.faithfulThemes, 
			faithfulEnemies = options.faithfulEnemies,
			difficulty = options.difficulty
			)
	levelGen.genLevel()
	levelGen.printRegions()
printFooter()
