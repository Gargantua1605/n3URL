import pygame
from pygame.locals import *

#The Ball Class
class Ball:
	def __init__(self, x, y):
		self.reset(x, y)

	def move(self, wall, screen_width, screen_height, player_paddle):

		collision_threshold = 5

		# Start off with the assumption that the wall has been destroyed completely
		wall_destroyed = 1
		row_counter = 0
		for row in wall.blocks:
			item_counter = 0
			for item in row:
				# Check for collision with each block in the wall
				if self.rect.colliderect(item[0]):
					# Check if collision is from above
					if abs(self.rect.bottom - item[0].top) < collision_threshold and self.velocity_y > 0:
						self.velocity_y *= -1
					# Check if collision is from below
					if abs(self.rect.top - item[0].bottom) < collision_threshold and self.velocity_y < 0:
						self.velocity_y *= -1
					# Check if collision is from left
					if abs(self.rect.right - item[0].left) < collision_threshold and self.velocity_x > 0:
						self.velocity_x *= -1
					# Check if collision is from right
					if abs(self.rect.left - item[0].right) < collision_threshold and self.velocity_x < 0:
						self.velocity_x *= -1
					# We also reduce the block strength by colliding with it
					if wall.blocks[row_counter][item_counter][1] > 1:
						wall.blocks[row_counter][item_counter][1] -= 1
					else:
						wall.blocks[row_counter][item_counter][0] = (0, 0, 0, 0)

				# Check if block still exists, in which case the wall is not destroyed
				if wall.blocks[row_counter][item_counter][0] != (0, 0, 0, 0):
					wall_destroyed = 0
				# increase the item counter
				item_counter += 1

			# increase the row counter, having completed the entire row
			row_counter += 1

		# After iterating through all the blocks, check if the wall is destroyed
		if wall_destroyed == 1:
			self.game_over = 1 # The player has won, rather than lost

		# Check for collision with the walls
		if self.rect.left < 0 or self.rect.right > screen_width:
			self.velocity_x *= -1

		# Check for the collision with the top and bottom
		if self.rect.top < 0:
			self.velocity_y *= -1

		# If the paddle misses the ball, the game should end
		if self.rect.bottom > screen_height:
			self.game_over = -1

		# Check for collision with the player paddle
		if self.rect.colliderect(player_paddle):
			# Check for collision from the top of the paddle
			if abs(self.rect.bottom - player_paddle.rect.top) < collision_threshold and self.velocity_y > 0:
				self.velocity_y *= -1
				self.velocity_x += player_paddle.direction
				if self.velocity_x > self.maximum_speed:
					self.velocity_x = self.maximum_speed
				elif self.velocity_x < 0 and self.velocity_x < -self.maximum_speed:
					self.velocity_x = -self.maximum_speed
			else:
				self.velocity_x *= -1


		self.rect.x += self.velocity_x
		self.rect.y += self.velocity_y

		return self.game_over

	def draw(self, screen, paddle_colour, paddle_outline):
		pygame.draw.circle(screen, paddle_colour, (self.rect.x + self.radius, self.rect.y + self.radius), self.radius)
		pygame.draw.circle(screen, paddle_outline, (self.rect.x + self.radius, self.rect.y + self.radius), self.radius, 3)

	def reset(self, x, y):
		self.radius = 10
		self.x = x - self.radius
		self.y = y
		self.rect = Rect(self.x, self.y, self.radius * 2, self.radius * 2)
		self.velocity_x = 4
		self.velocity_y = -4
		self.maximum_speed = 5
		self.game_over = 0
