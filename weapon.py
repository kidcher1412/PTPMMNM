import pygame 

class Weapon(pygame.sprite.Sprite):
	def __init__(self,player,groups):
		super().__init__(groups)
		