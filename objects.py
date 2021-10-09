import pygame, random, math

class Quadrant():
	
	def __init__(self, d):
		self.x, self.y = d["x"], d["y"]
		self.location = d["location"]
		self.wall = False
		
class Squad():
	
	def __init__(self, json_data):
		self.status = json_data["status"]
		self.player = json_data["player"]
		self.x, self.y = json_data["x"], json_data["y"]
		self.name = json_data["name"]
		self.soldiers = []
		self.load_soldiers(json_data['soldiers'])
		self.expanded = False
		
	def load_soldiers(self, json_data):
		for i in json_data:
			self.soldiers.append(Soldier(i))


class Soldier():
	def __init__(self, json_data):
		print(json_data)
		self.name = json_data['name']
		self.portrait = json_data['portrait']
		self.level = json_data['level']
		self.hp = json_data["hp"]
		self.health = json_data['health']
		self.agility = json_data['agility']
		self.strength = json_data['strength']
		self.leadership = json_data['leadership']
		self.marksmanship = json_data['marksmanship']
		
		self.primary_weapon = json_data["primary_weapon"]
		self.secondary_weapon = json_data["secondary_weapon"]
		self.head = json_data["head"]
		self.torso = json_data["torso"]
		self.legs = json_data["legs"]
		self.inventory = json_data["inventory"]	
		self.data = json_data
		

		
