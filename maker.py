import pandas, json
from objects import Soldier, Squad
from random import seed, randint, random, choice



class Maker():
	
	def __init__(self):
		cols_names = ["Quebec.Male.Firstname", "Quebec.Female.Firstname", "Quebec.Neuter.Firstname", "Quebec.Lastname", "Quebec.Nickname", "Merc.Male.Firstname", "Merc.Female.Firstname", "Merc.Neuter.Firstname", "Merc.Lastname", "Merc.Nickname"]
		self.names = pandas.read_csv("names.csv", usecols=cols_names)
		self.portrait_number = 5
		
	def MakeSquad(self, name, location, player):
		squad = {}
		squad["player"] = player
		squad["name"] = name
		squad["status"] = "idle"
		squad["x"] = location[0]
		squad["y"] = location[1]
		squad["soldiers"] = []
		return(Squad(squad))

		
	def MakeSoldiers(self, amount, faction="Quebec"):
		soldiers = []
		for person in range(0, amount):
			soldier = {}
			gender_roll = randint(1, 100)
			if gender_roll < 50:
				gender = "male"
				first_names = self.names[faction+".Male.Firstname"].dropna()
			if 49 < gender_roll < 98:
				gender = "female"
				first_names = self.names[faction+".Male.Firstname"].dropna()
			if gender_roll > 97:
				gender = "neuter"
				first_names = self.names[faction+".Neuter.Firstname"].dropna()
			last_names = self.names[faction+".Lastname"].dropna()
			nicknames = self.names[faction+".Nickname"].dropna()
			
			name_type_roll = randint(1, 100)
			only_lastname = False #2
			only_firstname = False #2
			only_nickname = False #2
			has_nickname = False #3
			if name_type_roll < 3:
				only_lastname = True #2
			if 2 < name_type_roll < 5:
				only_firstname = True #2
			if 4 < name_type_roll < 7:
				only_nickname = True #2
			if 6 < name_type_roll < 10:
				has_nickname = True #3
			if only_lastname:
				soldier["name"] = choice(last_names)
			elif only_firstname:
				soldier["name"] = choice(first_names)
			elif only_nickname:
				soldier["name"] = choice(nicknames)
			else:
				first = choice(first_names)
				last = choice(last_names)
				nickname = ''
				if has_nickname:
					nickname = choice(nicknames)
					soldier["name"] = first+" "+nickname+" "+last
				else:
					soldier["name"] = first+" "+last
			
			stats = ["agility", "strength", "marksmanship", "leadership"]
			special_stat = randint(0, 3)
			for i in range(0, len(stats)):
				stat = stats[i]
				if faction=="Quebec":
					if i == special_stat:
						soldier[stat] = randint(1, 100)
					else:
						soldier[stat] = min([randint(1, 100), randint(1, 100), randint(1, 100)])
				if faction == "Merc":
					if i == special_stat:
						soldier[stat] = max([randint(1, 100), randint(20, 100), randint(10, 100)])
						
					else:
						soldier[stat] = max([randint(1, 100), randint(1, 100)])
					if stat=="marksmanship":
						soldier[stat] += 5
						if soldier[stat]>99:
							soldier[stat] -= 15
				if faction=="Quebec":
					hp = 1
					roll_again = True
					while roll_again:
						hp_roll = randint(1, 100)-(hp*4)
						if hp_roll > 46:
							hp += 1
						else:
							roll_again = False
						soldier["health"] = hp
						soldier["hp"] = hp
					primary_weapon_options = ["combat_knife"] #"browning_hipower", "exacto_knife", "crowbar", "baseball_bat", "shovel", "pitchfork", "remington_model_788"
					primary_weapon_roll = randint(1, 100)
					if primary_weapon_roll > 60:
						soldier["primary_weapon"] = choice(primary_weapon_options)
					else:
						soldier["primary_weapon"] = 'None'
					soldier["level"] = 1
					soldier["secondary_weapon"] = 'None'
					soldier["head"] = 'None'
					soldier["torso"] = 'None'
					soldier["legs"] = 'None'
					soldier["inventory"] = ['None', 'None', 'None', 'None', 'None', 'None']
				if faction=="Merc":
					hp = 1
					roll_again = True
					while roll_again:
						hp_roll = randint(1, 100)-(hp*5)
						if hp_roll > 25:
							hp += 1
						else:
							roll_again = False
							soldier["health"] = hp
							soldier["heath_max"] = hp
					
			soldier["portrait"] = randint(0, self.portrait_number)
			
			soldiers.append(Soldier(soldier))
		
		return(soldiers)
		
	
	def MakeQuadrants(self):
		quadrants = []
		for y in range(0, 16):
			row = []
			for x in range(0, 16):
				quadrant = {}
				quadrant["x"] = x
				quadrant["y"] = y
				quadrant["location"] = (y*16)+x
				row.append(quadrant)
			quadrants.append(row)
		with open('data2.json', 'w') as f:
			json.dump({"quadrants":quadrants}, f)
			
	def MakeEnemySquad(self):
		enemy_squad = self.MakeSquad("X Squad "+str(randint(1000, 9999)), (randint(0, 15), randint(0,15)), 2)
		enemy_squad.soldiers = self.MakeSoldiers(5)
		return(enemy_squad)
		
maker = Maker()

print(maker.MakeSoldiers(3, "Quebec"))

maker.MakeQuadrants()
