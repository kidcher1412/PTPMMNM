import pygame
import pytmx
from pytmx.util_pygame import load_pygame

class Map(pygame.sprite.Sprite):
    def __init__(self,screen):
        self.screen = screen
        self.map_preview = {
            'position': (10, 10),  # Đặt vị trí xuất hiện của bản đồ thu nhỏ
            'size': (200, 150)  # Đặt kích thước của bản đồ thu nhỏ
        }
    def draw_map_preview(self,map_data):
        # Vẽ bản đồ thu nhỏ tại vị trí và kích thước đã đặt
        map_image = pygame.image.load('./p1_setup/map.png').convert_alpha()
        self.screen.blit(map_image, self.map_preview['position'])



        
