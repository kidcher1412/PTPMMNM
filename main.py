import pygame
import sys
import threading
from pygame.math import Vector2 as vector
from settings import * 
from player import Player
import pytmx
from pytmx.util_pygame import load_pygame
from sprite import Sprite, Bullet, Item
from monster import Coffin, Cactus
from minimap import Map
from oderplayer import OderPlayer
from chatting import Chatting
from health_bar import HealthBar
from health_bar import AmmoBar
from entity import Entity
from test_ import Update_fireStatus


# Ẩn chuột mặc định của hệ điều hành
#change test
# ctypes.windll.user32.ShowCursor(False)


class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = vector()
        self.display_surface = pygame.display.get_surface()
        self.bg = pygame.image.load('p1_setup/graphics/other/bg.png').convert()

    def customize_draw(self, player):
        # change the offset vector
        self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2

        # blit the surfaces 
        self.display_surface.blit(self.bg, -self.offset)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_rect = sprite.image.get_rect(center=sprite.rect.center)
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Western shooter')
        self.clock = pygame.time.Clock()
        self.bullet_surf = pygame.image.load('p1_setup/graphics/other/particle.png').convert_alpha()
        self.name = "test"



        #map
        self.map_data = []

        # groups 
        self.all_sprites = AllSprites()
        self.obstacles = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.otherNors = pygame.sprite.Group()
        self.skills = pygame.sprite.Group()
        self.health_bar = pygame.sprite.Group()
        self.ammo_bar = pygame.sprite.Group()

        self.team = "B"
        
        self.update_online = Update_fireStatus(self.name)
        self.list_player = self.update_online.get_all_players(self.name)
        self.setup()
        self.music = pygame.mixer.Sound('p1_setup/sound/music.mp3')
        self.music.play(loops=-1)

        self.current_attack = None
        self.health_bars = {}
        self.ammo_bars = {}
        
        # Khởi tạo luồng phụ để cập nhật trạng thái trực tuyến
        self.online_status_thread = threading.Thread(target=self.update_online_status)
        self.online_status_thread.daemon = True
        self.online_status_thread.start()

    def create_item(self, pos, type):
        Item(pos, type, [self.all_sprites, self.items])

    def create_bullet(self, pos, direction):
        Bullet(pos, direction, self.bullet_surf, [self.all_sprites, self.bullets])

    def create_health_bar(self, entity: Entity):
        if entity in self.health_bars and self.health_bars[entity].alive():
            self.health_bars[entity].keep_alive()
            return
        self.health_bars[entity] = HealthBar(
            entity, self.health_bar, self.all_sprites
        )

    def create_ammo_bar(self, entity: Entity):
        if entity in self.ammo_bars and self.ammo_bars[entity].alive():
            self.ammo_bars[entity].keep_alive()
            return
        self.ammo_bars[entity] = AmmoBar(
            entity, self.ammo_bar, self.all_sprites
        )

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
                    self.create_health_bar(sprite)
                    
            # player bullet collision
            sprites = pygame.sprite.spritecollide(bullet, self.players, False, pygame.sprite.collide_mask)
            if sprites:
                bullet.kill()
                for sprite in sprites:
                    sprite.damage()
                    self.create_health_bar(sprite)
     
        # # player bullet collision
        # if pygame.sprite.spritecollide(self.player, self.bullets, True, pygame.sprite.collide_mask):
        #     self.player.damage()

    def setup(self):
        tmx_map = load_pygame('p1_setup/map/map5.tmx')
        for layer in tmx_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                self.map_data.append(layer)

        # tiles
        for x, y, surf in tmx_map.get_layer_by_name('Fence').tiles():
            Sprite((x * 64, y * 64), surf, [self.all_sprites, self.obstacles])	

        # objects
        for obj in tmx_map.get_layer_by_name('Object'):
            Sprite((obj.x, obj.y), obj.image, [self.all_sprites, self.obstacles])

        #spaw player
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player-A': self.spawnA = (obj.x, obj.y)
            if obj.name == 'Player-B': self.spawnB = (obj.x, obj.y)

            if obj.name == 'Coffin':
                Coffin((obj.x, obj.y), [self.all_sprites, self.monsters], PATHS['coffin'], self.obstacles, self.player, self.create_item )

            if obj.name == 'Cactus':
                Cactus((obj.x, obj.y), [self.all_sprites, self.monsters], PATHS['cactus'], self.obstacles, self.player, self.create_bullet, self.create_item)
        
        #init player
        spawn_fist = self.spawnA if self.team == "A" else self.spawnB
        self.player = Player(
            pos=spawn_fist, 
            groups=[self.all_sprites, self.players], 
            path=PATHS['player'], 
            collision_sprites=self.obstacles,
            create_bullet=self.create_bullet , 
            create_item=self.create_item,
            spawn=spawn_fist,
            name= self.name
        )
        self.player.team = self.team
        self.player.name = self.name
        
        
		#init other player
        for key_username,other_player_data in self.list_player.items():
        #   print(str(other_player_data))
          spawn_fist_other = self.spawnA if other_player_data["team"] == "A" else self.spawnB
          print(spawn_fist_other)
          OderPlayer(
              pos=spawn_fist_other,
              groups=[self.all_sprites, self.players],
              path=PATHS['player'],
              collision_sprites=self.obstacles,
              create_bullet=self.create_bullet ,
              create_item=self.create_item,
              spawn=spawn_fist,
              team= other_player_data["team"],
              name= key_username
		  )
          



    def play_state(self):
        self.player.direction.x = 0
        self.player.direction.y = 0

    #update online
    def update_online_status(self):
        while True:
            dataUpdate = {
                "spawn": str(self.player.spawn),
                "name": self.player.name,
                "team": self.player.team,
                "direction": str(self.player.direction),
                "health": self.player.health,
                "is_vulnerable": self.player.is_vulnerable,
                "attacking": self.player.attacking,
                "ammo": self.player.ammo,
                "Pos": str(self.player.pos),
                "bullet_direction": str(self.player.bullet_direction),
                "status": self.player.status
            }
            self.update_online.update_player_status(dataUpdate)
            # Lấy danh sách người chơi từ luồng phụ
            self.list_player = self.update_online.get_all_players(self.player.name)
            # del self.list_player[self.player.name]
            # print(self.list_player)
            

    def update_other_player_on_server(self):
        for key_username, user_data in self.list_player.items():
            for other_player in self.players.sprites():
                if other_player.name == key_username:
                    other_player.update_oder_player(
                        user_data["status"]
					)

    def run(self):
        MiniMap = Map(self.display_surface)
        chat = Chatting(self.display_surface)
        show_map_preview = False
        name = 'abc'
        show_chat = False
        mouse_img_normal = pygame.image.load('./p1_setup/graphics/other/mouse.png')
        mouse_img_tab = pygame.image.load('./p1_setup/graphics/map/icon_tim_kiem.png')
        while True:
            # event loop 
            self.player.handle_item(self.items)
            dt = self.clock.tick() / 1000

            # update groups 
            self.all_sprites.update(dt)
            self.bullet_collision()
            if self.player.ammo == 0:
                self.create_ammo_bar(self.player)

            # draw groups
            self.display_surface.fill('black')
            self.all_sprites.customize_draw(self.player)

            if not self.player.Viewing_Map:
                self.player.draw_healthSceen(self.display_surface)
                self.player.draw_cooldown_skill(self.display_surface)
                self.play_state()
            self.player.draw_damege_lost(self.display_surface)

            MiniMap.update_dot_position(self.player.pos)
            # map show
            for event in pygame.event.get():
                #sự kiện nhập input
                if show_chat:
                    chat.handle_events(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                elif event.type == pygame.KEYDOWN:
                    if not show_chat:
                        if event.key == pygame.K_TAB:
                            self.player.Viewing_Map = not self.player.Viewing_Map
                            show_map_preview = not show_map_preview
                    if not show_map_preview:
                        if event.key == pygame.K_RETURN:
                            show_chat = True
                            self.player.Viewing_Map = True
                        elif event.key == pygame.K_ESCAPE:
                            show_chat = False
                            self.player.Viewing_Map = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.player.Viewing_Map:								
                        MiniMap.handle_zoom(event)

            if show_chat:
                chat.show_chat(name)
            elif self.player.Viewing_Map:
                MiniMap.draw_map_preview(self.map_data)
                mouse_img = mouse_img_tab
            else:
                chat.mini_chat(name)
                MiniMap.draw_mini_frame()
                mouse_img = mouse_img_normal

            # # Chạy luồng phụ để cập nhật trạng thái trực tuyến
            if not self.online_status_thread.is_alive():
                self.online_status_thread = threading.Thread(target=self.update_online_status)
                self.online_status_thread.daemon = True
                self.online_status_thread.start()
            self.update_other_player_on_server()
			#cap nhat trang thai tung nguoi choi khac

			
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()
