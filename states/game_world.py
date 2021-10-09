import pygame, os, json
from random import seed, randint, random, choice

from states.state import State
from states.viewport import MapViewport
from states.details import SquadDetails
from states.pause_menu import PauseMenu
from states.battle import Battle
from objects import Quadrant, Squad, Soldier
from enemy import Enemy
from pathing import Node, astar
from maker import Maker


class Game_World(State):
	def __init__(self, game):
		State.__init__(self,game)
		self.maker = Maker()
		self.player = Player(self.game)
		self.map_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"]
		self.quadrants = []
		self.squads = []
		self.turn = 0
		self.turn_events = []
		self.viewport_state_stack = []
		self.details_state_stack = []
		self.load_images()
		self.load_data()
		self.load_states()
		self.enemy = Enemy(self)
		
	def load_data(self):
		#Load Quadrant Data
		data = self.game.data["quadrants"]
		quadrants = []
		number = 0
		for y in data:
			row = []
			for x in y:
				row.append(Quadrant(x))
			quadrants.append(row)
		self.quadrants = quadrants
		#Load Squad Data
		for i in self.game.data["squads"]:
				self.squads.append(Squad(i))
	
	def load_images(self):
		self.template_img = pygame.image.load(os.path.join(self.game.assets_dir, "map", "template_map.png"))
		self.portraits_img = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "soldiers",  "portraits.png"))
		self.heart_img = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "soldiers",  "heart.png"))
		self.viewport_map_img = pygame.image.load(os.path.join(self.game.assets_dir, "map", "viewport_map.png"))
		self.viewport_quebec_img = pygame.image.load(os.path.join(self.game.assets_dir, "map", "quebec.png"))
		self.blank_img = pygame.image.load(os.path.join(self.game.assets_dir, "map", "blank.png"))

		self.battlefield_img = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "battlefield", "grass02.png"))
		self.viewport_squad_img = {"player":pygame.image.load(os.path.join(self.game.assets_dir, "map", "player_squad.png")), "enemy":pygame.image.load(os.path.join(self.game.assets_dir, "map", "enemy_squad.png"))}
		
		self.building_tile_img = {}
		building_tiles = ["left", "right", "top", "bottom", "top-left", "top-right", "bottom-left", "bottom-right", "middle"]
		for tile in building_tiles:
			self.building_tile_img[tile] = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "battlefield", "buildings", tile+".png"))
		#Loading the soldier sprites for battles
		soldier_battle_img = {}
		soldier_battle_img["01"] = pygame.transform.rotate(pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "soldiers",  "battle_soldier_01.png")), 180)
		soldier_battle_img["02"] = pygame.transform.rotate(pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "soldiers",  "battle_soldier_02.png")), 180)
		self.soldier_battle_img = soldier_battle_img
		
		#Loading all the weapon and item sprites
		self.weapon_img = {}
		self.head_img = {}
		self.torso_img = {}
		self.legs_img = {}
		self.item_img = {}
		for key, value in self.game.items["weapon"].items():
			self.weapon_img[key] = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "weapons", value["image"]))
		for key, value in self.game.items["head"].items():
			self.head_img[key] = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "head", value["image"]))
		for key, value in self.game.items["torso"].items():
			self.torso_img[key] = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "torso", value["image"]))
		for key, value in self.game.items["legs"].items():
			self.legs_img[key] = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "legs", value["image"]))
		for key, value in self.game.items["item"].items():
			self.item_img[key] = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "item", value["image"]))



	def load_states(self):
		#Load Viewport State
		self.viewport = MapViewport(self)
		self.viewport_state_stack.append(self.viewport)
		#Load Details State
		self.details = SquadDetails(self)
		self.details_state_stack.append(self.details)
		
	def turn_manager(self):
		#Enemy submits their orders
		self.enemy.take_turn()
		#Turn is over, add one to the turn counter
		self.turn += 1
		print("-----TURN END-----")
		print("--starting turn "+str(self.turn))
		print("--processing "+str(len(self.turn_events))+" events.")
		#Processing all the orders and events
		for event in self.turn_events:
			print(str(event["turn"])+" "+event["squad"].name)
		#Only executing the events that are set to execute this turn
			if event['turn'] <= self.turn:
				if event["type"] == "move":
					self.move_squad(event["squad"], event["destination"])
				if event["type"] == "recruit":
					self.squad_recruit(event["squad"])
		#Saving future events for later
		next_events = []
		for event in self.turn_events:
			if event['turn'] > self.turn:
				next_events.append(event)
			else:
				print("--removing "+event['type']+" "+event["squad"].name+" from queue.")
		self.turn_events = next_events
		print("--remaining events "+str(len(self.turn_events)))

		
	def squad_recruit(self, squad):
		leadership_scores = []
		recruit_roll = randint(1, 100)
		for soldier in squad.soldiers:
			leadership_scores.append(soldier.leadership)
		leadership_scores = sorted(leadership_scores, reverse=True)
		if len(leadership_scores)>0:
			recruit_roll += int(leadership_scores[0]/5)
		if len(leadership_scores)>1:
			recruit_roll += int(leadership_scores[1]/10)
		if len(leadership_scores)>2:
			recruit_roll += int(leadership_scores[2]/10)
		if recruit_roll>50:
			number = int(recruit_roll/45) 
			for s in self.squads:
				if s == squad:
					for new_soldier in self.maker.MakeSoldiers(number, "Quebec"):
						s.soldiers.append(new_soldier)

	def create_squad(self, name, location, soldiers=None):
		squad = self.maker.MakeSquad(name, location, 1)
		self.squads.append(squad)
		if soldiers is not None:
			if isinstance(soldiers, list):
				for soldier in soldiers:
					self.move_soldier(soldier, self.squads[-1])
			else:
				self.move_soldier(soldiers, self.squads[-1])

	def remove_empty_squads(self):
		empty_squads = [s for s in self.squads if len(s.soldiers)==0]
		for squad in self.squads:
			if squad in empty_squads:
				self.squads.remove(squad)

	def move_squad(self, squad, destination):
		print("--move_squad "+squad.name)
		for s in self.squads:
			if s == squad:
				s.status = "transit"
				if (s.x, s.y) == destination:
					print(s.name + " is already in "+str(destination))
					s.status = "idle"
				else:
					print("--finding path")
					path = astar(self.quadrants, (s.x, s.y), destination)
					s.x = path[1][0]
					s.y = path[1][1]
				if (s.x, s.y) == destination:
						print(s.name + " has arrived in "+str(destination))
						s.status = "idle"
				else:
					print("--adding move "+s.name+" to queue")
					self.turn_events.append({"turn":self.turn+1, "type":"move", "squad":s, "destination":destination}) 
	
	def move_soldier(self, soldier, destination_squad):
		for squad in self.squads:
			print(squad.soldiers)
			if soldier in squad.soldiers:
				squad.soldiers.remove(soldier)
			if squad == destination_squad:
				squad.soldiers.append(soldier)
		return True


	def get_line(self, start, end):
		"""Bresenham's Line Algorithm
		Produces a list of tuples from start and end

		>>> points1 = get_line((0, 0), (3, 4))
		>>> points2 = get_line((3, 4), (0, 0))
		>>> assert(set(points1) == set(points2))
		>>> print points1
		[(0, 0), (1, 1), (1, 2), (2, 3), (3, 4)]
		>>> print points2
		[(3, 4), (2, 3), (1, 2), (1, 1), (0, 0)]
		"""
		# Setup initial conditions
		x1, y1 = start
		x2, y2 = end
		dx = x2 - x1
		dy = y2 - y1

		# Determine how steep the line is
		is_steep = abs(dy) > abs(dx)

		# Rotate line
		if is_steep:
			x1, y1 = y1, x1
			x2, y2 = y2, x2

		# Swap start and end points if necessary and store swap state
		swapped = False
		if x1 > x2:
			x1, x2 = x2, x1
			y1, y2 = y2, y1
			swapped = True

		# Recalculate differentials
		dx = x2 - x1
		dy = y2 - y1

		# Calculate error
		error = int(dx / 2.0)
		ystep = 1 if y1 < y2 else -1

		# Iterate over bounding box generating points between start and end
		y = y1
		points = []
		for x in range(x1, x2 + 1):
			coord = (y, x) if is_steep else (x, y)
			points.append(coord)
			error -= abs(dy)
			if error < 0:
				y += ystep
				error += dx

		# Reverse the list if the coordinates were swapped
		if swapped:
			points.reverse()
		return points


		
	def resolve_battles(self):
		#Resolve all battles
		#Find the location of all squads
		squad_locations = []
		for squad in self.squads:
			squad_locations.append((squad.x, squad.y))
		#Find locations occupied by more than one squad
		shared_locations = []
		for q in squad_locations:
			if squad_locations.count(q) > 1:
				shared_locations.append(q)
		shared_locations = list(set(shared_locations))
		for q in shared_locations:
		#Find all squads in a particular location with more than one squad
			occupants = [squad for squad in self.squads if (squad.x, squad.y) == q]
			number_of_different_players = len(list(set([o.player for o in occupants])))
			if number_of_different_players>1:
				for o in occupants:
					#Find out if the squad has any enemies
					enemy_squads = [e for e in occupants if e.player != o.player]
					if enemy_squads is not None:
						if len(enemy_squads)>0:
							enemy = choice(enemy_squads)
							print("--"+o.name+" battling "+enemy.name+" in quadrant "+str(q))
							new_state = Battle(self, o, enemy)
							new_state.enter_state()
							break
				break

	def update(self,delta_time, actions, mouse):
		self.remove_empty_squads()
		self.resolve_battles()
		# Check if the game was paused
		if actions["action2"]:
			self.squads.append(self.maker.MakeEnemySquad())
			self.game.actions["action2"] = False
		#if actions["action1"]:
		#	self.details_state_stack[-1].load_buttons()
		#	self.game.actions["action1"] = False
		#if actions["start"]:
		#	new_state = PauseMenu(self.game)
		#	new_state.enter_state()
		self.viewport_state_stack[-1].update(delta_time, actions, mouse)
		self.details_state_stack[-1].update(delta_time, actions, mouse)
		self.player.update(delta_time, actions, mouse)
	
	def render(self, display):
		display.blit(self.template_img, (0,0))
		self.viewport_state_stack[-1].render(display)
		self.details_state_stack[-1].render(display)
		self.player.render(display)
		

