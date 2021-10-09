import pygame, os
from states.state import DetailsState
from states.viewport import MoveViewport
from inputbox import InputBox

class SquadDetails(DetailsState):
	def __init__(self, game_world):
		DetailsState.__init__(self, game_world)
		self.soldier_info_img = pygame.image.load(os.path.join(self.game_world.game.assets_dir, "map", "soldier_info.png"))
		self.details_squad_img = pygame.image.load(os.path.join(self.game_world.game.assets_dir, "map", "details_squad.png"))
		#self.soldier_stat_text = {"Level" : self.game_world.game.body_font("LVL", False, (255,203,0)), "Agility" : self.game_world.game.body_font("AGI", False, (255,203,0)), "Strength" : self.game_world.game.body_font("STR", False, (255,203,0)), "Leadership" : self.game_world.game.body_font("LDR", False, (255,203,0)), "Marskmanship" : self.game_world.game.body_font("MRK", False, (255,203,0))}
		self.selected_soldier = None
		self.selected_squad = None
		self.drag = None
		self.squad_buttons = []
		self.load_buttons()

	def load_buttons(self):
		self.squad_buttons = []
		number = 0
		for squad in self.game_world.squads:
			if squad.player == 1:
				self.squad_buttons.append(SquadButton(self.x, self.y, number, squad, self.game_world, self.selected_soldier))
				number += 1
		self.position_buttons()
		

			
	def position_buttons(self):
		if len(self.squad_buttons)>0:
			for b in range(0, len(self.squad_buttons)):
				if b is not 0:
					if previous_button.expanded:
						y_adjustment = previous_button.rect.y + previous_button.rect.height*(len(previous_button.soldier_buttons)+1)
						self.squad_buttons[b].rect.y =  y_adjustment
						self.squad_buttons[b].collapse_button.rect.y = y_adjustment
					else:
						y_adjustment = previous_button.rect.y + (self.squad_buttons[b].rect.height)
						self.squad_buttons[b].rect.y = y_adjustment
						self.squad_buttons[b].collapse_button.rect.y = y_adjustment
				for i in range(0, len(self.squad_buttons[b].soldier_buttons)):
					self.squad_buttons[b].soldier_buttons[i].rect.y  = self.squad_buttons[b].rect.y + (self.squad_buttons[b].rect.height*(i+1))
				previous_button = self.squad_buttons[b]

				
	
	def draw_buttons(self, display):
		featured_soldier = self.selected_soldier
		featured_squad = self.selected_squad
		for squad in self.squad_buttons:
			#Drawing the squad and all its soldier buttons
			squad.draw(display)
		
		#Checking if any soldier is featured
			if featured_soldier is None:
				for soldier in squad.soldier_buttons:
					if soldier.hover:
						featured_soldier = soldier.soldier
						featured_squad = squad.squad
		
		#If there is a featured soldier, then put it in the soldier info panel
		if featured_soldier is not None:
			#Drawing soldier's attribute numbers
			level_text = featured_soldier.level
			agility_text = featured_soldier.agility
			strength_text = featured_soldier.strength
			leadership_text = featured_soldier.leadership
			marksmanship_text = featured_soldier.marksmanship
			y = 0
			for i in [level_text, agility_text, strength_text, leadership_text, marksmanship_text]:
				text_surface = self.game_world.game.body_font.render(str(i), True, (255,203,0))
				text_rect = text_surface.get_rect()
				text_rect.x = 108
				text_rect.y = 28+(y*(text_rect.height+2.8))
				display.blit(text_surface, text_rect)
				y += 1
			#Drawing soldier's name
			text_surface = self.game_world.game.body_font.render(featured_soldier.name, True, (255,203,0))
			text_rect = text_surface.get_rect(center=(80, 8))
			display.blit(text_surface, text_rect)
			
			#Drawing soldier's squad
			text_surface = self.game_world.game.body_font.render(featured_squad.name, True, (255,203,0))
			text_rect = text_surface.get_rect(center=(80, 7.5+text_rect.height+1))
			display.blit(text_surface, text_rect)
			
			#Drawing soldier's portrait
			if featured_soldier.portrait != 'None':
				num = featured_soldier.portrait
				display.blit(self.game_world.portraits_img, (4,23), (num*47, 0, 47, 54))
				
			#Drawing the soldier's health
			if featured_soldier.health != "None":
				for heart in range(1, featured_soldier.health+1):
					display.blit(self.game_world.heart_img, (50-(heart*5), 68), (0+5*(heart%2), 0, 5+5*(heart%2), 9))
			
			#Drawing soldier's primary weapon
			if featured_soldier.primary_weapon != 'None':
				if self.game_world.game.items["weapon"][featured_soldier.primary_weapon]["size"] == 2:
					display.blit(self.game_world.weapon_img[featured_soldier.primary_weapon], (2,82))
				if self.game_world.game.items["weapon"][featured_soldier.primary_weapon]["size"] == 1:
					display.blit(self.game_world.weapon_img[featured_soldier.primary_weapon], (14,82))
			
			#Drawing soldier's helmet
			if featured_soldier.head != 'None':
				display.blit(self.game_world.head_img[featured_soldier.head], (54,30))
			
			#Drawing soldier's torso
			if featured_soldier.torso != 'None':
				display.blit(self.game_world.torso_img[featured_soldier.torso], (54,57))
			
			#Drawing soldier's legs
			if featured_soldier.legs != 'None':
				display.blit(self.game_world.legs_img[featured_soldier.legs], (54,82))		
			
			#Drawing soldier's secondary weapon
			if featured_soldier.secondary_weapon != 'None':
				if self.game_world.game.items["weapon"][featured_soldier.secondary_weapon]["size"] == 2:
					display.blit(self.game_world.weapon_img[featured_soldier.secondary_weapon], (180,11))
				if self.game_world.game.items["weapon"][featured_soldier.secondary_weapon]["size"] == 1:
					display.blit(self.game_world.weapon_img[featured_soldier.secondary_weapon], (215,11))
			
			#Drawing soldier's inventory
			if len(featured_soldier.inventory) > 0:
				start_xy = [179,51]
				number = 0
				for item in featured_soldier.inventory:
					xy = (start_xy[0]+(25*(number%3)), start_xy[1]+(25*(int(number/3))))
					if item != 'None' :
						if item in self.game_world.game.items["weapon"]:
							display.blit(self.game_world.weapon_img[item], xy)
						if item in self.game_world.game.items["head"]:
							display.blit(self.game_world.head_img[item], xy)
						if item in self.game_world.game.items["torso"]:
							display.blit(self.game_world.torso_img[item], xy)
						if item in self.game_world.game.items["legs"]:
							display.blit(self.game_world.legs_img[item], xy)
						if item in self.game_world.game.items["item"]:
							display.blit(self.game_world.item_img[item], xy)
					number += 1
							
	def update(self, delta_time, actions, mouse):
		self.load_buttons()
		for squad in self.squad_buttons:
			if squad.rect.collidepoint(mouse):
			#Checking for Squad Buttons
				squad.hover = True
				if actions["rclick"]:
					if len(self.game_world.details_state_stack)==1:
						print("Right click on "+squad.name)
						new_state = RightClickDetails(self.game_world, squad.squad, mouse)
						new_state.enter_state()
						self.game_world.game.actions['rclick'] = False
				else:
					squad.hover = False
				#Checking for Soldier Buttons
			for soldier in squad.soldier_buttons:
				if soldier.rect.collidepoint(mouse):
					soldier.hover = True
					if actions["rclick"]:
						if len(self.game_world.details_state_stack)==1:
							print("Right click on "+soldier.name)
							new_state = RightClickDetails(self.game_world, soldier.soldier, mouse)
							new_state.enter_state()
							self.game_world.game.actions['rclick'] = False
					if actions["lclick"] and squad.expanded:
						if (self.drag is None) and (self.selected_soldier != soldier.soldier):
							self.selected_soldier = soldier.soldier
							self.selected_squad = squad.squad
							self.drag = mouse
				if not soldier.rect.collidepoint(mouse):
					soldier.hover = False
					if actions["lclick"] and squad.expanded and (self.drag is None):
						self.selected_soldier = None
						self.selected_squad = None
				if (self.selected_soldier == soldier.soldier) and (self.drag is not None):
					if abs(sum(self.drag)-sum(mouse))>5:
						if len(self.game_world.details_state_stack)==1:
							new_state = DragSoldierDetails(self.game_world, soldier, mouse)
							new_state.enter_state()

						
			#Checking for Collapse Button
			if squad.collapse_button.rect.collidepoint(mouse):
				squad.hover = True
				if actions["lclick"]:
					print("Click on Expanding Button for squad "+squad.name)
					squad.squad.expanded = not squad.squad.expanded
					self.game_world.game.actions['lclick'] = False
					
		if not actions["lclick"]:
			self.drag = None


	def render(self, display):
		display.blit(self.details_squad_img, (self.x,self.y))
		display.blit(self.soldier_info_img, (self.x,self.y))
		self.draw_buttons(display)

