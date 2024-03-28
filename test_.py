import pygame
import sys
import pygame_gui

pygame.init()

WIDTH , HEIGHT = 1500,800
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("text")

CLOCK = pygame.time.Clock()
MANAGER = pygame_gui.UIManager((WIDTH,HEIGHT))

TEXT_INPUT  = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350,275),(WIDTH/2,50),manager=MANAGER))
chat_background_color = (50, 50, 50, 200)

def show_text(tex_to_show):
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        SCREEN.fill("white")
        new_text = pygame.font.SysFont("bahnschrift",100).render(f"hello,{tex_to_show}",True,"black")
        new_text_rect = new_text.get_rect(center=(WIDTH/2,HEIGHT/2))
        SCREEN.blit(new_text,new_text_rect)
        CLOCK.tick(60)
        pygame.display.update()
def get_user_name():
    while True:
        UI_REFRESH_RATE = CLOCK.tick(60)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type== pygame_gui.UI_TEXT_ENTRY_FINISHED:
                show_text(event.text)

            MANAGER.process_events(event)
        MANAGER.update(UI_REFRESH_RATE)
        SCREEN.fill(chat_background_color)
        MANAGER.draw_ui(SCREEN)
        pygame.display.update()
get_user_name()