import pygame, sys
from pygame.math import Vector2 as vector
from entity import Entity
from settings import * 
from minimap import Map

# from test_ import Update_fireStatus
# import threading

class Player(Entity):
	def __init__(self, pos, groups, path, collision_sprites, create_bullet, create_item, spawn,name):
		self.name = name
		self.spawn = spawn
		self.team = ""
		super().__init__(pos, groups, path, collision_sprites,create_item)
		self.create_bullet = create_bullet
		self.bullet_shot = False
		self.health = 5
		self.max_health = 5
		self.face_direction = vector(0, 0)  # New variable for facing direction
		self.last_slide_time = pygame.time.get_ticks()
		self.skill = 'gun'
		# moverment information
		self.sliding_distance = 150   # Thời gian lướt nhanh (tính bằng khoan cach man hinh)
		self.slide_cooldown = 4000   # Thời gian giữa các lần lướt nhanh (tính bằng giây)
		self.Viewing_Map = False
		self.bullet_direction = vector(0,0)
		self.command = ""

	#override
	def vulnerability_timer(self):
		if not self.is_vulnerable:
			current_time = pygame.time.get_ticks()
			if current_time - self.hit_time > 2000:
				self.is_vulnerable = True
				
	def draw_healthSceen(self, screen):
		heart_image = pygame.image.load('./p1_setup/graphics/heart/heart.png').convert_alpha()
		for i in range(self.health):
			heart_rect = pygame.Rect(i * (40 + 30), 10, 40, 40)
			screen.blit(heart_image, heart_rect)

	def draw_cooldown_skill(self, screen):
		skill_player = {'skill1': "./p1_setup/graphics/heart/heart.png", 'skill2': "./p1_setup/graphics/heart/heart.png"}
		
		# Màu viền và độ dày của viền
		border_color = (255, 255, 255)
		border_width = 3

		# Vị trí và kích thước của vòng tròn
		circle_radius = 40
		circle_spacing = 20
		# Vẽ các vòng tròn cho từng kỹ năng
		current_x = 20 + circle_radius + border_width  # Bắt đầu vị trí X của vòng tròn đầu tiên
		for skill_name, skill_path in skill_player.items():
			# Load hình ảnh cho vòng tròn
			circle_image = pygame.image.load(skill_path).convert_alpha()
			circle_image = pygame.transform.scale(circle_image, (2 * circle_radius, 2 * circle_radius))

			# Vị trí của vòng tròn
			circle_position = (current_x, WINDOW_HEIGHT - circle_radius - border_width)

			# Vẽ vòng tròn với hình ảnh và viền
			pygame.draw.circle(screen, border_color, circle_position, circle_radius + border_width)
			pygame.draw.circle(screen, (0, 0, 0), circle_position, circle_radius)
			screen.blit(circle_image, (circle_position[0] - circle_radius, circle_position[1] - circle_radius))

			# Cập nhật vị trí cho vòng tròn tiếp theo
			current_x += 2 * circle_radius + circle_spacing
			
	def draw_damege_lost(self, screen):
		if not self.is_vulnerable:
			lost_image = pygame.image.load('./p1_setup/graphics/heart/heart.png').convert_alpha()
			screen.blit(lost_image, (self.rect.centerx - WINDOW_WIDTH / 2,self.rect.centery - WINDOW_HEIGHT / 2))



	def get_status(self):
		# idle 
		if self.direction.x == 0 and self.direction.y == 0:
			self.status = self.status.split('_')[0] + '_idle'

		# attacking 
		if self.attacking:
			self.status = self.status.split('_')[0] + '_attack'
	
	def input(self):
		if not self.Viewing_Map:
			keys = pygame.key.get_pressed()
			if not self.attacking:

				if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
					self.direction.x = 1
					self.status = 'right'
				elif keys[pygame.K_LEFT]or keys[pygame.K_a]:
					self.direction.x = -1
					self.status = 'left'
				else:
					self.direction.x = 0


				if keys[pygame.K_UP]or keys[pygame.K_w]:
					self.direction.y = -1
					self.status = 'up'
				elif keys[pygame.K_DOWN]or keys[pygame.K_s]:
					self.direction.y = 1
					self.status = 'down'
				else:
					self.direction.y = 0

			mouse_buttons = pygame.mouse.get_pressed()
			if mouse_buttons[0]:
				if self.ammo > 0:
				# Thực hiện hành động bắn đạn
					self.last_shot_time = pygame.time.get_ticks()  # Ghi nhận thời điểm bắn đạn cuối cùng
					self.attacking = True
					self.frame_index = 0
					self.bullet_shot = False
					mouse_position = pygame.mouse.get_pos()
					player_center = pygame.display.get_surface().get_rect().center
					firePos = vector(mouse_position[0] - player_center[0], mouse_position[1] - player_center[1])
					magnitude = firePos.length()
					if magnitude != 0:
						normalized_vector = firePos / magnitude
						self.bullet_direction = normalized_vector
						
					else:
						self.bullet_direction = firePos

					#không cho nhân vật di chuyển
					self.direction = vector(0,0)

					#đổi hướng nhìn nhân vật sang gốc bắn
					self.status = "right" if firePos.x>0 else "left"
					# current_animation = self.animations[self.status]
				else: 
					# no ammo
					pass

			elif mouse_buttons[2]:  # nếu nhấn chuột phải
				current_time = pygame.time.get_ticks()
				if current_time - self.last_slide_time > self.slide_cooldown:
					backup_status = self.status
					# self.status = 'lurking'  # Add a new status for lurking movement
					mouse_position = pygame.mouse.get_pos()
					player_center = pygame.display.get_surface().get_rect().center
					move_direction = vector(mouse_position[0] - player_center[0], mouse_position[1] - player_center[1])
					self.direction = move_direction.normalize()  # Chỉ cần chuẩn hóa hướng, không cần tốc độ
					distance_to_move = min(self.sliding_distance, move_direction.length())  # Chọn khoảng cách ngắn nhất

					# Áp dụng độ dãn cho acceleration
					acceleration = 1
					t = min(1, distance_to_move / self.sliding_distance)  # Tính thời gian t trong khoảng [0, 1]
					eased_acceleration = acceleration * (t ** 3)  # Áp dụng độ dãn (exponential easing)

					# Sử dụng hàm lerp để di chuyển với tốc độ tăng lên
					self.pos = vector.lerp(self.pos, self.pos + self.direction * (distance_to_move * eased_acceleration), t)

					self.rect.center = round(self.pos.x), round(self.pos.y)
					self.hitbox.center = round(self.pos.x), round(self.pos.y)
					self.last_slide_time = current_time
					self.status = backup_status
			self.face_direction = self.direction

	def animate(self,dt):
		current_animation = self.animations[self.status]

		self.frame_index += 7 * dt

		if int(self.frame_index) == 2 and self.attacking and not self.bullet_shot:
			bullet_start_pos = self.rect.center + self.bullet_direction * 80		#tầm bắn đạn được xuất hiện là 80 có thể chỉnh cao hơn
			self.command = "attack"
			self.create_bullet(bullet_start_pos,self.bullet_direction)
			self.ammo -= 1  # Giảm số lượng đạn hiện có
			print(str(self.ammo)+"/"+str(self.max_ammo))
			self.bullet_shot = True
			self.shoot_sound.play()

		if self.frame_index >= len(current_animation):
			self.frame_index = 0
			if self.attacking:
				self.attacking = False

		self.image = current_animation[int(self.frame_index)]
		self.mask = pygame.mask.from_surface(self.image)
  
	def check_death(self):
		if self.health <= 0:
			pygame.quit()
			sys.exit()

	def handle_item(self, items):
		items_nearby= pygame.sprite.spritecollide(self, items, True, pygame.sprite.collide_mask)
		for item in items_nearby:
			print("nhận hiệu ứng "+item.type)
			self.health+=1
	

	def update(self,dt):
		self.command=""
		self.input()
		self.get_status()
		self.move(dt)
		self.animate(dt)
		self.blink()

		self.vulnerability_timer()
		self.check_death()

        # Cập nhật trạng thái đạn
		self.update_ammo(dt)



		