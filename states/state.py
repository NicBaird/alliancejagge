class State():
	def __init__(self, game):
		self.game = game
		self.prev_state = None

	def update(self, delta_time, actions, mouse):
		pass
	def render(self, surface):
		pass

	def enter_state(self):
		if len(self.game.state_stack) > 1:
			self.prev_state = self.game.state_stack[-1]
		self.game.state_stack.append(self)

	def exit_state(self):
		self.game.state_stack.pop()


#Game World States

class ViewportState():
	def __init__(self, game_world):
		self.game_world = game_world
		self.prev_state_viewport = None
		self.x, self.y = 258, 0
		self.chartx, self.charty = self.x+30, self.y+27
	def update(self, delta_time, actions, mouse):
		pass
	def render(self, surface):
		pass

	def enter_state(self):
		if len(self.game_world.viewport_state_stack) > 0:
			self.prev_state_viewport = self.game_world.viewport_state_stack[-1]
		self.game_world.viewport_state_stack.append(self)

	def exit_state(self):
		self.game_world.viewport_state_stack.pop()

class DetailsState():
	def __init__(self, game_world):
		self.game_world = game_world
		self.prev_state_details = None
		self.x, self.y = 0, 0

	def update(self, delta_time, actions, mouse):
		pass
	def render(self, surface):
		pass

	def enter_state(self):
		if len(self.game_world.details_state_stack) > 0:
			self.prev_state_details = self.game_world.details_state_stack[-1]
		self.game_world.details_state_stack.append(self)

	def exit_state(self):
		self.game_world.details_state_stack.pop()
