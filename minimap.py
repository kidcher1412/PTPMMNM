import pygame

class Map(pygame.sprite.Sprite):
    def __init__(self, screen):
        self.screen = screen
        self.map_preview = {
            'size': (980, 720)
        }
        self.zoom_factor = 1.0
        self.min_zoom = 0.5
        self.max_zoom = 2.0
        
        # Phông dưới ảnh
        self.background_color = (50, 50, 50)
        # Tạo điểm tại tọa độ (x, y)
        # 1945, 1514
        self.dot_position = (486, 378)

    def draw_map_preview(self, map_data):
        # Lấy kích thước ảnh gốc
        original_image = pygame.image.load('./p1_setup/map.png').convert_alpha()
        original_size = original_image.get_rect().size

        # Thay đổi kích thước ảnh theo mức độ zoom
        zoomed_size = (int(original_size[0] * self.zoom_factor), int(original_size[1] * self.zoom_factor))
        zoomed_image = pygame.transform.scale(original_image, zoomed_size)

         # Tính toán vị trí để đưa ảnh vào giữa màn hình
        image_position = ((self.screen.get_width() - zoomed_size[0]) // 2, (self.screen.get_height() - zoomed_size[1]) // 2)
        background_rect = pygame.Rect((0, 0), self.map_preview['size'])
        background_rect.topleft = ((self.screen.get_width() - self.map_preview['size'][0]) // 2, (self.screen.get_height() - self.map_preview['size'][1]) // 2)

        # Vẽ phông dưới ảnh
        pygame.draw.rect(self.screen, self.background_color, background_rect)

        # Giới hạn phạm vi vẽ của ảnh bằng background_rect
        self.screen.set_clip(background_rect)

        # Vẽ ảnh đã zoom
        self.screen.blit(zoomed_image, image_position)

        # Tính toán vị trí mới của chấm
        dot_position_on_screen = (self.dot_position[0] * self.zoom_factor + image_position[0],
                                self.dot_position[1] * self.zoom_factor + image_position[1])

        # Vẽ chấm tại tọa độ dot_position
        pygame.draw.circle(self.screen, (255, 0, 0), (int(dot_position_on_screen[0]), int(dot_position_on_screen[1])), 5)

        # Trả lại phạm vi vẽ ban đầu
        self.screen.set_clip(None)

        # Vẽ khung
        pygame.draw.rect(self.screen, (0, 0, 0), background_rect, 10)
        icon_image = pygame.image.load('./p1_setup/graphics/map/icon_xoa.png').convert_alpha()

        icon_position = (background_rect.right - icon_image.get_width(), background_rect.top)
        self.screen.blit(icon_image, icon_position)
    
    def handle_zoom(self, event):
        # Xử lý sự kiện zoom
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:  # Lăn lên
            self.zoom_factor = min(self.max_zoom, self.zoom_factor + 0.1)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:  # Lăn xuống
            self.zoom_factor = max(self.min_zoom, self.zoom_factor - 0.1)


    # Trong class MiniMap hoặc Map
    def update_dot_position(self, player_pos):
        # Chia tọa độ mới thành 4 phần
        new_x = player_pos[0] / 4
        new_y = player_pos[1] / 4

        # Gán giá trị mới cho self.dot_position
        self.dot_position = (new_x, new_y)
