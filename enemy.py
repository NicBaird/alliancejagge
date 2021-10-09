from objects import Squad
from pathing import Node, astar
from random import randint

class Enemy():
	
	def __init__(self, game_world):
		self.game_world = game_world
	
	def take_turn(self):
		for squad in self.game_world.squads:
			if squad.player == 2:
				self.random_patrol(squad)
	
	def random_patrol(self, squad):
		if squad.status == "idle":
			random_quadrant = (randint(0, 15), randint(0, 15))
			self.game_world.move_squad(squad, astar(self.game_world.quadrants, (squad.x, squad.y), random_quadrant)[-1])
