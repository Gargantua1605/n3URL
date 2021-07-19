import pygame
from pygame.locals import *

# Brick wall class
class Wall():
	def __init__(self, screen_width, columns):
		self.width = screen_width // columns
		self.height = 50

	def create_wall(self, rows, columns):
		self.blocks = []

		# Define an empty list for an individual block 
		block_individual = []
		for row in range(rows):
			# Reset the block row list
			block_row = []

			# Iterate through each column in that row
			for column in range(columns):
				# Generate x and y positions from each block to create the rectangle
				block_x = column * self.width 
				block_y = row * self.height
				rect = pygame.Rect(block_x, block_y, self.width, self.height)

				# Assign block strength based on row
				if row < 2:
					strength = 3
				elif row < 4:
					strength = 2
				elif row < 6:
					strength = 1

				# Create a list to store the rectangle and colour the data
				block_individual = [rect, strength]

				# Append that individual block to the block row
				block_row.append(block_individual)

			# Append the row to the full list of blocks
			self.blocks.append(block_row)


	def draw_wall(self, block_blue, block_red, block_green, screen, background):
		for row in self.blocks:
			for block in row:
				# Assign a colour based on block strength
				if block[1] == 3:
					block_colour = block_blue  
				elif block[1] == 2:
					block_colour = block_green
				elif block[1] == 1:
					block_colour = block_red


				pygame.draw.rect(screen, block_colour, block[0])
				pygame.draw.rect(screen, background, block[0], 2)
