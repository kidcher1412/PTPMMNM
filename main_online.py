import time
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
from health_bar import AmmoBar , NameBar , HealthBar
from entity import Entity

from death import Death
from test_ import HubGame
from realtime_data import Realtime_Data

from realtime_data import Realtime_Data
import firebase_admin
from firebase_admin import credentials, db

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
    def __init__(self, name, team, ipserver):
        self.name = name
        self.team = team
        self.ipserver = ipserver
        self.update_online = HubGame(self.name,self.ipserver)

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
        self.players = pygame.sprite.Group()
        self.otherNors = pygame.sprite.Group()
        self.skills = pygame.sprite.Group()
        self.health_bar = pygame.sprite.Group()
        self.ammo_bar = pygame.sprite.Group()
        self.name_bar = pygame.sprite.Group()
        self.health_bars = {}
        self.ammo_bars = {}
        self.name_bars = {}
        

        self.setup()
        self.music = pygame.mixer.Sound('p1_setup/sound/music.mp3')
        self.music.play(loops=-1)

        self.current_attack = None

        
        # Khởi tạo luồng phụ để cập nhật trạng thái trực tuyến
        self.list_player = {}
        self.list_player_command = {}


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
    def create_name_bar(self, entity: Entity):
        self.name_bars[entity] = NameBar(
            entity, self.name_bar, self.all_sprites
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
                    # self.create_name_bar(sprite)
     
        # # player bullet collision
        # if pygame.sprite.spritecollide(self.player, self.bullets, True, pygame.sprite.collide_mask):
        #     self.player.damage()

    def setup(self):
        # Tạo một thể hiện của Realtime_Data và chuyển tham chiếu của ứng dụng Firebase cho nó
        # Đường dẫn đến tệp cấu hình dịch vụ Firebase JSON
        cred = credentials.Certificate("./p1_setup/connect/connect.json")
        # Khởi tạo ứng dụng Firebase với tệp cấu hình
        firebase_app = firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://test-app-b6d6d-default-rtdb.firebaseio.com'
        })
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
        self.create_name_bar(self.player)

        self.Join_Fist()
        dataUpdate = {"name": self.name,"command": "", "pos":str(self.player.pos), "direction": str(self.player.face_direction)}
        self.update_online.send_data_command(dataUpdate)
        #lay nhung player ton tai san

        self.list_player = self.update_online.client.list_player
        self.list_player_command = self.update_online.client.list_player_command

        # print(self.list_player)
        for keyname, valPlayer in self.list_player.items():
            if not valPlayer["name"] == self.name:
                spawn_fist_other = self.spawnA if valPlayer["team"] == "A" else self.spawnB
                point = eval(self.list_player_command[valPlayer["name"]]["pos"])
                # print((point[0],point[1]))

                initOther =  OderPlayer(
                    pos= (point[0],point[1]),
                    groups=[self.all_sprites, self.players],
                    path=PATHS['player'],
                    collision_sprites=self.obstacles,
                    create_bullet=self.create_bullet ,
                    create_item=self.create_item,
                    spawn=spawn_fist_other,
                    team= valPlayer["team"],
                    name= valPlayer["name"],
                    health= valPlayer["health"]
                )
                self.create_name_bar(initOther)
                print("da sinh ra other "+ valPlayer["name"])
    def check_name_in_sprite(self, name):
        check = False
        for sprite in self.players:
            if sprite.name == name:
                check = True
                break
        return check

    def check_sprite_in_list(self):
        for sprite in self.players:
            if not sprite.name == self.name:
                check = False
                for keyname, val in self.list_player_command.items():
                        if sprite.name == keyname:
                            check = True
                            break
                if not check: sprite.kill()


    def play_state(self):
        self.player.direction.x = 0
        self.player.direction.y = 0


    #update online
    def Join_Fist(self):
        dataJoin = {
            "spawn": str(self.player.spawn),
            "name": self.player.name,
            "team": self.player.team,
            "direction": str(self.player.direction),
            "health": self.player.health,
            "is_vulnerable": self.player.is_vulnerable,
            "attacking": self.player.attacking,
            "ammo": self.player.ammo,
            "pos": str(self.player.pos),
            "bullet_direction": str(self.player.bullet_direction),
            "status": self.player.status
        }
        self.update_online.send_join(dataJoin)
    def update_online_status(self):
        # while True:

            self.Join_Fist()
            dataUpdate = {"name": self.name,"command": self.player.command, "pos":str(self.player.pos), "direction": str(self.player.face_direction)}
            self.update_online.send_data_command(dataUpdate)
                
            # Lấy danh sách người chơi từ luồng phụ
            self.list_player = self.update_online.client.list_player
            self.list_player_command = self.update_online.client.list_player_command

            # del self.list_player[self.player.name]
            # print(self.list_player)

            #cap nhat ammo
            list_ammo = []
            for ammo in self.bullets:
                list_ammo.append(ammo.create_data_socket_this_bullet(self.name))
            # print(list_ammo)

    def update_other_player_on_server(self):
        # print("==========")
        # print(self.list_player)
        # print(self.list_player_command)


        for key_username, user_data in self.list_player.items():
            if not self.check_name_in_sprite(key_username):
                spawn_fist_other = self.spawnA if user_data["team"] == "A" else self.spawnB
                point = eval(self.list_player_command[user_data["name"]]["pos"])

                initOther = OderPlayer(
                    pos= (point[0],point[1]),
                    groups=[self.all_sprites, self.players],
                    path=PATHS['player'],
                    collision_sprites=self.obstacles,
                    create_bullet=self.create_bullet ,
                    create_item=self.create_item,
                    spawn=spawn_fist_other,
                    team= user_data["team"],
                    name= user_data["name"],
                    health = user_data["health"]
                )
                self.create_name_bar(initOther)
                print("da sinh ra other "+ user_data["name"])
        for key_username, user_data in self.list_player_command.items():
            directionUpdate = eval(user_data["direction"])
            # check nguoi cho co trong Sprite khong ,=> khoi tao
            # if not self.check_name_in_sprite():
            for other_player in self.players.sprites():
                if other_player.name == key_username:
                    if not other_player.name == self.name:
                        bullet_point = eval(self.list_player[user_data["name"]]["bullet_direction"])
                        point = eval(self.list_player_command[user_data["name"]]["pos"])
                        print(vector(float(bullet_point[0]),float(bullet_point[1])))
                        other_player.update_oder_player(
                            direction= vector(directionUpdate[0],directionUpdate[1]),
                            status = self.list_player[key_username]["status"],
                            attacking = self.list_player[key_username]["attacking"],
                            bullet_direction = vector(float(bullet_point[0]),float(bullet_point[1])),
                            pos = vector(point[0],point[1]),
                            is_vulnerable = self.list_player[key_username]["is_vulnerable"]
                        )
        self.check_sprite_in_list()
    def run(self):
        MiniMap = Map(self.display_surface)
        chat = Chatting(self.display_surface,self.name, self.ipserver)
        death = Death(self.display_surface, self.ipserver)
        show_map_preview = False
        name = 'abc'
        show_chat = False
        mouse_img_normal = pygame.image.load('./p1_setup/graphics/other/mouse.png')
        mouse_img_tab = pygame.image.load('./p1_setup/graphics/map/icon_tim_kiem.png')

        while True:
            # event loop 
            if self.player.health == 0:

                caser = Realtime_Data(self.ipserver)
                caser.send_kill(self.name)
                pygame.quit()
                sys.exit()
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
                    # test hiển thị chết
                    if event.key == pygame.K_x:  # Add a death event when 'x' key is pressed
                        death.add_death(f"Player test ", f"Player test")
						# Increment player number for the next death event

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
                death.draw_death()
                chat.mini_chat(name)
                MiniMap.draw_mini_frame()
                mouse_img = mouse_img_normal

			#cap nhat trang thai tung nguoi choi khac

            # # Chạy luồng phụ để cập nhật trạng thái trực tuyến
            # if not self.online_status_thread.is_alive():
            #     self.online_status_thread = threading.Thread(target=self.update_online_status)
            #     self.online_status_thread.daemon = True
            #     self.online_status_thread.start()
            self.update_online_status()
            self.update_other_player_on_server()

			
            # print(self.list_player)
            # Kiểm tra xem đã đủ thời gian để chạy lệnh mới chưa
            # current_time = time.time()
            # if current_time - last_command_time >= self.command_interval:
            #     self.update_online_status()
            #     last_command_time = current_time
            pygame.display.update()

if __name__ == '__main__':
    # Kiểm tra xem có đủ số lượng tham số không
    if len(sys.argv) != 4:
        print("Usage: python script.py name team ipserver")
        sys.exit(1)

    # Lấy các tham số từ dòng lệnh
    param1 = sys.argv[1]
    param2 = sys.argv[2]
    param3 = sys.argv[3]

    # In ra các tham số
    print("Tham số 1:", param1)
    print("Tham số 2:", param2)
    print("Tham số 3:", param3)
    game = Game(param1,param2,param3)
    game.run()
