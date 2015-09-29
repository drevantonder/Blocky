import pygame,random,time

#Constants
WINDOWHEIGHT=800
WINDOWWIDTH=800
BLACK=[10,10,10]
WHITE=[255,255,255]
BLUE=[0,0,255]
GREEN=[0,255,0]
RED=[255,0,0]
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
		self.in_air=False
	def update_position(self,direction,WINDOWHEIGHT,MAP,world_sprites):
		if direction=="left":
			self.move(-40,MAP,world_sprites)
		elif direction=="right":
			self.move(40,MAP,world_sprites)
		elif direction=="up" and self.rect.y!=0 :
			self.jump(MAP)
			self.in_air=True
	def player_position(self):
		pos={}
		pos['x']=self.rect.x
		pos['y']=self.rect.y
		return pos
	def move(self,x,MAP,world_sprites):
		try:
			if MAP[self.rect.x+x,self.rect.y] == "air":
				for block in world_sprites:
					block.rect.x -= x
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
class Map:
	def __init__(self):
		self.platform=False
	def generate_type(self,x,y):
		if x == 400 and y == 720: # for the player
			Type = "air"
		elif y == 760:
			Type = "land"
			self.platform = True
		elif self.platform == True:
			Type=random.choice(["land","land","land","air","land","air"])
		else:
			Type=random.choice(["land","air","air","air","air","air","air","air","air","air","air","air","air","air"])
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
	gravity=0
	#make pygame sprite groups
	world_sprites=pygame.sprite.Group()
	other_sprites=pygame.sprite.Group()
	power_up_sprites=pygame.sprite.Group()
	
	#classes
	map=Map()
	player=Player()
	
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
	power_up_sprites.draw(screen)
	other_sprites.draw(screen)
	pygame.display.update()
	
	#game loop
	while 1:
		MAP.clear()
		for block in world_sprites:
			MAP[block.rect.x,block.rect.y]=block.type
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					direction="left"
					player.update_position(direction,WINDOWHEIGHT,MAP,world_sprites)
				elif event.key == pygame.K_RIGHT:
					direction="right"
					player.update_position(direction,WINDOWHEIGHT,MAP,world_sprites)
				elif event.key == pygame.K_SPACE:
					direction="up"
					player.update_position(direction,WINDOWHEIGHT,MAP,world_sprites)
		
		#gravity
		if player.rect.y+80 < WINDOWHEIGHT:
			if gravity == 35:
				gravity=0
				if player.in_air == True and MAP[player.rect.x,player.rect.y+40] != "land":
					player.fall()
			elif MAP[player.rect.x,player.rect.y+40] == "air":
				player.in_air = True
				gravity+=1
			if MAP [player.rect.x,player.rect.y+40] == "land":
				player.in_air = False
				gravity = 0
		#draw background
		screen.blit(background, (0, 0))
		world_sprites.draw(screen)
		power_up_sprites.draw(screen)
		other_sprites.draw(screen)
		pygame.display.update()
		time.sleep(0.01 )
if __name__ == '__main__': main()
