import random
import time
import pygame
from pygame.math import Vector2 as vector
from os import walk
from math import sin
from settings import * 



class Entity(pygame.sprite.Sprite):
	def __init__(self, pos, groups, path, collision_sprites, create_item):
		super().__init__(groups)

		self.create_item = create_item
		self.import_assets(path)
		self.frame_index = 0
		self.status = 'down'

		self.image = self.animations[self.status][self.frame_index]
		self.rect = self.image.get_rect(center = pos)

		# float based movement
		self.pos = vector(self.rect.center)
		self.direction = vector()
		self.speed = 200




		# collisions
		self.hitbox = self.rect.inflate(-self.rect.width * 0.5,-self.rect.height / 2)
		self.collision_sprites = collision_sprites
		self.mask = pygame.mask.from_surface(self.image)

		# attack 
		self.attacking = False

		# health
		self.health = 3
		self.max_health = 10
		self.is_vulnerable = True
		self.hit_time = None
  
		# sound
		self.hit_sound = pygame.mixer.Sound('p1_setup/sound/hit.mp3')
		self.hit_sound.set_volume(0.2)
		self.shoot_sound = pygame.mixer.Sound('p1_setup/sound/bullet.wav')
		self.shoot_sound.set_volume(0.3)

	def blink(self):
		if not self.is_vulnerable:
			if self.wave_value():
				mask = pygame.mask.from_surface(self.image)
				white_surf = mask.to_surface()
				white_surf.set_colorkey((0,0,0)) # remove all black pixels from mask
				self.image = white_surf
			
	# def draw_damege_lost(self, screen):
	# 	if not self.is_vulnerable:
	# 		lost_image = pygame.image.load('./p1_setup/graphics/heart/heart.png').convert_alpha()
	# 		screen.blit(lost_image, (self.rect.centerx - lost_image.get_width() // 2, self.rect.top - 10))


	def wave_value(self):
		value = sin(pygame.time.get_ticks())
		if value >= 0:
			return True
		else:
			return False


	def damage(self):
		if self.is_vulnerable:
			self.health -= 1
			self.is_vulnerable = False
			self.hit_time = pygame.time.get_ticks()
			self.hit_sound.play()
   
	def check_death(self):
		if self.health <= 0:
			self.kill()
			item_types = ['increase_damage', 'heal','money']  # Các loại vật phẩm
			item_type = random.choice(item_types)  # Chọn ngẫu nhiên một loại vật phẩm
			self.create_item(self.pos, item_type)

	def draw_health(self):
		health_bar_length = 20
		health_bar_height = 10
		health_bar_color = (0, 255, 0)
		health_percentage = self.health / self.max_health
		health_bar_width = int(health_bar_length * health_percentage)
		
		# Tính toán vị trí để vẽ thanh máu dựa trên tọa độ thế giới
		health_bar_pos = (self.pos.x - health_bar_length // 2, self.pos.y - 10)

		# Tạo một Surface mới để vẽ thanh máu 
		health_bar_surface = pygame.Surface((health_bar_length, health_bar_height), pygame.SRCALPHA)
		pygame.draw.rect(health_bar_surface, (255, 255, 255), (0, 0, health_bar_length, health_bar_height))
		pygame.draw.rect(health_bar_surface, health_bar_color, (0, 0, health_bar_width, health_bar_height))

		# Vẽ thanh máu lên hình ảnh và hitbox của quái
		self.image.blit(health_bar_surface, (health_bar_pos[0] - self.rect.left, health_bar_pos[1] - self.rect.top))
		self.hitbox = self.rect.inflate(-self.rect.width * 0.5, -self.rect.height / 2)
			




	def vulnerability_timer(self):
		if not self.is_vulnerable:
			current_time = pygame.time.get_ticks()
			if current_time - self.hit_time > 1500:
				self.is_vulnerable = True
		

	def import_assets(self,path):
		self.animations = {}

		for index,folder in enumerate(walk(path)):
			if index == 0:
				for name in folder[1]:
					self.animations[name] = []
			else:
				for file_name in sorted(folder[2], key = lambda string: int(string.split('.')[0])):
					path = folder[0].replace('\\','/') + '/' + file_name
					surf = pygame.image.load(path).convert_alpha()
					key = folder[0].split('\\')[-1]
					self.animations[key].append(surf)

	def move(self,dt):
		# normalize 
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()

		# horiztonal movement
		self.pos.x += self.direction.x * self.speed * dt
		self.hitbox.centerx = round(self.pos.x)
		self.rect.centerx = self.hitbox.centerx
		self.collision('horizontal')

		# vertical movement
		self.pos.y += self.direction.y * self.speed * dt
		self.hitbox.centery = round(self.pos.y)
		self.rect.centery = self.hitbox.centery
		self.collision('vertical')

	def collision(self,direction):
		for sprite in self.collision_sprites.sprites():
			if sprite.hitbox.colliderect(self.hitbox):
				if direction == 'horizontal':
					if self.direction.x > 0: # moving right 
						self.hitbox.right = sprite.hitbox.left
					if self.direction.x < 0: # moving left
						self.hitbox.left = sprite.hitbox.right
					self.rect.centerx = self.hitbox.centerx
					self.pos.x = self.hitbox.centerx

				else: # vertical
					if self.direction.y > 0: # moving down
						self.hitbox.bottom = sprite.hitbox.top
					if self.direction.y < 0: # moving up
						self.hitbox.top = sprite.hitbox.bottom
					self.rect.centery = self.hitbox.centery
					self.pos.y = self.hitbox.centery

