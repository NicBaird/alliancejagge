import pygame as pg

pg.init()

COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pg.font.Font(None, 32)


class InputBox:

	def __init__(self, x, y, w, h, font, text=''):
		self.rect = pg.Rect(x, y, w, h)
		self.font = font
		self.color = COLOR_INACTIVE
		self.text = text
		self.txt_surface = self.font.render(text, True, self.color)
		self.active = False

	def handle_event(self, event):
		if event.type == pg.KEYDOWN:
			if self.active:
				if event.key == pg.K_BACKSPACE:
					self.text = self.text[:-1]
				else:
					self.text += event.unicode
				# Re-render the text.
				self.txt_surface = self.font.render(self.text, True, self.color)

	def return_text(self):
		text = self.text
		self.text = ''
		return(text)

	def update(self):
		self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
		# Resize the box if the text is too long.
		width = max(200, self.txt_surface.get_width()+10)
		self.rect.w = width

	def draw(self, screen):
		# Blit the text.
		screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
		# Blit the rect.
		pg.draw.rect(screen, self.color, self.rect, 2)