class Player():
	def __init__(self,game):
		self.game = game
		self.load_sprites()
		self.position_x, self.position_y = 200,200
		self.current_frame, self.last_frame_update = 0,0
		

	def update(self,delta_time, actions, mouse):
		# Get the direction from inputs
		direction_x = actions["right"] - actions["left"]
		direction_y = actions["down"] - actions["up"]
		# Update the position
		self.position_x += 100 * delta_time * direction_x
		self.position_y += 100 * delta_time * direction_y
		# Animate the sprite
		self.animate(delta_time,direction_x,direction_y)


	def render(self, display):
		display.blit(self.curr_image, (self.position_x,self.position_y))

	def animate(self, delta_time, direction_x, direction_y):
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

	def load_sprites(self):
		# Get the diretory with the player sprites
		self.sprite_dir = os.path.join(self.game.sprite_dir, "player")
		self.front_sprites, self.back_sprites, self.right_sprites, self.left_sprites = [],[],[],[]
		# Load in the frames for each direction
		for i in range(1,5):
			self.front_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "player_front" + str(i) +".png")))
			self.back_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "player_back" + str(i) +".png")))
			self.right_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "player_right" + str(i) +".png")))
			self.left_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "player_left" + str(i) +".png")))
		# Set the default frames to facing front
		self.curr_image = self.front_sprites[0]
		self.curr_anim_list = self.front_sprites


	
	
	