class SoldierButton():
	
	def __init__(self, rectangle, soldier, game_world):
		self.game_world = game_world
		self.name = soldier.name
		self.rect = rectangle
		self.soldier = soldier
		self.hover = False
		self.font = self.game_world.game.body_font
		self.name_text = self.font.render(self.name, False, (255,203,0))
		self.name_text_hover = self.font.render(self.name, False, (255,229,19))
		self.name_text_selected = self.font.render(self.name, False, (231,212,114))
		
class CollapseButton():
	
	def __init__(self, rectangle):
		self.rect = rectangle
		
	def create_arrow(self, expanded):
		if expanded:
			return([[self.rect.x+2, self.rect.y+2], [self.rect.x+(self.rect.height/2), self.rect.y+self.rect.height-2], [self.rect.x+self.rect.height-2, self.rect.y+2]])
		else:
			return([[self.rect.x+2, self.rect.y+2], [self.rect.x+2, self.rect.y+self.rect.height-2], [self.rect.x+self.rect.height-2, self.rect.y+(self.rect.height/2)]])

class SquadButton():
	
	def __init__(self, x, y, pos, squad, game_world, selected_soldier):
		self.game_world = game_world
		self.width, self.height = 230, 10
		self.pos = pos
		self.squad = squad
		self.rect = None
		self.rect = pygame.Rect(x+17, y+(self.height*0)+145, self.width, self.height)
		self.name = squad.name
		self.map_location = self.game_world.map_letters[self.squad.y]+str(self.squad.x+1)
		self.soldiers = squad.soldiers
		self.soldier_buttons = []
		self.collapse_button = None
		self.font = self.game_world.game.body_font
		self.location_text = self.font.render(self.map_location, False, (255,203,0))
		self.location_text_hover = self.font.render(self.map_location, False, (255,229,19))
		self.name_text = self.font.render(self.name, False, (255,203,0))
		self.name_text_hover = self.font.render(self.name, False, (255,229,19))
		self.hover = False
		self.expanded = squad.expanded
		self.selected_soldier = selected_soldier
		
		self.load_buttons()
		
	def load_buttons(self):
		#Loading Soldier Buttons
		if (len(self.soldiers)>0) and self.expanded:
			self.soldier_buttons = []
			number = 0
			for soldier in self.soldiers:
				soldier_rect = self.rect.copy()
				soldier_rect.y += (self.height*(number+1)) + number
				self.soldier_buttons.append(SoldierButton(soldier_rect, soldier, self.game_world))
				number += 1
			#Loading Collapse Button
		self.collapse_button = CollapseButton(pygame.Rect(self.rect.x-self.height, self.rect.y, self.height, self.height))
		

		
	def draw(self, display):
		#Drawing the temporary button bounds for ez visualization
		pygame.draw.rect(display, (255, 0, 0), self.rect, 1)
		pygame.draw.rect(display, (255, 0, 0), self.collapse_button.rect, 1)
		#Writing the Squad name and location text
		if self.hover:
			name_text = self.name_text_hover
			location_text = self.location_text_hover
			pygame.draw.polygon(display, (255, 229, 19), self.collapse_button.create_arrow(self.expanded), 1)
		else:
			name_text = self.name_text
			location_text = self.location_text
			pygame.draw.polygon(display, (255, 203, 0), self.collapse_button.create_arrow(self.expanded), 1)
		
		text_rect = name_text.get_rect(centery=(self.rect.y+(self.rect.height/2)))
		text_rect.x = self.rect.x
		display.blit(name_text, text_rect)
		text_rect = location_text.get_rect(center=(self.rect.x+142, self.rect.y+(self.rect.height/2)))
		display.blit(location_text, text_rect)
		
		#Writing the soldier buttons'
		if self.expanded:
			number = 0
			for button in self.soldier_buttons:
				pygame.draw.rect(display, (255, 0, 0), button.rect, 1)
				if button.soldier == self.selected_soldier:
					name_text = button.name_text_selected
					location_text = self.location_text_hover
				elif button.hover:
					name_text = button.name_text_hover
					location_text = self.location_text_hover
				else:
					name_text = button.name_text
					location_text = self.location_text
					
				text_rect = name_text.get_rect(centery=(button.rect.y+(button.rect.height/2)))
				text_rect.x = button.rect.x+10
				display.blit(name_text, text_rect)
				text_rect = location_text.get_rect(center=(button.rect.x+142, button.rect.y+(button.rect.height/2)))
				display.blit(location_text, text_rect)
				number += 1
	
			
	def update(self):
		pass
	
	def OnClick():
		pass

