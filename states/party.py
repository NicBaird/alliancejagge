import pygame, os
from states.state import State

class PartyMenu(State):
	def __init__(self, game):
		self.game = game
		State.__init__(self, game)
		self.template_img = pygame.image.load(os.path.join(self.game.assets_dir, "map", "template_map.png"))

	def update(self, delta_time, actions):
		if actions["action2"]:
			self.exit_state()
		self.game.reset_keys()

	def render(self, display):
		display.blit(self.template_img, (0,0))
		self.game.draw_text(display, "PARTY MENU GOES HERE", (0,0,0), self.game.GAME_W/2, self.game.GAME_H/2 )


