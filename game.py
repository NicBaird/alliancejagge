import os, time, pygame, json
# Load our scenes
from states.title import Title

class Game():
		def __init__(self):
			pygame.init()
			self.GAME_W,self.GAME_H = 629, 477
			self.SCREEN_WIDTH,self.SCREEN_HEIGHT = 1258, 954
			self.game_canvas = pygame.Surface((self.GAME_W,self.GAME_H))
			self.screen = pygame.display.set_mode((self.SCREEN_WIDTH,self.SCREEN_HEIGHT))
			self.running, self.playing = True, True
			self.actions = {"left": False, "right": False, "up" : False, "down" : False, "action1" : False, "action2" : False, "start" : False, "rclick" : False, "lclick" : False}
			self.previous_actions = None
			self.mouse = (0, 0)
			self.dt, self.prev_time = 0, 0
			self.state_stack = []
			self.input_box = None
			self.load_assets()
			self.load_data()
			self.load_states()

		def game_loop(self):
			while self.playing:
				self.get_dt()
				self.get_events()
				self.update()
				self.render()

		def get_events(self):
			self.previous_actions = self.actions

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.playing = False
					self.running = False
					
					
				if self.input_box is not None:
					self.input_box.handle_event(event)
					
				if event.type == pygame.KEYUP:
					if event.key == pygame.K_a:
						self.actions['left'] = False
					if event.key == pygame.K_d:
						self.actions['right'] = False
					if event.key == pygame.K_w:
						self.actions['up'] = False
					if event.key == pygame.K_s:
						self.actions['down'] = False
					if event.key == pygame.K_p:
						self.actions['action1'] = False
					if event.key == pygame.K_o:
						self.actions['action2'] = False
					if event.key == pygame.K_RETURN:
						self.actions['enter'] = False
				
				if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
					self.actions['lclick'] = False
				if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
					self.actions['rclick'] = False
				self.mouse = ((pygame.mouse.get_pos()[0]/self.SCREEN_WIDTH)*self.GAME_W, (pygame.mouse.get_pos()[1]/self.SCREEN_HEIGHT)*self.GAME_H)
				
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.playing = False
						self.running = False
					if event.key == pygame.K_a:
						self.actions['left'] = True
					if event.key == pygame.K_d:
						self.actions['right'] = True
					if event.key == pygame.K_w:
						self.actions['up'] = True
					if event.key == pygame.K_s:
						self.actions['down'] = True
					if event.key == pygame.K_p:
						self.actions['action1'] = True
					if event.key == pygame.K_o:
						self.actions['action2'] = True    
					if event.key == pygame.K_RETURN:
						self.actions['start'] = True
						
				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					self.actions['lclick'] = True
				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
					self.actions['rclick'] = True

		def update(self):
			self.state_stack[-1].update(self.dt,self.actions, self.mouse)

		def render(self):
			self.state_stack[-1].render(self.game_canvas)
			# Render current state to the screen
			self.screen.blit(pygame.transform.scale(self.game_canvas,(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)), (0,0))
			pygame.display.flip()

		def get_dt(self):
			now = time.time()
			self.dt = now - self.prev_time
			self.prev_time = now

		def draw_text(self, surface, text, color, x, y):
			text_surface = self.font.render(text, True, color)
			#text_surface.set_colorkey((0,0,0))
			text_rect = text_surface.get_rect()
			text_rect.center = (x, y)
			surface.blit(text_surface, text_rect)

		def load_assets(self):
			# Create pointers to directories 
			self.assets_dir = os.path.join("assets")
			self.sprite_dir = os.path.join(self.assets_dir, "sprites")
			self.font_dir = os.path.join(self.assets_dir, "font")
			
			#Load Game Fonts
			self.font= pygame.font.Font(os.path.join(self.font_dir, "PressStart2P-vaV7.ttf"), 20)
			self.body_font= pygame.font.Font(os.path.join(self.font_dir, "SFPixelate.ttf"), 8)
			self.body_font= pygame.font.Font(os.path.join(self.font_dir, "SFPixelate.ttf"), 8)
			self.h1_bold_font= pygame.font.Font(os.path.join(self.font_dir, "SFPixelate-Bold.ttf"), 16)
	
		def load_data(self):
			f = open('data.json',)
			i = open('items.json',)
			self.data = json.load(f)
			self.items = json.load(i)
			f.close()
			i.close()

		def load_states(self):
			self.title_screen = Title(self)
			self.state_stack.append(self.title_screen)

		def reset_keys(self):
			for action in self.actions:
				self.actions[action] = False
				
			
if __name__ == "__main__":
	g = Game()
	while g.running:
		g.game_loop()