class RightClickDetails(DetailsState):
	def __init__(self, game_world, soldier_or_squad, click_location):
		self.game_world = game_world
		DetailsState.__init__(self, game_world)
		self.soldier_or_squad = soldier_or_squad
		self.click_location = click_location
		self.squad_menu_options = ["Order", "Inventory", "Manage"]
		self.soldier_menu_options = ["Assign", "Inventory", "Manage"]
		self.menu_buttons = []
		self.version = None
		print("RightClickDetails menu")
		if soldier_or_squad in self.game_world.squads:
			self.version = "squad"
		else:
			for s in self.game_world.squads:
				if soldier_or_squad in s.soldiers:
					self.version = "soldier"
		self.create_menu(self.version)

	def create_menu(self, version):
		number = 0
		menu_options = None
		if version == "squad":
			menu_options = self.squad_menu_options
		if version == "soldier":
			menu_options = self.soldier_menu_options
		for option in menu_options:
			self.menu_buttons.append(RightClickMenuButton(option, self.click_location, number, self.game_world.game.body_font))
			number += 1
			
				
	def update(self, delta_time, actions, mouse):
		for button in self.menu_buttons:
			if (button.rect.collidepoint(mouse)):
				if actions["lclick"]:
					print("left-click menu_button.")
					if self.version == "squad":
						if button.name == "Order":
							print("left-click on Move menu_button.")
							new_state = RightClickOrderDetails(self.game_world, self.soldier_or_squad, (button.rect.x+button.rect.width, button.rect.y), self.version)
							new_state.enter_state()
					if self.version == "soldier":
						if button.name == "Assign":
							print("left-click on Assign menu_button.")
							new_state = RightClickOrderDetails(self.game_world, self.soldier_or_squad, (button.rect.x+button.rect.width, button.rect.y), self.version)
							new_state.enter_state()	
					self.game_world.game.actions['lclick'] = False
						
		if actions["lclick"]:
			self.game_world.game.actions['lclick'] = False
			self.exit_state()

	def render(self, display):
		self.prev_state_details.render(display)
		for button in self.menu_buttons:
			button.draw(display)

