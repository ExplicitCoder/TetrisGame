import pygame
import random
from pprint import pprint

SCREEN = WIDTH, HEIGHT = 300, 500
CELL = 20
ROWS, COLS = (HEIGHT - 100) // CELL, WIDTH // CELL
print(ROWS, COLS)

# colors
BLACK = (124, 145, 111)
WHITE = (255, 255, 255)

class Tetraminos:
	def __init__(self, matrix):
		self.matrix = matrix
		self.on_tetris = False
		self.is_dead = False

		O = [[1,1],
			 [1,1]]

		I1 = [[1],
			 [1],
			 [1],
			 [1]]

		I2 = [[1, 1, 1, 1]]

		J = [[0,1],
			 [0,1],
			 [1,1]]

		L = [[1,0],
			 [1,0],
			 [1,1]]

		S = [[0,1,1],
			 [1,1,0]]

		T = [[1,1,1],
			 [0,1,0]]

		Z = [[1,1,0],
			 [0,1,1]]

		self.shape = random.choice([O,I1,I2,J,L,S,T,Z])
		self.width = len(self.shape[0])
		self.height = len(self.shape)
		self.x = random.randint(0,COLS-self.width)
		self.y = 0
		self.color = random.randint(1,4)

	def create_tetramino(self):
		self.draw_grid()

	def move_left(self):
		move_left = False
		if self.x > 0:
			for y in range(self.height):
				if self.shape[y][0] == 1:
					if self.matrix[self.y + y][self.x - 1] != 0:
						break
			else:
				move_left = True

		if move_left:
			self.erase_grid()
			self.x -= 1
			self.draw_grid()

	def move_right(self):
		move_right = False
		if self.x < COLS - self.width:
			for y in range(self.height):
				if self.shape[y][self.width-1] == 1:
					if self.matrix[self.y + y][self.x + self.width] != 0:
						break
			else:
				move_right = True

		if move_right:
			self.erase_grid()
			self.x += 1
			self.draw_grid()

	def move_down(self):
		if self.can_move_down():
			self.erase_grid()
			self.y += 1
			self.draw_grid()

	def can_move_down(self):
		move_down = False
		if self.y < ROWS - self.height:
			for x in range(self.width):
				r, c = self.y+self.height, self.x + x
				if self.shape[self.height-1][x] == 1:
					if self.matrix[r][c] != 0:
						self.on_tetris = True
						move_down = False
						break
				else:
					if self.matrix[r][c] != 0:
						self.on_tetris = True
			else:
				move_down = True
		else:
			self.on_tetris = True

		if self.on_tetris and self.y == 0:
			self.is_dead = True

		return move_down

	def rotate_shape(self):
		rotated = list(zip(*self.shape[::-1]))
		if self.x + len(rotated[0]) < COLS:
			self.erase_grid()
			self.shape = rotated
			self.width = len(self.shape[0])
			self.height = len(self.shape)
			self.draw_grid()

	def draw_grid(self):
		for y in range(self.height):
			for x in range(self.width):
				r, c = self.y+y, self.x+x
				if self.shape[y][x] == 1:
					self.matrix[r][c] = self.color

	def erase_grid(self):
		for y in range(self.height):
			for x in range(self.width):
				r, c = self.y + y, self.x + x
				if self.shape[y][x] == 1:
					self.matrix[r][c] = 0

class Button(pygame.sprite.Sprite):
	def __init__(self, img, scale, x, y):
		super(Button, self).__init__()

		self.image = pygame.transform.scale(img, scale)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		self.clicked = False

	def draw(self, win, image=None):
		if image:
			self.image = image
		action = False
		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] and not self.clicked:
				action = True
				self.clicked = True

			if not pygame.mouse.get_pressed()[0]:
				self.clicked = False

		win.blit(self.image, self.rect)
		return action
		

def draw_grid(win):
		for i in range(ROWS + 1):
			pygame.draw.line(win, WHITE, (0, CELL * i), (WIDTH, CELL * i))
		for i in range(COLS):
			pygame.draw.line(win, WHITE, (CELL * i, 0), (CELL * i, HEIGHT - 100))
