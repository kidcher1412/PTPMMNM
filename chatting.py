import pygame
import pygame_gui
import threading

class Chatting:
    def __init__(self, screen):
        self.screen = screen
        # Create a new UIManager with a custom theme
        self.manager = pygame_gui.UIManager(screen.get_size())
        self.chat_messages = ['abc','acsc','htc','asasf','asdfe','htc  ádf ádf ádf adf ádf adsf ádf adsfasdfsdaf','abc','ádfasdffsdf']
        self.chat_font = pygame.font.Font(None, 36)  # You may adjust the font size
        # Dark gray background color
        self.background_dark_gray =(30, 30, 30, 200)
        # Input box attributes
        input_box_height = 30
        # Use a relative rectangle to position the input box at the bottom
        self.input_box = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((10, screen.get_height() - input_box_height - 10), (screen.get_width() - 20, input_box_height)),
                                                              manager=self.manager)

        # Scroll offset
        self.scroll_offset = 0

        from realtime_data import Realtime_Data
        self.caser = Realtime_Data()

        self.chat_listener_thread = threading.Thread(target=self.caser.ref_chat.listen, args=(self.caser.handle_new_message,))
        self.chat_listener_thread.daemon = True  # Thiết lập cờ daemon
        self.chat_listener_thread.start()

        # self.caser.ref_chat.listen(self.caser.handle_new_message)
        # self.caser.ref_kill.listen(self.caser.handle_new_kill)

        print(self.caser.list_chat)


    def show_chat(self,name):

        # Render chat messages
        chat_surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        chat_surface.fill(self.background_dark_gray)

        start_y = self.screen.get_height() - self.input_box.rect.height - 10 - len(self.caser.list_chat) * 40 + self.scroll_offset
        i = 0
        for msg in self.caser.list_chat:
            text_surface = self.chat_font.render(msg["sender"]+ ': ' + msg["content"], True, (255, 255, 255))  # Thêm dấu chấm ở đây
            text_rect = text_surface.get_rect(topleft=(20, start_y + i * 40))
            chat_surface.blit(text_surface, text_rect)
            i+=1

        self.screen.blit(chat_surface, (0, 0))

        # Update manager and draw UI elements
        self.manager.update(pygame.time.Clock().tick(60) / 1000.0)
        self.manager.draw_ui(self.screen)


    def mini_chat(self,name):
        mini_chat_width = 200

        # Create mini chat surface
        mini_chat_surface = pygame.Surface((mini_chat_width, 150), pygame.SRCALPHA)
        mini_chat_surface.fill(self.background_dark_gray)  # Background color for mini chat

        # Draw border around mini chat
        pygame.draw.rect(mini_chat_surface, self.background_dark_gray, mini_chat_surface.get_rect(), 5)
        self.mini_chat_font = pygame.font.Font(None, self.chat_font.get_height() - 3)

        # Display all messages in chat_messages in reverse order (from newest to oldest)
        line_height = 30
        line_count = 0  # Initialize line count
        for msg in reversed(self.caser.list_chat[-6:]):  # Loop through messages in reverse order
            # Split message into lines that fit within the width of the mini chat
            lines = self.wrap_text(f'{msg["sender"]}: {msg["content"]}', self.mini_chat_font, mini_chat_width - 34)  # Adjusted width accounting for padding

            # Calculate starting y position for current message
            start_y = 150 - (line_count + len(lines)) * line_height

            # Render each line of text
            first_line = True
            for i, line in enumerate(lines):
                # Calculate the width of ":" character
                colon_width, _ = self.mini_chat_font.size(': ')

                # Add colon at the beginning of the first line
                if first_line:
                    line_with_colon = line
                    first_line = False
                else:
                    # Calculate the width of text before ":"
                    prefix_width, _ = self.mini_chat_font.size(line.split(':')[0] + ': ')

                    # Add space to align text with the first line
                    line_with_colon = ' ' * (colon_width - prefix_width) + line

                text_surface = self.mini_chat_font.render(line_with_colon, True, (255, 255, 255))  # Render text
                text_rect = text_surface.get_rect(topleft=(10, start_y + i * line_height))
                mini_chat_surface.blit(text_surface, text_rect)

            # Increment line count
            line_count += len(lines)


        # Display mini chat in the top right corner of the screen
        mini_chat_rect = mini_chat_surface.get_rect(topright=(self.screen.get_width() - 10, 300))
        self.screen.blit(mini_chat_surface, mini_chat_rect)

    def wrap_text(self, text, font, max_width):
        """Wrap text to fit within a maximum width."""
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

    def handle_events(self, event):
        if event.type == pygame.USEREVENT:  # Bắt sự kiện kết thúc nhập liệu từ ô text
            if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                if event.ui_element == self.input_box:
                    self.process_return_key()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                self.process_up_key()
            elif event.button == 5:  # Scroll down
                self.process_down_key()
            elif event.button == 5: 
                self.input_box.unfocus()            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.input_box.unfocus()  # Xóa trạng thái focus của ô nhập liệu khi nhấn Esc
            elif event.key == pygame.K_RETURN:
                self.input_box.focus()  
        self.manager.process_events(event)

    def process_return_key(self): #apend submit chat
        if self.input_box.text:
            self.caser.send_message("thong",self.input_box.text)
            self.input_box.set_text('')
            self.process_down_key()


    def process_up_key(self):
        if len(self.caser.list_chat) * 40 > self.screen.get_height() - self.input_box.rect.height - 20:
            if self.scroll_offset < 0:
                self.scroll_offset = min(self.scroll_offset + 40, 0)
            else:
                self.scroll_offset += 40
                

    def process_down_key(self):
        if self.scroll_offset == 0 and len(self.caser.list_chat) > 0:
            first_message_y = self.screen.get_height() - self.input_box.rect.height - 10 - len(self.caser.list_chat) * 40 + self.scroll_offset
            if first_message_y <= self.input_box.rect.y:
                return
        elif self.scroll_offset >= 0:
            self.scroll_offset = 0
        else:
            self.scroll_offset = max(self.scroll_offset - 40, -len(self.caser.list_chat) * 40 + self.screen.get_height() - self.input_box.rect.height - 20)