import pygame, sys
from pygame.math import Vector2 as vector
from entity import Entity
from settings import * 


class OderPlayer(Entity):
	def __init__(self, pos, groups, path, collision_sprites, create_bullet, create_item, spawn,team, name):
		self.spawn = spawn
		self.team = team
		self.name = name
		super().__init__(pos, groups, path, collision_sprites,create_item)
		self.create_bullet = create_bullet
		self.bullet_shot = False
		self.health = 5
		self.max_health = 5
		self.face_direction = vector(0, 0)  # New variable for facing direction
		self.direction = vector(0, 0)  # New variable for facing direction

		self.last_slide_time = pygame.time.get_ticks()
		self.skill = 'gun'
		
		# moverment information
		self.sliding_distance = 150   # Thời gian lướt nhanh (tính bằng khoan cach man hinh)
		self.slide_cooldown = 4000   # Thời gian giữa các lần lướt nhanh (tính bằng giây)




	def get_status(self):
		# idle 
		if self.direction.x == 0 and self.direction.y == 0:
			self.status = self.status.split('_')[0] + '_idle'

		# attacking 
		if self.attacking:
			self.status = self.status.split('_')[0] + '_attack'

	def update_oder_player(self, direction, status, attacking, bullet_direction, pos , is_vulnerable):
		# self.attacking = newdata.attacking
		self.direction = direction
		self.status = status
		if not self.attacking == attacking:
			self.frame_index = 0
			self.bullet_shot = False
		self.attacking = attacking
		self.bullet_direction = bullet_direction
		self.pos = pos
		self.is_vulnerable = is_vulnerable

		# self.status = newdata.status
		# self.health = newdata.health
		# self.attacking = newdata.attacking
		# self.status = newdata
	#overright
	def move(self,dt):
		# normalize 
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()

		# horiztonal movement
		self.hitbox.centerx = round(self.pos.x)
		self.rect.centerx = self.hitbox.centerx
		self.collision('horizontal')

		# vertical movement
		self.hitbox.centery = round(self.pos.y)
		self.rect.centery = self.hitbox.centery
		self.collision('vertical')

	def animate(self,dt):
		current_animation = self.animations[self.status]

		self.frame_index += 7 * dt

		if int(self.frame_index) == 2 and self.attacking and not self.bullet_shot:
			bullet_start_pos = self.rect.center + self.bullet_direction * 80		#tầm bắn đạn được xuất hiện là 80 có thể chỉnh cao hơn
			self.create_bullet(bullet_start_pos,self.bullet_direction)
			self.bullet_shot = True
			self.shoot_sound.play()

		if self.frame_index >= len(current_animation):
			self.frame_index = 0
			if self.attacking:
				self.attacking = False

		self.image = current_animation[int(self.frame_index)]
		self.mask = pygame.mask.from_surface(self.image)
  


	def handle_item(self, items):
		items_nearby= pygame.sprite.spritecollide(self, items, True, pygame.sprite.collide_mask)
		for item in items_nearby:
			print("nhận hiệu ứng "+item.type)
			self.health+=1
			
	def update(self,dt):
		self.get_status()
		self.move(dt)
		self.animate(dt)
		self.blink()
		#hàm cập nhật nhân vật người chơi khác bên ngoài main
		self.check_death()



		