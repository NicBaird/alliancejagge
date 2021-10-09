import pygame, os, random, math
from states.state import State
from pathing import astar


class Battle(State):
	def __init__(self, game_world, squad_1, squad_2):
		self.squad_1 = squad_1
		self.squad_2 = squad_2
		self.game_world = game_world
		State.__init__(self, game_world.game)
		self.soldiers = []
		self.bullets = []
		self.font = self.game_world.game.h1_bold_font
		self.width = self.game_world.game.GAME_W
		self.height = self.game_world.game.GAME_H
		print("Size of screen: "+str(int(self.width/10))+", "+str(int(self.height/10)))
		self.map = [[]]
		self.buildings = []
		self.structures_img = pygame.sprite.Group()
		
		self.setup()


	def setup(self):
		#Load Map
		self.map = [[0 for y in range(0, int(self.height/10))] for x in range(0, int(self.width/10))]
		
		#Create 3 Rectangles of random sizes
		num = random.randint(0, 3)
		buildings = []
		for b in range(0, num):
			width = random.randint(10, 30)
			height = random.randint(10, 30)
			x_coord = random.randint(6, 56-width)
			y_coord = random.randint(0, 46)
			building = pygame.Rect(x_coord*10, y_coord*10, width*10, height*10)
			buildings.append(Building(building))
			for x in range(0, len(self.map)):
				if x_coord<x<(x_coord+width):
					for y in range(0, len(self.map[x])):
						if y_coord<y<(y_coord+height):
							if self.map[x][y]==0:
								self.map[x][y]=1
		for x in range(0, len(self.map)):
				for y in range(0, len(self.map[x])):
					if self.map[x][y]==1:
						tile = None
						t = False
						b = False
						l = False
						r = False
						if y!=len(self.map[x])-1:
							if self.map[x][y+1]==1:
								b = True
						else:
							b = True
						if y!=0:
							if self.map[x][y-1]==1:
								t = True
						else:
							t = True
						if x!=len(self.map)-1:
							if self.map[x+1][y]==1:
								r = True
						else:
								r = True
						if x!=0:
							if self.map[x-1][y]==1:
								l = True
						else:
								l = True
								
								print("r")
						if b and l and not t and not r:
							tile = "bottom-left"
						if b and r and not t and not l:
							tile = "bottom-right"
						if t and l and not b and not r:
							tile = "top-left"
						if t and r and not b and not l:
							tile = "top-right"
						if l and t and r and not b:
							tile = "bottom"
						if t and r and b and not l:
							tile = "left"
						if l and t and b and not r:
							tile = "right"
						if l and b and r and not t:
							tile = "top"
						if t and l and b and r:
							tile = "middle"
						if self.structures_img == None:
							self.structures_img.add(Block(x*10, y*10+10, self.game_world.building_tile_img[tile]))
						else:
							self.structures_img.add(Block(x*10, y*10+10, self.game_world.building_tile_img[tile]))
		for x in range(0, len(self.map)):
			for y in range(0, len(self.map[x])):
				if x==0:
					self.map[x][y] = 0
				if y==0:
					self.map[x][y] = 0
				if x==len(self.map)-1:
					self.map[x][y] = 0
				if y==len(self.map[x])-1:
					self.map[x][y] = 0
		
		self.buildings = buildings
		num = 0
		for column in self.map:
			print(str(num)+" : "+str(column))
			num += 1

		#check conditions for battle
		if (self.squad_1.x, self.squad_1.y) != (self.squad_2.x, self.squad_2.y):
			print("Squads are not in the same location to battle.")
			self.exit_state()
		self.quadrant = self.game_world.quadrants[self.squad_1.x][self.squad_1.y]
		self.battle_details_box = [self.font.render(self.squad_1.name, False, (135,151,255)), self.font.render(" engaging ", False, (0,0,0)), self.font.render(self.squad_2.name, False, (255,135,135)), self.font.render(" in ("+str(self.quadrant.x)+", "+str(self.quadrant.y)+").", False, (0,0,0))]
		for s in self.squad_1.soldiers:
			s.battle = BattleSoldier(s, 1, self.game_world.soldier_battle_img["01"], self)
			s.battle.SetPos()
			s.battle.WalkReset()
			self.soldiers.append(s)
		for s in self.squad_2.soldiers:
			s.battle = BattleSoldier(s, 2, self.game_world.soldier_battle_img["02"], self)
			s.battle.SetPos()
			s.battle.WalkReset()
			self.soldiers.append(s)

	def draw_background(self, display):
		display.blit(self.game_world.battlefield_img, (0,0))
		
	def draw_battle_details_box(self, display):
		prev_rect = pygame.Rect(15, 15, 10, 10)
		for e in self.battle_details_box:
			text_rect = e.get_rect()
			text_rect.x = prev_rect.x+prev_rect.width
			text_rect.y = prev_rect.y
			prev_rect = text_rect
			display.blit(e, text_rect)


	def update(self, delta_time, actions, mouse):
		for s in self.soldiers:
			if s not in self.squad_1.soldiers and s not in self.squad_2.soldiers:
				if s.battle.player == 1:
					self.squad_1.soldiers.append(s)
				if s.battle.player == 2:
					self.squad_2.soldiers.append(s)
				
				
			s.battle.update(delta_time)
			

		
		
		for b in self.bullets:
			b.update(delta_time)
			for s in self.soldiers:
				if b.rect.colliderect(s.battle.rect):
					if b.squad != s.battle.player:
						if b in self.bullets:
							self.bullets.remove(b)
						s.hp -= 1
					#	if s.battle.player == 1:
					#		self.squad_1.soldiers.remove(s)
					#	if s.battle.player == 2:
					#		self.squad_2.soldiers.remove(s)
		
		soldiers_to_remove = [s for s in self.soldiers if s.hp <=0]
		for s in soldiers_to_remove:
			self.soldiers.remove(s)
			if s.battle.player == 1:
				self.squad_1.soldiers.remove(s)
			if s.battle.player == 2:
				self.squad_2.soldiers.remove(s)
		

		if self.squad_1.soldiers == [] or self.squad_2.soldiers == []:
			print("Game Over!")
			self.exit_state()

	def render(self, display):
		# render the gameworld behind the menu, which is right before the pause menu on the stack
		#self.game.state_stack[-2].render(display)
		self.draw_background(display)
		for s in self.soldiers:
			s.battle.draw(display)
			s.battle.draw(display)
		for b in self.bullets:
			pygame.draw.rect(display, (255,255,255), b.rect)
		self.draw_battle_details_box(display)
		self.structures_img.draw(display)
		for b in self.buildings:
			pygame.draw.rect(display, (255,255,255), b.rect, 1)
	
	
