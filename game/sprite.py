import pygame

class Sprite(pygame.sprite.Sprite):
	def __init__(self, pos, surf, groups):
		super().__init__(groups)
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0,-self.rect.height / 3)
  
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=pos)
        self.start_pos = pos
        
        # float based movement
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = direction
        self.speed = 350
        
        # track distance traveled
        self.distance_traveled = 0
        self.max_distance = 700  # max distance bullet can travel
        
    def create_data_socket_this_bullet(self, name):
         return_val=  {
              "playername": name,
              "pos_start": str(self.start_pos),
              "pos":str(self.pos),                          #make data [x,y]
              "direction": str(self.direction),             #make data [x,y]
              "distance_traveled": self.distance_traveled
         }
         return return_val
    def update(self, dt):
        # calculate distance moved this frame
        distance_moved = self.speed * dt
        self.distance_traveled += distance_moved
        
        # move the bullet
        self.pos += self.direction * distance_moved
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        
        # check if bullet has traveled max distance
        if self.distance_traveled >= self.max_distance:
            self.kill()  # remove bullet from sprite groups

  
class Item(pygame.sprite.Sprite):
    def __init__(self, pos, type , groups):
        super().__init__(groups)
        self.type = type  # Loại của vật phẩm (ví dụ: 'increase_damage', 'heal')
        print("đã rơi ra vật phâm "+type)
        self.image = self.load_image(type)  # Gán hình ảnh dựa trên tên
        self.rect = self.image.get_rect(center=pos)
        



    def load_image(self, type):
        # Ánh xạ giữa tên vật phẩm và đường dẫn đến hình ảnh
        item_images = {
            'increase_damage': 'p1_setup/graphics/item/0.png',
            'heal': 'p1_setup/graphics/item/1.png',
            'money': 'p1_setup/graphics/item/1.png',
            # Thêm các loại vật phẩm khác nếu cần
        }

        # Kiểm tra xem type có trong item_images không
        if type in item_images:
            return pygame.image.load(item_images[type]).convert_alpha()
        else:
            # Trả về một hình ảnh mặc định nếu không tìm thấy
            return pygame.Surface((20, 20))
        
    def handle_interaction(self, player):
        # Xử lý tương tác với người chơi tại đây
        if self.type == 'increase_damage':
            player.increase_damage_effect()
        elif self.type == 'heal':
            player.heal_effect()
        # Thêm các tùy chọn xử lý khác nếu cần
        self.kill()  # Xóa item sau khi tương tác


class Skill(pygame.sprite.Sprite):
	def __init__(self,player,groups):
          super().__init__(groups)
          full_path = f'./p1_setup/graphics/skill/{player.skill}.png'
          self.image = pygame.image.load(full_path).convert_alpha()
          self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0,16))
        