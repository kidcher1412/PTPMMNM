import pygame
import sys

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 300

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Đăng Nhập')

font = pygame.font.Font(None, 36)

username = ''
password = ''
active_input = 'username'  # Biến để xác định trường nhập liệu đang được chọn

def draw_text(surface, text, color, x, y):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

def main():
    global username, password, active_input

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print("Username:", username)
                    print("Password:", password)
                elif event.key == pygame.K_BACKSPACE:
                    if active_input == 'username' and len(username) > 0:
                        username = username[:-1]
                    elif active_input == 'password' and len(password) > 0:
                        password = password[:-1]
                elif event.key == pygame.K_TAB:
                    if active_input == 'username':
                        active_input = 'password'
                    else:
                        active_input = 'username'
                else:
                    if event.unicode.isalnum() or event.unicode in ['.', '_']:
                        if active_input == 'username' and len(username) < 15:
                            username += event.unicode
                        elif active_input == 'password' and len(password) < 15:
                            password += '*'

        screen.fill(WHITE)

        draw_text(screen, 'Login', BLACK, 150, 50)
        draw_text(screen, 'Username:', BLACK, 50, 120)
        if active_input == 'username':
            pygame.draw.rect(screen, BLACK, (198, 120, 4, 36), 2)  # Vẽ khung nhấp nháy cho trường username
        draw_text(screen, username, BLACK, 200, 120)

        draw_text(screen, 'Password:', BLACK, 50, 160)
        if active_input == 'password':
            pygame.draw.rect(screen, BLACK, (198, 160, 4, 36), 2)  # Vẽ khung nhấp nháy cho trường password
        draw_text(screen, '*' * len(password), BLACK, 200, 160)

        pygame.display.flip()

if __name__ == "__main__":
    main()