class RightClickMenuButton():
	def __init__(self, name, click_location, pos, font):
		self.pos = pos
		self.width, self.height = 50, 10
		self.name = name
		self.text = font.render(self.name, True, (255,203,0))
		self.text_hover = font.render(self.name, True, (255,229,19))
		self.hover = False
		self.rect = pygame.Rect(click_location[0], click_location[1]+(self.pos*self.height), self.width, self.height)
		
	def draw(self, display):
		pygame.draw.rect(display, (255, 0, 0), self.rect, 1)
		if self.hover:
			text_surface = self.text.hover
		else:
			text_surface = self.text
		text_rect = text_surface.get_rect()
		text_rect.center = (self.rect.x+(self.rect.width/2), self.rect.y+(self.rect.height/2))
		display.blit(text_surface, text_rect)

class RightClickOrderDetails(DetailsState):
	def __init__(self, game_world, soldier_or_squad, click_location, version):
		self.game_world = game_world
		DetailsState.__init__(self, game_world)
		self.soldier_or_squad = soldier_or_squad
		self.click_location = click_location
		self.version = version
		self.nearby_squads = []
		self.menu_options = []
		self.squads = []
		self.location = None
		self.game_world.game.input_box = InputBox(100, 100, 140, 32, font=self.game_world.game.body_font)
		if version == "squad":
			self.menu_options = ["Move", "Defend", "Recruit"]
		if version == "soldier":
			self.menu_options.append("New")
			for s in self.game_world.squads:
				if soldier_or_squad in s.soldiers:
					self.location = (s.x, s.y)
					break
			for s in self.game_world.squads:
				if (s.x, s.y) == self.location:
					self.menu_options.append(s.name)
					self.squads.append(s)
		self.order_menu_buttons = []
		print("RightClickDetails menu")
		self.create_menu()


	def create_menu(self):
		number = 0
		for option in self.menu_options:
			self.order_menu_buttons.append(RightClickMenuButton(option, self.click_location, number, self.game_world.game.body_font))
			number += 1
			
				
	def update(self, delta_time, actions, mouse):
		for i in range(0, len(self.order_menu_buttons)):
			button = self.order_menu_buttons[i]
			if self.game_world.game.input_box.active == True:
				self.game_world.game.input_box.update()
				if actions["start"]:
					print("--submitting text")
					self.game_world.create_squad(self.game_world.game.input_box.text, self.location, self.soldier_or_squad)
					self.game_world.game.input_box.active = False
					self.exit_state()
					self.game_world.game.actions["start"] = False 
				if actions["lclick"]:
				#Checking for click on input box
						# If the user clicked on the input_box rect.
					if not self.game_world.game.input_box.rect.collidepoint(mouse):
						print("--clicking to deactivate text box")
						self.game_world.game.input_box.text = ''
						self.game_world.game.input_box.active = False
						self.exit_state()
					self.game_world.game.actions['lclick'] = False
			if (button.rect.collidepoint(mouse)):
				if self.version == "squad":
					if actions["lclick"]:
						if button.name == "Move":
							new_state = MoveViewport(self.game_world, self.soldier_or_squad)
							new_state.enter_state()
							self.exit_state()
							self.game_world.game.actions['lclick'] = False
						if button.name == "Recruit":
							for event in self.game_world.turn_events:
								if "squad" in event.keys():
									if (event["squad"]==self.soldier_or_squad) and (event["type"] in ["move", "train"]):
										self.game_world.turn_events.remove(event)
							self.game_world.turn_events.append({"turn" : self.game_world.turn+1, "type": "recruit", "squad": self.soldier_or_squad})
							self.exit_state()
							self.game_world.game.actions['lclick'] = False
				if self.version == "soldier":
					if actions["lclick"]:
						if i == 0:
							self.game_world.game.input_box.active = True
							self.game_world.game.actions['lclick'] = False

	def render(self, display):
		self.prev_state_details.render(display)
		for button in self.order_menu_buttons:
			button.draw(display)
		if self.game_world.game.input_box.active == True:
			self.game_world.game.input_box.draw(display)

