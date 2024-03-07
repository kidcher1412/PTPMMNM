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
        self.dot_position = (0, 0)

        # Tải ảnh và lấy kích thước ảnh gốc chỉ một lần
        self.original_image = pygame.image.load('./p1_setup/map/map4.png').convert_alpha()
        self.original_size = self.original_image.get_rect().size

        self.dragging = False

    def draw_map_preview(self, map_data):

        # Thay đổi kích thước ảnh theo mức độ zoom
        zoomed_size = (int(self.original_size[0] * self.zoom_factor), int(self.original_size[1] * self.zoom_factor))
        zoomed_image = pygame.transform.scale(self.original_image, zoomed_size)


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

        if self.dragging:
            # Nếu đang kéo, cập nhật vị trí của ảnh
            mouse_x, mouse_y = pygame.mouse.get_pos()
            drag_offset = (mouse_x - self.dot_position[0], mouse_y - self.dot_position[1])
            image_position = (image_position[0] + drag_offset[0], image_position[1] + drag_offset[1])
            self.dot_position = (mouse_x, mouse_y)
    
    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Nếu là nút trái chuột
                self.dragging = True
                self.last_mouse_pos = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                # Tính khoảng di chuyển của chuột
                mouse_x, mouse_y = pygame.mouse.get_pos()
                dx = mouse_x - self.last_mouse_pos[0]
                dy = mouse_y - self.last_mouse_pos[1]

                # Di chuyển ảnh theo khoảng di chuyển của chuột
                self.dot_position = (self.dot_position[0] + dx / (4 * self.zoom_factor),
                                    self.dot_position[1] + dy / (4 * self.zoom_factor))

                # Lưu lại vị trí chuột cho lần tiếp theo
                self.last_mouse_pos = (mouse_x, mouse_y)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False

    def handle_zoom(self, event):
        # Xử lý sự kiện zoom
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:  # Lăn lên
            self.zoom_factor = min(self.max_zoom, self.zoom_factor + 0.1)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:  # Lăn xuống
            self.zoom_factor = max(self.min_zoom, self.zoom_factor - 0.1)

        # Tính toán kích thước ảnh sau khi zoom
        zoomed_size = (int(self.original_size[0] * self.zoom_factor), int(self.original_size[1] * self.zoom_factor))

        # Kiểm tra nếu kích thước ảnh nhỏ hơn kích thước của background, thì giữ kích thước của background
        if zoomed_size[0] < self.map_preview['size'][0]:
            self.zoom_factor = self.map_preview['size'][0] / self.original_size[0]
        if zoomed_size[1] < self.map_preview['size'][1]:
            self.zoom_factor = self.map_preview['size'][1] / self.original_size[1]

        # Giới hạn kích thước zoom_factor để không vượt quá giới hạn
        self.zoom_factor = min(self.max_zoom, max(self.min_zoom, self.zoom_factor))
    
    # Trong class MiniMap hoặc Map
    def update_dot_position(self, player_pos):
        # Chia tọa độ mới thành 4 phần
        new_x = player_pos[0] / 4
        new_y = player_pos[1] / 4

        # Gán giá trị mới cho self.dot_position
        self.dot_position = (new_x, new_y)
