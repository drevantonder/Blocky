#!/usr/bin/env python

import pygame,random,time
from pygame.locals import *
from button import *

#Constants
WINDOWHEIGHT=800
WINDOWWIDTH=800
BLACK=[10,10,10]
WHITE=[255,255,255]
BLUE=[0,0,255]
GREEN=[50,255,50]
RED=[255,50,50]
YELLOW=[255,255,0]
WATER=[235,244,250]
LAND=[0,250,30]
FPS=28
MAP={}

class Block(pygame.sprite.Sprite):
	def __init__(self,color,x,y,width,height,Type):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([width, height])
		self.image.fill(color)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.type = Type
class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([40, 40])
		self.rect = self.image.get_rect()
		self.image.fill([0,0,255])
		self.rect.x = 400
		self.rect.y = 720
		self.in_air = False
		self.gravity = 0
	def update_position(self,direction,WINDOWHEIGHT,MAP,world_sprites,ai_sprites):
		if direction=="left":
			self.move(-40,MAP,world_sprites,ai_sprites)
		elif direction=="right":
			self.move(40,MAP,world_sprites,ai_sprites)
		elif direction=="up" and self.rect.y!=0 :
			self.jump(MAP)
			self.in_air=True
	def move(self,x,MAP,world_sprites,ai_sprites):
		try:
			if MAP[self.rect.x+x,self.rect.y] == "air":
				for block in world_sprites:
					block.rect.x -= x
				for enemy in ai_sprites:
					enemy.rect.x -= x
		except KeyError:
			pass
	def jump(self,MAP):
		try:
			if MAP[self.rect.x,self.rect.y-40] != "land" and MAP[self.rect.x,self.rect.y-80] != "land" and MAP[self.rect.x,self.rect.y+40] != "air":
				self.rect.y-=80
				self.in_air=True
			elif MAP[self.rect.x,self.rect.y-40] != "land" and MAP[self.rect.x,self.rect.y-80] == "land" and MAP[self.rect.x,self.rect.y+40] != "air":
				self.rect.y-=40
				self.in_air=True
		except KeyError:
			try:
				if MAP[self.rect.x,self.rect.y-40] != "land" and self.rect.y == 40  and MAP[self.rect.x,self.rect.y+40] != "air":
					self.rect.y-=40
					self.in_air=True
			except KeyError:
				pass	
	def fall(self):
		if self.in_air:
			self.rect.y+=40