class FloatingSoldierNameButton():
	def __init__(self, soldier_button, mouse):
		self.name_text = soldier_button.name_text
		self.rect = self.name_text.get_rect()
		self.mouse = mouse
	
	def draw(self,display):
		self.rect.center = self.mouse
		display.blit(self.name_text, self.rect)
		
	def update(self, mouse):
		self.mouse = mouse

class DragSoldierDetails(DetailsState):
	def __init__(self, game_world, soldier_button, click_location):
		self.game_world = game_world
		DetailsState.__init__(self, game_world)
		self.soldier_button = soldier_button
		self.click_location = click_location
		print("DragSoldierDetails menu")
		self.floating_soldier_name_button = FloatingSoldierNameButton(self.soldier_button, self.click_location)


	def update(self, delta_time, actions, mouse):
		self.floating_soldier_name_button.update(mouse)
		if not actions["lclick"]:
			squad_buttons = self.prev_state_details.squad_buttons
			for squad in squad_buttons:
				if self.soldier_button.soldier not in squad.squad.soldiers:
					for soldier in squad.soldier_buttons:
						if (soldier.rect.collidepoint(mouse)):
							self.game_world.move_soldier(self.soldier_button.soldier, squad.squad)
					if squad.rect.collidepoint(mouse):
						self.game_world.move_soldier(self.soldier_button.soldier, squad.squad)
			self.exit_state()

	def render(self, display):
		self.prev_state_details.render(display)
		self.floating_soldier_name_button.draw(display)
