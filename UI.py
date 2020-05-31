from pygame.locals import *
from random import randint
import pygame
import time
 
def App():
	BLUE = pygame.Color(0, 0, 255)

	running = True
	pygame.display.init()

	#get display size
	display_h = pygame.display.Info().current_h
	display_w = pygame.display.Info().current_w

	logo = pygame.image.load("logo32x32.png")
	pygame.display.set_icon(logo)
	pygame.display.set_caption("minimal program")

	#create new "full-screen" window
	window = pygame.display.set_mode((display_w , display_h))

	while(running):
		window.fill((0,0,0))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.MOUSEMOTION:
				m_pos = pygame.mouse.get_pos()
				pygame.draw.circle(window, BLUE, m_pos, 10, 0)	
				pygame.display.update()
				
	
 
if __name__ == "__main__" :
	App()