class BattleSoldier():
	def __init__(self, soldier, player, sprites, battle):
		self.state = "idle"
		self.battle = battle
		self.soldier = soldier
		self.player = player
		self.sprites = sprites
		self.rect = pygame.Rect(0, 0, 15, 15)
		self.pos_x = self.rect.centerx
		self.pos_y = self.rect.centery
		self.reload = random.randint(100, 500)
		self.path_cooldown = 0
		self.target = None
		self.move_path = None
		self.image = sprites
		self.current_frame, self.last_frame_update = 0,0
		self.curr_image = self.sprites
		self.sprite_rect = self.curr_image.get_rect()
		self.curr_anim_list = [self.sprites]
		self.font = self.battle.game.body_font
		self.name_text = self.font.render(self.soldier.name, False, (255,203,0))
		if self.soldier.primary_weapon == "None":
			self.primary_weapon = self.battle.game.items["weapon"]["unarmed"]
		else:
			self.primary_weapon = self.battle.game.items["weapon"][self.soldier.primary_weapon]
			
		#self.move_path = astar(self.battle.map, (int(self.rect.centerx/10), int(self.rect.centery/10)), (5, 5), grid="battle")
		self.log_c = 120
		self.paths = 0
		self.pos = None
		
		self.vel = pygame.math.Vector2(0, 0)
		self.max_speed = 0.5
		
		self.move_path_index = 0
		self.move_path_target = None
		self.move_path_target_radius = 50

	def log(self, t):
		if self.log_c<=0:
			self.log_c = 120
			print(str(t))
	def Melee(self):
			melee_range_enemy_soldiers  = [s for s in self.battle.soldiers if s.battle.player!=self.player and (abs(s.battle.rect.centerx-self.rect.centerx)<50) and (abs(s.battle.rect.centery-self.rect.centery)<50)]
			if len(melee_range_enemy_soldiers)>0:
				self.state = "idle"
				self.move_path = None
				if self.reload <= 0:
					print(self.soldier.name+" MELEE ATTACK.")
					chosen = random.choice(melee_range_enemy_soldiers).battle
					self.target = chosen
					hit_roll = random.randint(1, self.soldier.strength) + random.randint(1, 100)
					opposing_roll = random.randint(1, self.target.soldier.strength) + random.randint(1, self.target.soldier.agility)
					self.reload = random.randint(100-self.soldier.agility, 100)
					if hit_roll > opposing_roll:
						self.target.soldier.hp -= 1
						self.target.soldier.state = "idle"
						self.target.soldier.move_path = None
						self.target.target = self
						print(self.soldier.name+" melee hit "+self.target.soldier.name)
			else:
				return(False)
				
	def inSight(self, target, range_):
		line_of_sight = self.battle.game_world.get_line(self.rect.center, target.rect.center)
		zone = self.rect.inflate(range_,range_)
		obstacles_list = [rectangle.rect for rectangle in self.battle.buildings] #to support indexing
		obstacles_in_sight = zone.collidelistall(obstacles_list)
		for x in range(1,len(line_of_sight),5):
			for obs_index in obstacles_in_sight:
				if obstacles_list[obs_index].collidepoint(line_of_sight[x]):
					return False
		return True

	def movePath(self, delta_time):
		if (self.move_path is not None) and (len(self.move_path)>0):
			# A vector pointing from self to the target.
			heading = self.move_path_target - self.pos
			distance = heading.length()  # Distance to the target.
			heading.normalize_ip()
			if distance <= 2 and (len(self.move_path)>1):  # We're closer than 2 pixels.
				# Increment the waypoint index to swtich the target.
				# The modulo sets the index back to 0 if it's equal to the length.
				self.move_path_index = (self.move_path_index + 1)
				self.move_path_target = self.move_path[self.move_path_index]
			self.vel = heading * self.max_speed

			self.pos += self.vel
			self.rect.x = self.pos[0]
			self.rect.y = self.pos[1]
			if (self.move_path_index)>len(self.move_path)-1:
				print(self.soldier.name+" move path endded since self.move_path_index == "+str(self.move_path_index+1)+" and length of self.move_path == "+str(len(self.move_path)))
				self.move_path = None
				self.move_path_index = 0
				self.state = "idle"
				return(False)
			'''
		if (self.move_path != None) and (len(self.move_path)!=1):
			self.state = "moving"
			curr_x, curr_y = self.rect.centerx, self.rect.centery
			diff = (curr_x - self.move_path[0][0]*10, curr_y-self.move_path[0][1]*10)
			distance = math.sqrt(diff[0]**2 + diff[1]**2)
			speed = 5*delta_time
			if diff == (0, 0):
				print("popping new path location")
				print(str((self.rect.centerx, self.rect.centery)))
				self.move_path.pop(0)
				print("heading to "+str(self.move_path))
				diff = (curr_x - self.move_path[0][0]*10, curr_y-self.move_path[0][1]*10)
			diff_norm = ((5*delta_time) * (diff[0]), (5*delta_time) * (diff[1] / distance))
			self.rect.centerx = int(self.rect.centerx-diff_norm[0])
			self.rect.centery = int(self.rect.centery-diff_norm[1])
			print(str((self.move_path[0][0]*10, self.move_path[0][1]*10)))
			return(True)
		else:
			print("move path complete")
			self.state="idle"
			self.move_path = None
			return(False)
	'''
	def moveRandom(self, delta_time):
		if self.walkCooldown <= 0:
			self.WalkReset()
			randMove = random.randint(1,3)
			randDistance = 10*delta_time
			if self.player == 1:
				if randMove == 1:
					self.rect.x += randDistance*100
				if randMove == 2:
					self.rect.y -= randDistance*100
				if randMove == 3:
					self.rect.y += randDistance*100
			if self.player == 2:
				if randMove == 1:
					self.rect.x -= randDistance*100
				if randMove == 2:
					self.rect.y += randDistance*100
				if randMove == 3:
					self.rect.y -= randDistance*100
					self.rect.y -= randDistance*100
			return(True)
		else:
			return(False)
		
		
	def chargePath(self, delta_time):
		if self.state=="idle":
			if self.target is None:
				enemy_soldiers  = [s.battle for s in self.battle.soldiers if s.battle.player!=self.player]
				closest = enemy_soldiers[0]
				closest_diff = max([abs(closest.rect.centerx-self.rect.centerx), abs(closest.rect.centery-self.rect.centery)])
				for e in enemy_soldiers:
					hd = abs(e.rect.centerx-self.rect.centerx)
					vd = abs(e.rect.centery-self.rect.centery)
					if max([hd, vd])<closest_diff:
						closest_diff = max([hd, vd])
						closest = e
					if closest_diff < 50:
						self.state = "idle"
					else:
						self.target = closest
						self.state="charge"
						print(self.soldier.name+" CHARGING "+self.target.soldier.name)
		if self.state=="charge":
			print("CHARGE")
			if self.target is not None:
				print(self.soldier.name+"'s CHARGE target is "+self.target.soldier.name+". ")
				target_x, target_y = int(self.target.pos[0]/10), int(self.target.pos[1]/10)
				self.log(self.soldier.name+" targetting "+str((target_x, target_y)))
				curr_x, curr_y = int(self.pos[0]/10), int(self.pos[1]/10)
				if self.move_path is not None:
					print(self.soldier.name+" has a CHARGE path.")
					self.path_cooldown -= 1
					if (self.move_path[-1] != (target_x, target_y)) and (self.path_cooldown<=0):
						print("--new CHARGE path for "+self.soldier.name)
						self.move_path = astar(self.battle.map, (curr_x, curr_y), (target_x, target_y), grid="battle")
						print(str((curr_x, curr_y))+" to "+str(self.move_path))
						self.path_cooldown = 500*len(self.move_path)
						self.move_path_index = 0
						self.move_path_target = self.move_path[self.move_path_index]
				elif self.move_path == None:
					print(self.soldier.name+" at ("+str(self.rect.x)+", "+str(self.rect.y)+") is getting a CHARGE path for target "+self.target.soldier.name+" at "+str(self.target.rect.x)+", "+str(self.target.rect.y)+" using coordinates "+str(target_x)+", "+str(target_y)+" and using "+str(curr_x)+", "+str(curr_y)+" as a starting position.")
					self.move_path = astar(self.battle.map, (curr_x, curr_y), (target_x, target_y), grid="battle")
					self.path_cooldown = 400*len(self.move_path)
					self.move_path_index = 0
					self.move_path_target = self.move_path[self.move_path_index]
					print(self.soldier.name+"'s starting  CHARGE path "+str(self.move_path)+", first move is from ("+str(self.rect.x)+", "+str(self.rect.y)+") to "+self.target.soldier.name+" at "+str(self.move_path_target)+".")
				if (len(self.move_path)==0) or (self.move_path==None):
					print(self.soldier.name+" charge path endded since the generated move_path has no elements")
					self.state = "idle"
					self.move_path = None
					return(False)

					


			'''
		if self.state=="idle":
			if self.target is None:
				enemy_soldiers  = [s.battle for s in self.battle.soldiers if s.battle.player!=self.player]
				closest = enemy_soldiers[0]
				closest_diff = max([abs(closest.rect.centerx-self.rect.centerx), abs(closest.rect.centery-self.rect.centery)])
				for e in enemy_soldiers:
					hd = abs(e.rect.centerx-self.rect.centerx)
					vd = abs(e.rect.centery-self.rect.centery)
					if max([hd, vd])<closest_diff:
						closest_diff = max([hd, vd])
						closest = e
				self.target = closest
			self.state="charge"
			print(self.soldier.name+" charging "+self.target.soldier.name)
		if self.target is not None:
			target_x, target_y = int(self.target.rect.x/10), int(self.target.rect.y/10)
			self.log(self.soldier.name+" targetting "+str((target_x, target_y)))
			curr_x, curr_y = int(self.rect.centerx/10), int(self.rect.centery/10)
			if self.charge_path is not None:
				self.path_cooldown -= 1
				if (self.charge_path[-1] != (target_x, target_y)) and (self.path_cooldown<=0):
					self.charge_path = astar(self.battle.map, (curr_x, curr_y), (target_x, target_y), grid="battle")
					self.charge_path.pop(0)
					self.paths += 1
					self.log(self.paths)
					self.path_cooldown = 120
			elif self.charge_path == None:
				self.path_cooldown = 120
				self.charge_path = astar(self.battle.map, (curr_x, curr_y), (target_x, target_y), grid="battle")
				self.charge_path.pop(0)
				self.paths += 1
			self.move_to_adjacent(delta_time)
				'''
				

		
		
		
	def Shoot(self):
		if self.target is None:
			enemy_soldiers  = [s for s in self.battle.soldiers if s.battle.player!=self.player]
			for e in enemy_soldiers:
				if self.inSight(e.battle, 300):
					self.target = e.battle
					print(self.soldier.name+" beginning to SHOOT at "+self.target.soldier.name+".")
					break
		if self.reload <= 0 and self.state=="idle" and self.target is not None:
			if self.inSight(self.target, 300):
				print(self.soldier.name+" SHOOTS at "+self.target.soldier.name+".")
				hit_roll = random.randint(1, 100)
				if hit_roll <= self.soldier.marksmanship:
					destX = self.target.rect.centerx
					destY = self.target.rect.centery
					dest = [destX, destY]
				else:
					deviation = hit_roll - self.soldier.marksmanship
					deviation_x = deviation - random.randint(0, deviation)
					deviation_y = deviation - deviation_x
					destX = self.target.rect.centerx - deviation_x
					destY = self.target.rect.centery - deviation_y
					dest = [destX, destY]
				self.battle.bullets.append(Bullet(self, self.player, dest))
				self.reload = random.randint(100,200)
				return(True)
			else:
				return(False)
		else:
			return(False)
	  
	def WalkReset(self):
		self.walkCooldown = random.randint(10, 100)
	
	
	def SetPos(self):
		if self.player == 1:
			self.squad_name = self.battle.squad_1.name
			self.squad_name_text = self.font.render(self.squad_name, False, (135,151,255))
			self.color = (255,255,255)
			ranX = random.randint(1 , 5)
			ranY = random.randint(1, 46)
			while self.battle.map[ranX][ranY]==1:
				ranX = random.randint(2 , 7)
				ranY = random.randint(1, 46)
			self.rect.x = ranX*10
			self.rect.y = ranY*10
			self.sprite_rect.center = self.rect.center
			self.name_text = self.font.render(self.soldier.name, False, (135,151,255))
		elif self.player == 2:
			self.squad_name = self.battle.squad_2.name
			self.squad_name_text = self.font.render(self.squad_name, False, (255,135,135))
			self.color = (0,0,255)
			ranX = random.randint(57, 60)
			ranY = random.randint(1, 46)
			while self.battle.map[ranX][ranY]==1:
				ranX = random.randint(58, 61)
				ranY = random.randint(1, 46)
			self.rect.y = ranY*10
			self.rect.x = ranX*10
			self.sprite_rect.center = self.rect.center
			self.curr_image = pygame.transform.rotate(self.curr_image, 180)
			self.name_text = self.font.render(self.soldier.name, False, (255,135,135))
		print("--positioning "+self.soldier.name+" at ("+str(self.rect.x)+", "+str(self.rect.y)+")")
		self.pos = pygame.math.Vector2(self.rect.x, self.rect.y)
		
	def update(self, delta_time):
		if self.target== None:
			print(self.soldier.name+" has no target.")
			self.state = "idle"
		self.log_c -= 1
		if self.target is not None:
			if not self.target.soldier in self.battle.soldiers:
				print(self.soldier.name+" target "+self.target.soldier.name+" doesn't exist.")
				self.target = None
			else:
				rel_x, rel_y = self.target.rect.centerx - self.rect.centerx, self.target.rect.centery - self.rect.centery
				angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
				self.curr_image = pygame.transform.rotate(self.sprites, int(angle))
				self.sprite_rect = self.curr_image.get_rect()
		self.reload -= 1
		self.walkCooldown -= 1
		if not self.Melee():
			if self.primary_weapon["type"] == "melee":
				self.chargePath(delta_time)
			if self.primary_weapon["type"] == "light":
				if not self.Shoot():
					pass
					#self.moveRandom(delta_time)
			if not self.movePath(delta_time):
				pass

		self.sprite_rect.center = self.rect.center
		print(self.soldier.name+" is at ("+str(self.rect.x)+", "+str(self.rect.y)+"). ")
		
		# Animate the sprite
		#self.animate(delta_time,direction_x,direction_y)

	
	def draw(self, display):
		#pygame.draw.rect(display, (self.color), self.rect)

		display.blit(self.curr_image, self.sprite_rect)
		text_rect = self.name_text.get_rect(center=((self.rect.x,self.rect.y+20)))
		display.blit(self.name_text, text_rect)
		if self.move_path is not None:
			for coord in self.move_path:
				pygame.draw.rect(display, (255, 0, 0), (coord[0], coord[1], 10, 10), 1)
			print(self.move_path)
		pygame.draw.rect(display, (255, 255, 0), (self.pos[0], self.pos[1], 2, 2), 1)
		#Drawing the soldier's health
		if self.soldier.hp > 0:
			for heart in range(1, self.soldier.hp+1):
				display.blit(self.battle.game_world.heart_img, ((text_rect.x+text_rect.width)-(heart*5), text_rect.y + text_rect.height), (0+5*(heart%2), 0, 5+5*(heart%2), 9))

