#!/bin/env python3

import pygame
from pygame.locals import *

import numpy as np
import tensorflow as tf
import keras
from keras.models import model_from_json

from paddle import Paddle
from ball import Ball
from eeg_classifier import EEGClassifier
from wall import Wall

pygame.init()

screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Breakout')

# Background colour 
background = (234, 218, 184)

# Block colours
block_red = (245, 85, 96)
block_green = (86, 174, 87)
block_blue = (69, 177, 232)

# Paddle colours
paddle_colour = (142, 135, 123)
paddle_outline = (100, 100, 100)  

# Define the font
font = pygame.font.SysFont('Constantia', 30)

# Game variables
columns = 6
rows = 6
clock = pygame.time.Clock()
fps =45
live_ball = False # To check if the ball has gone out of the game window
game_over = 0

# Text Colour
text_colour = (78, 81, 139)

# Define the text font
font = pygame.font.SysFont('Constantia', 30)

def draw_text(text, font, text_colour, x, y):
	image = font.render(text, True, text_colour)
	screen.blit(image, (x, y))

load_left_data = np.loadtxt("../../processed-data/python-model-2/test_left_data.txt")
left_data = np.reshape(load_left_data, (load_left_data.shape[0], load_left_data.shape[1] // 10, 10))
# print(left_data.shape)
left_data = left_data.transpose(0, 2, 1)
# print(left_data.shape)

load_right_data = np.loadtxt("../../processed-data/python-model-2/test_right_data.txt")
right_data = np.reshape(load_right_data, (load_right_data.shape[0], load_right_data.shape[1] // 10, 10))
# print(right_data.shape)
right_data = right_data.transpose(0, 2, 1)
# print(right_data.shape)

# Create the wall
wall = Wall(screen_width, columns)
wall.create_wall(rows, columns)

# Create the paddle
player_paddle = Paddle(screen_width, columns, screen_height)

# Create the ball
ball = Ball(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)

# Create the EEG Classififer
model_json_file = '../../models/Deep_Conv_Net_10Channel_RestData_Excluded/Deep_Conv_Net_10Channel_model.json'
model_h5_file = '../../models/Deep_Conv_Net_10Channel_RestData_Excluded/Deep_Conv_Net_10Channel_model.h5'
classifier = EEGClassifier(model_json_file, model_h5_file)

# Parameters to plot confusion matrix
left_as_right = 0
left_as_left = 0
right_as_right = 0
right_as_left = 0

run = True
while run:
	clock.tick(fps) # Add a limit to how fast the screen updates
	screen.fill(background)

	# Draw all objects
	wall.draw_wall(block_blue, block_red, block_green, screen, background)
	player_paddle.draw(screen, paddle_colour, paddle_outline)
	ball.draw(screen, paddle_colour, paddle_outline)

	if live_ball:
		# Move the objects
		if ball.rect.x < player_paddle.rect.x:
			epoched_data = left_data[np.random.choice(left_data.shape[0])]
			# print(epoched_data.shape)
			epoched_data = epoched_data[np.newaxis, :, :, np.newaxis]
			# print(epoched_data.shape)
			prediction = classifier.classify_thought(epoched_data)
			player_paddle.move(prediction, screen_width)
			print(f"Paddle should move left but actually moves {prediction}")
			if prediction == 'left':
				left_as_left += 1
			else:
				left_as_right += 1
		elif ball.rect.x > player_paddle.rect.x:
			epoched_data = right_data[np.random.choice(right_data.shape[0])]
			# print(epoched_data.shape)
			epoched_data = epoched_data[np.newaxis, :, :, np.newaxis]
			# print(epoched_data.shape)
			prediction = classifier.classify_thought(epoched_data)
			player_paddle.move(prediction, screen_width)
			print(f"Paddle should move right but actually moves {prediction}")
			if prediction == 'right':
				right_as_right += 1
			else:
				right_as_left += 1

		game_over = ball.move(wall, screen_width, screen_height, player_paddle)
		if game_over != 0:
			live_ball = False

	# Print player instructions/state
	if not live_ball:
		if game_over == 0:
			draw_text('CLICK ANYWHERE TO START', font, text_colour, 100, screen_height // 2 + 100)
		elif game_over == 1:
			draw_text('YOU WON!', font, text_colour, 240, screen_height // 2 + 50)
			draw_text('CLICK ANYWHERE TO START', font, text_colour, 100, screen_height // 2 + 100)
		elif game_over == -1:
			draw_text('YOU LOST!', font, text_colour, 240, screen_height // 2 + 50)
			draw_text('CLICK ANYWHERE TO START', font, text_colour, 100, screen_height // 2 + 100)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

		if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False:
			live_ball = True
			ball.reset(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)
			player_paddle.reset(screen_width, columns, screen_height)
			wall.create_wall(rows, columns)

	pygame.display.update()

accuracy = (left_as_left + right_as_right) / (left_as_left + left_as_right + right_as_left + right_as_right)
print("Accuracy", accuracy)
pygame.quit()
