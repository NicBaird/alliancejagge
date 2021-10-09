import pygame, os
from states.state import ViewportState
from pathing import Node, astar

class MapViewport(ViewportState):
	def __init__(self, game_world):
		self.game_world = game_world
		ViewportState.__init__(self, game_world)
		self.quadrant_buttons = []
		
		self.load_buttons()
	
	def load_buttons(self):
		width, height = 20, 17
		number = 0
		self.next_turn_button = NextTurnButton(self.game_world)
		
		for row in self.game_world.quadrants:
			for quadrant in row:
				button = QuadrantButton(self.game_world, quadrant)
				button.rect.x += self.chartx
				button.rect.y += self.charty
				self.quadrant_buttons.append(button)

	def draw_quadrants(self, display):
		for button in self.quadrant_buttons:
			button.draw(display)
			
	def draw_lines(self, display):
		x, y = 308, 44
		xlinesleft = 15
		ylinesleft = 15
		while xlinesleft != 0:
			pygame.draw.line(display, (230, 230, 151), (x,26), (x,314))
			x += 21
			xlinesleft -= 1
		while ylinesleft != 0:
			pygame.draw.line(display, (230, 230, 151), (286,y), (623, y))
			y += 18
			ylinesleft -= 1


	def update(self, delta_time, actions, mouse):
		if actions["lclick"]:
			self.next_turn_button.update(self.next_turn_button.rect.collidepoint(mouse))
		if actions["action2"]:
			pass
			#self.exit_state()

	def render(self, display):
		display.blit(self.game_world.viewport_map_img, (self.x,self.y))
		display.blit(self.game_world.viewport_quebec_img, (286,26))
		self.draw_quadrants(display)
		#Draw Grid lines
		self.draw_lines(display)
		self.next_turn_button.draw(display)

class Button():
	
	def __init__(self, rectangle):
		self.rect = rectangle
		

class QuadrantButton(Button):
	
	def __init__(self, game_world, d):
		width, height = 20, 17
		self.x, self.y = d.x, d.y
		rectangle = pygame.Rect((d.x*width)+d.x, (d.y*height)+d.y, width, height)
		Button.__init__(self, rectangle)
		self.game_world = game_world
		self.location = d.location
		self.path = []
		self.hover = False

	def draw(self, display):
		number_of_squads = 0
		number_of_enemy_squads = 0
		for squad in self.game_world.squads:
			if (squad.x, squad.y) == (self.x, self.y):
				if squad.player ==1:
					number_of_squads += 1
				else: 
					number_of_enemy_squads +=1
		for i in range (0, number_of_squads+number_of_enemy_squads):
			if i >= number_of_squads:
				display.blit(self.game_world.viewport_squad_img["enemy"], ((self.rect.width + self.rect.x)-(4*(i+1)), self.rect.y + self.rect.height - 8))
			else:
				display.blit(self.game_world.viewport_squad_img["player"], ((self.rect.width + self.rect.x)-(4*(i+1)), self.rect.y + self.rect.height - 8))

class NextTurnButton(Button):
	def __init__(self, game_world):
		self.game_world = game_world
		rectangle = pygame.Rect(538, 419, 20, 10)
		Button.__init__(self, rectangle)
		self.font = self.game_world.game.body_font
		 
	def draw(self, display):
		pygame.draw.rect(display, (255, 0, 0), self.rect, 1)
		text = self.font.render(str(self.game_world.turn), True, (231,212,214))
		text_rect = text.get_rect(center=(self.rect.x+(self.rect.width/2), self.rect.y+(self.rect.height/2)))
		display.blit(text, text_rect)

	def update(self, click):
		if click:
			self.game_world.turn_manager()
			self.game_world.game.actions['lclick'] = False


class MoveViewport(ViewportState):
	def __init__(self, game_world, squad):
		self.squad = squad
		ViewportState.__init__(self, game_world)
		self.viewport_map_img = pygame.image.load(os.path.join(self.game_world.game.assets_dir, "map", "viewport_map_move_select.png"))
		self.quadrant_buttons = []
		
		self.load_buttons()
	
	def load_buttons(self):
		for row in self.game_world.quadrants:
			for quadrant in row:
				button = QuadrantButton(self.game_world, quadrant)
				button.rect.x += self.chartx
				button.rect.y += self.charty
				self.quadrant_buttons.append(button)
		
	def draw_quadrants(self, display):
		for button in self.quadrant_buttons:
			if button.hover:
				for b in self.quadrant_buttons:
					if (b.x, b.y) in button.path:
						pygame.draw.rect(display, (255, 0, 0), b.rect, 1)
				break

	def update(self, delta_time, actions, mouse):
		number = 0
		for button in self.quadrant_buttons:
			if (button.rect.collidepoint(mouse)):
				button.hover = True
				button.path = astar(self.game_world.quadrants, (self.squad.x, self.squad.y), (button.x, button.y))
				if actions["lclick"]:
					for event in self.game_world.turn_events:
						if "squad" in event.keys():
							if (event["squad"]==self.squad) and (event["type"] in ["move", "train"]):
								self.game_world.turn_events.remove(event)
								print("CANCEL ORDER: "+self.squad.name+" "+event["type"])
					print("ORDER: "+self.squad.name+" move to "+str(button.x)+", "+str(button.y))
					self.game_world.turn_events.append({"turn": (self.game_world.turn + 1), "type":"move", "squad": self.squad, "destination" : (button.x, button.y)})
					
					print("exiting state")
					self.game_world.game.actions['lclick'] = False
					self.exit_state()
					
			else:
				button.hover = False
			number += 1
		if actions["lclick"]:
			self.game_world.game.actions['lclick'] = False
			self.exit_state()

	def render(self, display):
		self.prev_state_viewport.render(display)
		display.blit(self.viewport_map_img, (self.x,self.y))
		self.draw_quadrants(display)