'''
	def render(self, display):
		display.blit(self.curr_image, (self.position_x,self.position_y))

	def animate(self, delta_time):
		# Compute how much time has passed since the frame last updated
		self.last_frame_update += delta_time
		# If no direction is pressed, set image to idle and return
		if not (direction_x or direction_y): 
			self.curr_image = self.curr_anim_list[0]
			return
		# If an image was pressed, use the appropriate list of frames according to direction
		if direction_x:
			if direction_x > 0: self.curr_anim_list = self.right_sprites
			else: self.curr_anim_list = self.left_sprites
		if direction_y:
			if direction_y > 0: self.curr_anim_list = self.front_sprites
			else: self.curr_anim_list = self.back_sprites
		# Advance the animation if enough time has elapsed
		if self.last_frame_update > .15:
			self.last_frame_update = 0
			self.current_frame = (self.current_frame +1) % len(self.curr_anim_list)
			self.curr_image = self.curr_anim_list[self.current_frame]
'''

class Bullet():
	def __init__(self, shooter, squad, dest):
		self.squad = squad
		self.rect = pygame.Rect(2,2,2,2)
		self.destX = dest[0]
		self.destY = dest[1]
		self.rect.x = shooter.rect.x
		self.rect.y = shooter.rect.y
		self.startX = shooter.rect.x
		self.startY = shooter.rect.y
		self.positionX = shooter.rect.x
		self.positionY = shooter.rect.y
		self.speed = 4
	
	def update(self, delta_time):
		diff = (self.startX - self.destX, self.startY - self.destY)
		distance = math.sqrt(diff[0]**2 + diff[1]**2)
		diff_norm = ((self.speed*100*delta_time) * (diff[0] / distance), (self.speed*100*delta_time) * (diff[1] / distance))
		self.positionX -= diff_norm[0]
		self.positionY -= diff_norm[1]
		self.rect.x = int(self.positionX)
		self.rect.y = int(self.positionY)
		

class Block(pygame.sprite.Sprite):

	# Constructor. Pass in the color of the block,
	# and its x and y position
	def __init__(self, x, y, image):
	   # Call the parent class (Sprite) constructor
	   pygame.sprite.Sprite.__init__(self)

	   # Create an image of the block, and fill it with a color.
	   # This could also be an image loaded from the disk.
	   self.image = image

	   # Fetch the rectangle object that has the dimensions of the image
	   # Update the position of this object by setting the values of rect.x and rect.y
	   self.rect = self.image.get_rect()
	   self.rect.x = x
	   self.rect.y = y
	   
class Building():

	def __init__(self, rect):
	   self.rect = rect
