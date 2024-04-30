import pygame

class Death:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 20)
        self.list_death = []  
        self.max_displayed_messages = 5  # Display only the last 5 messages

    def draw_death(self):
        if len(self.list_death) > self.max_displayed_messages:
            self.list_death = self.list_death[-self.max_displayed_messages:]

        if self.list_death:
            death_surface = pygame.Surface((200, 50 * self.max_displayed_messages), pygame.SRCALPHA)  
            death_surface.fill((0, 0, 0, 0))  # Fill with transparent color  

            line_height = 24  
            y_offset = 10  

            for i, formatted_message in enumerate(self.list_death):
                text_lines = self.wrap_text(formatted_message, self.font, 200 -34)  
                for line in text_lines:
                    if y_offset + line_height <= 50 * self.max_displayed_messages:
                        text_surface = self.font.render(line, True, (255, 255, 255))  
                        text_rect = text_surface.get_rect(topleft=(10, y_offset))  
                        death_surface.blit(text_surface, text_rect)  
                        y_offset += line_height  

            self.screen.blit(death_surface, (self.screen.get_width() - 210, 0))  

    def wrap_text(self, text, font, max_width):
        lines = []
        words = text.split(' ')
        current_line = ''
        for word in words:
            test_line = current_line + word + ' '
            test_width, _ = font.size(test_line)
            if test_width > max_width:
                lines.append(current_line.strip())
                current_line = word + ' '
            else:
                current_line = test_line
        lines.append(current_line.strip())
        return lines
    
    def add_death(self, name, order_name):
        self.list_death.append(f"{name} killed {order_name}")


# abc