from sys import exit as sys_exit
from os import getcwd as os_getcwd
from os import makedirs as os_mkdirs
from os.path import join as os_join

import pygame, pygame.freetype

class Game:
	def __init__(self):
		# Initialize backend variables and modules
		pygame.init()
		self.display = pygame.display.set_mode((800, 600))
		pygame.display.set_caption('MarioPy')
		self.font = pygame.freetype.SysFont('Arial', 30)
		self.clock = pygame.time.Clock()
		self.dt = 0
		self.game_state = 0

		# Load or Create saves file and initialize saves variables
		try:
			self.saves_file = open(os_join(os_getcwd(), 'saves'), 'r+')
			self.saves_data = bytes.fromhex(self.saves_file.read()).decode('utf-8').split('.')
			if self.saves_data[0] == '':
				self.saves_data = []
			else:
				self.saves_data.pop(len(self.saves_data) - 1)
		except:
			saves_file = open(os_join(os_getcwd(), 'saves'), 'w+')
			saves_file.close()
			self.saves_file = open(os_join(os_getcwd(), 'saves'), 'r+')
			self.saves_data = []
		self.game_save_file = None
		self.game_save_data = []
		os_mkdirs(os_join(os_getcwd(), 'save_files'), exist_ok = True)

	def update(self):
		self.handle_events()

	def render(self):
		self.display.fill((0, 0, 0))

		pygame.display.flip()

	def run(self):
		while True:
			self.update()
			self.render()
			self.dt = self.clock.tick(60) / 1000

	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.saves_file.close()
				if self.game_save_file != None: self.game_save_file.close()
				pygame.quit()
				sys_exit()

	def save_saves_file(self):
		self.saves_file.seek(0)
		for save in self.saves_data:
			self.saves_file.write((save + '.').encode('utf-8').hex())
		self.saves_file.truncate()

	def load_new_game_save(self, save_name):
		for save in self.saves_data:
			if save == save_name:
				return False
		game_save_file = open(os_join(os_getcwd(), 'save_files', save_name.encode('utf-8').hex()), 'w+')
		game_save_file.close()
		self.game_save_file = open(os_join(os_getcwd(), 'save_files', save_name.encode('utf-8').hex()), 'r+')
		self.game_save_data = [ '0', '0' ]
		self.saves_data.append(save_name)
		self.save_saves_file()
		self.save_game_save_file()


	def load_game_save_file(self, save_name):
		try:
			self.game_save_file = open(os_join(os_getcwd(), 'save_files', save_name.encode('utf-8').hex()), 'r+')
			self.game_save_data = bytes.fromhex(self.game_save_file.read()).decode('utf-8').split('.')
			self.game_save_data.pop(len(self.game_save_data) - 1)
		except:
			return False
		return True

	def save_game_save_file(self):
		self.game_save_file.seek(0)
		for data in self.game_save_data:
			self.game_save_file.write((data + '.').encode('utf-8').hex())
		self.game_save_file.truncate()

if __name__ == '__main__':
	game = Game()
	game.run()