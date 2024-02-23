import pygame, sys
from pygame.math import Vector2 as vector
from settings import * 
from player import Player
import pytmx
from pytmx.util_pygame import load_pygame
from sprite import Sprite, Bullet, Item, Skill
from monster import Coffin, Cactus
import ctypes
from minimap import Map
from oderplayer import OderPlayer

# Ẩn chuột mặc định của hệ điều hành
#change test
ctypes.windll.user32.ShowCursor(False)


class AllSprites(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.offset = vector()
		self.display_surface = pygame.display.get_surface()
		self.bg = pygame.image.load('p1_setup/graphics/other/bg.png').convert()



		

	def customize_draw(self,player):

		# change the offset vector
		# self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
		# self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2
		self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
		self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2

		# blit the surfaces 
		self.display_surface.blit(self.bg,-self.offset)
		for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
			offset_rect = sprite.image.get_rect(center = sprite.rect.center)
			offset_rect.center -= self.offset
			self.display_surface.blit(sprite.image,offset_rect)

class Game:
	def __init__(self):
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		pygame.display.set_caption('Western shooter')
		self.clock = pygame.time.Clock()
		self.bullet_surf = pygame.image.load('p1_setup/graphics/other/particle.png').convert_alpha()

		#map
		self.map_data = []

		# groups 
		self.all_sprites = AllSprites()
		self.obstacles = pygame.sprite.Group()
		self.bullets = pygame.sprite.Group()
		self.items = pygame.sprite.Group()
		self.monsters = pygame.sprite.Group()
		self.skills = pygame.sprite.Group()

		self.setup()
		self.music = pygame.mixer.Sound('p1_setup/sound/music.mp3')
		self.music.play(loops = -1)

		self.current_attack = None



	def create_item(self, pos, type):
		Item(pos, type, [self.all_sprites,self.items])

	def create_bullet(self, pos, direction):
		Bullet(pos, direction, self.bullet_surf, [self.all_sprites,self.bullets])


  
	def bullet_collision(self):
		# bullet obstacle collision
		for obstacle in self.obstacles.sprites():
			pygame.sprite.spritecollide(obstacle, self.bullets, True)
   
		# bullet monster collision
		for bullet in self.bullets.sprites():
			sprites = pygame.sprite.spritecollide(bullet, self.monsters, False, pygame.sprite.collide_mask)
   
			if sprites:
				bullet.kill()
				for sprite in sprites:
					sprite.damage()
     
		# player bullet collision
		if pygame.sprite.spritecollide(self.player, self.bullets, True, pygame.sprite.collide_mask):
			self.player.damage()



	def setup(self):
		# tmx_map = load_pygame('p1_setup/map.tmx')
		tmx_map = load_pygame('p1_setup/map/map3.tmx')
		for layer in tmx_map.visible_layers:
			if isinstance(layer, pytmx.TiledTileLayer):
				self.map_data.append(layer)

			
		# tiles
		for x, y, surf in tmx_map.get_layer_by_name('Fence').tiles():
			Sprite((x * 64, y * 64),surf,[self.all_sprites, self.obstacles])

		# objects
		for obj in tmx_map.get_layer_by_name('Object'):
			Sprite((obj.x, obj.y),obj.image,[self.all_sprites, self.obstacles])

		for obj in tmx_map.get_layer_by_name('Entities'):
			if obj.name == 'Player':
				self.player = Player(
					pos = (obj.x,obj.y), 
					groups = self.all_sprites, 
					path = PATHS['player'], 
					collision_sprites = self.obstacles,
					create_bullet = self.create_bullet , 
					create_item= self.create_item)

			if obj.name == 'oder-Player':
				self.player = OderPlayer(
					pos = (obj.x,obj.y), 
					groups = self.all_sprites, 
					path = PATHS['cactus'], 
					collision_sprites = self.obstacles,
					create_bullet = self.create_bullet , 
					create_item= self.create_item)

			if obj.name == 'Coffin':
				Coffin((obj.x,obj.y), [self.all_sprites, self.monsters], PATHS['coffin'], self.obstacles, self.player, self.create_item )

			if obj.name == 'Cactus':
				Cactus((obj.x, obj.y), [self.all_sprites, self.monsters], PATHS['cactus'], self.obstacles, self.player, self.create_bullet, self.create_item)

	def run(self):
		MiniMap = Map(self.display_surface)
		show_map_preview = False
		while True:
			# event loop 
			self.player.handle_item(self.items)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
			dt = self.clock.tick() / 1000


			# update groups 
			self.all_sprites.update(dt)
			self.bullet_collision()

			# draw groups
			self.display_surface.fill('black')
			self.all_sprites.customize_draw(self.player)



			self.player.draw_healthSceen(self.display_surface)
			self.player.draw_cooldown_skill(self.display_surface)
			self.player.draw_damege_lost(self.display_surface)

			# map show
			for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()
					elif event.type == pygame.KEYDOWN:
						if event.key == pygame.K_m:
							# Hiển thị hoặc ẩn bản đồ thu nhỏ tùy thuộc vào trạng thái hiện tại
							show_map_preview = not show_map_preview
			if show_map_preview:
				MiniMap.draw_map_preview(self.map_data)


			# draw custom mouse to tageter
			mouse_x, mouse_y = pygame.mouse.get_pos()
			mouse_img = pygame.image.load('./p1_setup/graphics/other/mouse.png')
			self.display_surface.blit(mouse_img, (mouse_x - 50 // 2, mouse_y - 50 // 2))


			pygame.display.update()

if __name__ == '__main__':
	game = Game()
	game.run()