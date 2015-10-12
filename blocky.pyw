buttons.remove(resumeButton)
								buttons.remove(restartButton)
								buttons.remove(exitButton)
								begin=True
								#reset game
								score=0
								world_sprites.empty()
								ai_sprites.empty()
								other_sprites.empty()
								coin_sprites.empty()
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
								#position coins 
								for block in world_sprites:
									try:
										if block.type == "land" and MAP[block.rect.x,block.rect.y-40] != "land" and random.choice(["coin","air","air"]) == "coin":
											coin = Coin(block.rect.x,block.rect.y-40)
											coin_sprites.add(coin)
									except KeyError:
										pass
