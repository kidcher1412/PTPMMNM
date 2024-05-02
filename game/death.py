import threading
import pygame

class Death:
    def __init__(self, screen, ipserver):
        self.screen = screen
        self.ipserver = ipserver
        self.font = pygame.font.Font(None, 20)
        self.max_displayed_messages = 5  # Display only the last 5 messages

        from realtime_data import Realtime_Data
        self.caser = Realtime_Data(self.ipserver)
        self.kill_listener_thread = threading.Thread(target=self.caser.ref_kill.listen, args=(self.caser.handle_new_kill,))
        self.kill_listener_thread.daemon = True  # Thiết lập cờ daemon
        self.kill_listener_thread.start()


    def draw_death(self):
        # if len(self.caser.list_kill) > self.max_displayed_messages:
        #     self.caser.list_kill = self.caser.list_kill[-self.max_displayed_messages:]

        if self.caser.list_kill:
            death_surface = pygame.Surface((200, 50 * self.max_displayed_messages), pygame.SRCALPHA)  
            death_surface.fill((30, 30, 30, 200))  # Fill with transparent color  

            line_height = 24  
            y_offset = 10  

# for msg in reversed(self.caser.list_chat[-6:]):
            for formatted_message in reversed(self.caser.list_kill[-6:]):
                text_lines = self.wrap_text(f'{formatted_message["sender"]} death!', self.font, 200 -34)  
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
    
    # def add_death(self, name, order_name):
    #     self.list_death.append(f"{name} killed {order_name}")


# abc