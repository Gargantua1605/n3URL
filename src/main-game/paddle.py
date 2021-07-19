import pygame
from pygame.locals import *

class Paddle():
	def __init__(self, screen_width, columns, screen_height):
		self.reset(screen_width, columns, screen_height)

	def move(self, direction, screen_width):
		# Reset movement direction
		self.direction = 0
		key = pygame.key.get_pressed()
		if direction == 'left' and self.rect.left > 0:
			self.rect.x -= self.speed
			self.direction = 1
		elif direction == 'right' and self.rect.right < screen_width:
			self.rect.x += self.speed
			self.direction = 0

	def draw(self, screen, paddle_colour, paddle_outline):
		pygame.draw.rect(screen, paddle_colour, self.rect)
		pygame.draw.rect(screen, paddle_outline, self.rect, 3)

	def reset(self, screen_width, columns, screen_height):
		# Define paddle variables
		self.height = 20
		self.width = int(screen_width / columns)
		self.x = int((screen_width / 2) - (self.width / 2))
		self.y = screen_height - (self.height * 2)
		self.speed = 10
		self.rect = Rect(self.x, self.y, self.width, self.height)
		self.direction = 0 # Track the direction the paddle is moving in