class AI(pygame.sprite.Sprite):
	def __init__(self,color,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([40, 40])
		self.rect = self.image.get_rect()
		self.image.fill(color)
		self.rect.x = x
		self.rect.y = y
		self.in_air = False
		self.gravity = 0
	def update_position(self,direction,WINDOWHEIGHT,MAP):
		if direction=="left":
			self.move(-40,MAP)
		elif direction=="right":
			self.move(40,MAP)
		elif direction=="up" and self.rect.y!=0:
			self.jump(MAP)
			self.in_air=True
		elif direction=="stay":
			pass
	def move(self,x,MAP):
		try:
			if MAP[self.rect.x+x,self.rect.y] == "air":
				self.rect.x += x
		except KeyError:
			pass
	def jump(self,MAP):
		try:
			if MAP[self.rect.x,self.rect.y-40] != "land" and MAP[self.rect.x,self.rect.y-80] != "land" and MAP[self.rect.x,self.rect.y+40] != "air":
				self.rect.y-=80
				self.in_air=True
			elif MAP[self.rect.x,self.rect.y-40] != "land" and MAP[self.rect.x,self.rect.y-80] == "land" and MAP[self.rect.x,self.rect.y+40] != "air":
				self.rect.y-=40
				self.in_air=True
		except KeyError:
			try:
				if MAP[self.rect.x,self.rect.y-40] != "land" and self.rect.y == 40  and MAP[self.rect.x,self.rect.y+40] != "air":
					self.rect.y-=40
					self.in_air=True
			except KeyError:
				pass	
	def fall(self):
		if self.in_air:
			self.rect.y+=40
	def think(self,player,MAP):
		try:
			if random.choice(["stay","stay","stay","stay","move"]) != "stay":
				if player.rect.y < self.rect.y and  random.choice(["stay","jump"])=="jump": return "up"
				elif player.rect.y > self.rect.y:
					if player.rect.x > self.rect.x:
						if MAP[self.rect.x-40,self.rect.y] == "air": return "right"
						else: return "up"
					elif player.rect.x < self.rect.x:
						if MAP[self.rect.x+40,self.rect.y] == "air": return "left"
						else: return "up"
					else: return random.choice(["left","right","stay"])
				else: return random.choice(["left","right","stay"])
			elif random.choice(["random","stay","stay","stay"]) != "stay": return random.choice(["left","right","stay"])
			else: return "stay"
		except KeyError:
			return random.choice(["left","right","stay"])
class Map:
	def __init__(self):
		self.platform=False
	def generate_type(self,x,y):
		if x == 400 and y == 720: # for the player
			Type = "air"
		elif x == 320 and y == 400: #for the red enemy
			Type = "air"
		elif x == 0 and y == 40: #for the yellow enemy
			Type = "air"
		elif y == 760:
			Type = "land"
			self.platform = True
		elif self.platform == True:
			Type=random.choice(["land","land","land","air","land","air"])
		else:
			Type=random.choice(["land","air","air","air","air","air","air","air","air","air","air","air","air","air","land","air"])
		if Type == "land":
			self.platform = True
		else:
			self.platform = False
		return Type
def myround(x, base):
	return int(base * round(float(x)/base))
def main():
	#begin
	pygame.init()
	screen = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
	pygame.display.set_caption('Blocky!!')
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((BLACK))
	#make pygame sprite groups
	world_sprites=pygame.sprite.Group()
	other_sprites=pygame.sprite.Group()
	ai_sprites=pygame.sprite.Group()
	buttons=pygame.sprite.Group()
	#classes
	map=Map()
	player=Player()
	enemyRed=AI(RED,320,400)
	other_sprites.add(enemyRed)
	ai_sprites.add(enemyRed)
	enemyYellow=AI(YELLOW,0,40)
	other_sprites.add(enemyYellow)
	ai_sprites.add(enemyYellow)
	other_sprites.add(player)
	#generate map
	amount=40
	x=-800
	y=0
	no=0
	for i in range(0,1200):
		if no == 60:
			y+=amount
			x=-800
			no=0
		elif i==0:
			x=-800
		else:
			x+= amount
		Type = map.generate_type(x,y)
		if Type == "air":
			world_sprites.add(Block([100,100,250],x,y,amount,amount,Type))
		elif Type == "land":
			world_sprites.add(Block([100,175,50],x,y,amount,amount,Type))
		MAP[x,y] = Type
		no += 1
	#Draw screen
	screen.blit(background, (0, 0))
	world_sprites.draw(screen)
	other_sprites.draw(screen)
	pygame.display.update()
	#beginning gui
	#                   Text    ,x   ,y   ,width ,height ,color
	startButton=(Button("Start" ,400 ,340 ,80    ,40     ,GREEN))
	exitButton=(Button("Exit",400,400,80,40,RED))
	begin=False
	buttons=pygame.sprite.Group()
	buttons.add(exitButton)
	buttons.add(startButton)
	buttons.draw(screen)
	while begin==False:
		#check if a button is press
		event=pygame.event.wait()
		if event.type == pygame.QUIT:
			quit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			if startButton.pressed(pygame.mouse.get_pos()):
				begin=True
			elif exitButton.pressed(pygame.mouse.get_pos()):
				quit()
		screen.blit(background, (0, 0))
		world_sprites.draw(screen)
		other_sprites.draw(screen)
		buttons.draw(screen)
		pygame.display.update()
	buttons.remove(startButton)
	buttons.remove(exitButton)
	#game loop
	while 1:
		MAP.clear()
		for block in world_sprites:
			MAP[block.rect.x,block.rect.y]=block.type
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					screen.blit(background, (0, 0))
					resumeButton=(Button("Resume",395,280,90,40,GREEN))
					restartButton=(Button("Restart",390,340,100,40,GREEN))
					exitButton=(Button("Exit",400,400,80,40,RED))
					buttons.add(resumeButton)
					buttons.add(exitButton)
					buttons.add(restartButton)
					buttons.draw(screen)
					begin=False
					while begin==False:
						#check if a button is press
						event=pygame.event.wait()
						if event.type == pygame.QUIT:
							quit()
						if event.type == pygame.MOUSEBUTTONDOWN:
							if resumeButton.pressed(pygame.mouse.get_pos()):
								buttons.remove(resumeButton)
								buttons.remove(restartButton)
								buttons.remove(exitButton)
								begin=True
							elif restartButton.pressed(pygame.mouse.get_pos()):
								buttons.remove(resumeButton)
								buttons.remove(restartButton)
								buttons.remove(exitButton)
								begin=True
								world_sprites.empty()
								ai_sprites.empty()
								other_sprites.empty()
								map=Map()
								player=Player()
								enemyRed=AI(RED,320,400)
								other_sprites.add(enemyRed)
								ai_sprites.add(enemyRed)
								enemyYellow=AI(YELLOW,0,40)
								other_sprites.add(enemyYellow)
								ai_sprites.add(enemyYellow)
								other_sprites.add(player)
								#generate map
								amount=40
								x=-800
								y=0
								no=0
								for i in range(0,1200):
									if no == 60:
										y+=amount
										x=-800
										no=0
									elif i==0:
										x=-800
									else:
										x+= amount
									Type = map.generate_type(x,y)
									if Type == "air":
										world_sprites.add(Block([100,100,250],x,y,amount,amount,Type))
									elif Type == "land":
										world_sprites.add(Block([100,175,50],x,y,amount,amount,Type))
									MAP[x,y] = Type
									no += 1
							elif exitButton.pressed(pygame.mouse.get_pos()):
								quit()
						screen.blit(background, (0, 0))
						world_sprites.draw(screen)
						other_sprites.draw(screen)
						buttons.draw(screen)
						pygame.display.update()
				elif event.key == pygame.K_LEFT:
					direction="left"
					player.update_position(direction,WINDOWHEIGHT,MAP,world_sprites,ai_sprites)
				elif event.key == pygame.K_RIGHT:
					direction="right"
					player.update_position(direction,WINDOWHEIGHT,MAP,world_sprites,ai_sprites)
				elif event.key == pygame.K_SPACE:
					direction="up"
					player.update_position(direction,WINDOWHEIGHT,MAP,world_sprites,ai_sprites)
		#gravity
		for sprite in other_sprites:
			if sprite.rect.y+80 < WINDOWHEIGHT:
				if sprite.gravity == 35:
					sprite.gravity=0
					if sprite.in_air == True and MAP[sprite.rect.x,sprite.rect.y+40] != "land":
						sprite.fall()
				elif MAP[sprite.rect.x,sprite.rect.y+40] == "air":
					sprite.in_air = True
					sprite.gravity+=1
				if MAP[sprite.rect.x,sprite.rect.y+40] == "land":
					sprite.in_air = False
					sprite.gravity = 0
		for sprite in ai_sprites:
			if sprite.rect == player.rect:
				screen.blit(background, (0, 0))
				restartButton=(Button("Retry",400,340,80,40,GREEN))
				exitButton=(Button("Exit",400,400,80,40,RED))
				buttons.add(exitButton)
				buttons.add(restartButton)
				buttons.draw(screen)
				begin=False
				while begin==False:
					#check if a button is press
					event=pygame.event.wait()
					if event.type == pygame.QUIT:
						quit()
					if event.type == pygame.MOUSEBUTTONDOWN:
						if restartButton.pressed(pygame.mouse.get_pos()):
							buttons.remove(restartButton)
							buttons.remove(exitButton)
							begin=True
							world_sprites.empty()
							ai_sprites.empty()
							other_sprites.empty()
							map=Map()
							player=Player()
							enemyRed=AI(RED,320,400)
							other_sprites.add(enemyRed)
							ai_sprites.add(enemyRed)
							enemyYellow=AI(YELLOW,0,40)
							other_sprites.add(enemyYellow)
							ai_sprites.add(enemyYellow)
							other_sprites.add(player)
							#generate map
							amount=40
							x=-800
							y=0
							no=0
							for i in range(0,1200):
								if no == 60:
									y+=amount
									x=-800
									no=0
								elif i==0:
									x=-800
								else:
									x+= amount
								Type = map.generate_type(x,y)
								if Type == "air":
									world_sprites.add(Block([100,100,250],x,y,amount,amount,Type))
								elif Type == "land":
									world_sprites.add(Block([100,175,50],x,y,amount,amount,Type))
								MAP[x,y] = Type
								no += 1
						elif exitButton.pressed(pygame.mouse.get_pos()):
							quit()
					screen.blit(background, (0, 0))
					world_sprites.draw(screen)
					other_sprites.draw(screen)
					buttons.draw(screen)
					pygame.display.update()
			sprite.update_position(sprite.think(player,MAP),WINDOWHEIGHT,MAP)
		#draw background
		screen.blit(background, (0, 0))
		world_sprites.draw(screen)
		other_sprites.draw(screen)
		pygame.display.update()
		time.sleep(0.01 )
if __name__ == '__main__': main()
