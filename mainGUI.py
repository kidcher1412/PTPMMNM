"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - GAME SELECTOR
Game with 3 difficulty options.
"""

__all__ = ['main']

import multiprocessing
import subprocess
import threading
import pygame
import pygame_menu
from pygame_menu.examples import create_example_window

from random import randrange
from typing import Tuple, Any, Optional, List


from Auth import FirestoreConnector
import firebase_admin
from firebase_admin import credentials, firestore


cred = credentials.Certificate("./game/p1_setup/connect/connect.json")
# firebase_admin.initialize_app(cred)
firebase_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://test-app-b6d6d-default-rtdb.firebaseio.com'
})
firestore_connector = FirestoreConnector()
UsernameThis = ""

# Constants and global variables
ABOUT = [f'Name of this Game: Gatering Shooter',
         f'Author: Truong-Thong-Tien-Nhan',
         f'Email: gathering_shooter@gamemaster.com',
         f'Subject: Phat Trien Phan Mem Ma Nguon Mo',
         f'Instructors: Tu Lang Phieu']
DIFFICULTY = ['EASY']
FPS = 60
WINDOW_SIZE = (1280, 720)

clock: Optional['pygame.time.Clock'] = None
main_menu: Optional['pygame_menu.Menu'] = None
surface: Optional['pygame.Surface'] = None


def change_difficulty(value: Tuple[Any, int], difficulty: str) -> None:
    """
    Change difficulty of the game.

    :param value: Tuple containing the data of the selected object
    :param difficulty: Optional parameter passed as argument to add_selector
    """
    selected, index = value
    print(f'Selected difficulty: "{selected}" ({difficulty}) at index {index}')
    DIFFICULTY[0] = difficulty


def random_color() -> Tuple[int, int, int]:
    """
    Return a random color.

    :return: Color tuple
    """
    return randrange(0, 255), randrange(0, 255), randrange(0, 255)


def play_function(difficulty: List, name: str, test: bool = False) -> None:
    # Tạo một tiến trình mới và chạy game trong đó
    import os
    # Lấy đường dẫn của thư mục chứa file thực thi Python
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Tạo đường dẫn tới thư mục "game"
    cast_dir = os.path.join(current_directory, "game")

    # Tạo đường dẫn tới file "main" trong thư mục "game"
    cast_game = os.path.join(cast_dir, "main_offline")


    # Thay đổi thư mục làm việc thành thư mục "game"
    os.chdir(cast_dir)

    # Chạy file thực thi "main" trong thư mục "game"
    subprocess.run([cast_game])

    # Thay đổi thư mục làm việc thành thư mục "game"
    os.chdir(current_directory)
    
def play_function_online(team, serverip):
    # Tạo một tiến trình mới và chạy game trong đó
    import os

    # Lấy đường dẫn của thư mục chứa file thực thi Python
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Tạo đường dẫn tới thư mục "game"
    cast_dir = os.path.join(current_directory, "game")

    # Tạo đường dẫn tới file "main" trong thư mục "game"
    cast_game = os.path.join(cast_dir, "main_online")


    # Thay đổi thư mục làm việc thành thư mục "game"
    os.chdir(cast_dir)

    # Chạy file thực thi "main" trong thư mục "game"
    global UsernameThis
    print(f"{UsernameThis} {team} {serverip}")
    subprocess.run([cast_game,UsernameThis, team, serverip])

    # Thay đổi thư mục làm việc thành thư mục "game"
    os.chdir(current_directory)

def main_background() -> None:
    """
    Function used by menus, draw on background while menu is active.
    """
    global surface
    surface.fill((128, 0, 128))


def main( test: bool = False) -> None:
    """
    Main program.

    :param test: Indicate function is being tested
    """

    # -------------------------------------------------------------------------
    # Globals
    # -------------------------------------------------------------------------
    global clock
    global main_menu
    global surface
    global UsernameThis
    # -------------------------------------------------------------------------
    # Create window
    # -------------------------------------------------------------------------
    surface = create_example_window('Gatering Shooter', WINDOW_SIZE)
    clock = pygame.time.Clock()

    # -------------------------------------------------------------------------
    # Create menus: Play Menu
    # -------------------------------------------------------------------------
    
    play_theme = pygame_menu.themes.THEME_DEFAULT.copy()
    play_theme.background_color = (150, 150, 150, 180)
    play_theme.widget_font_size = 40


    play_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.7,
        title='Play Menu',
        width=WINDOW_SIZE[0] * 0.75,
        theme=play_theme
    )

    submenu_theme = pygame_menu.themes.THEME_DEFAULT.copy()
    submenu_theme.widget_font_size = 40
    play_submenu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 1,
        theme=submenu_theme,
        title='Submenu',
        width=WINDOW_SIZE[0] * 0.7
    )
    play_submenu.add.button('Refresh Room', lambda:draw_room(play_submenu))
    play_submenu.add.button('Return to main menu', lambda:pygame_menu.events.RESET)
    def draw_room(play_submenu):
        widgets = play_submenu.get_widgets()
        # Duyệt qua từng widget
        for widget in widgets:
            # Kiểm tra nếu widget không có tiêu đề là "123" thì xóa widget đó
            if widget._title != "Refresh Room":
                play_submenu.remove_widget(widget)
        global firestore_connector
        firestore_connector.handle_new_room()
        print(firestore_connector.list_room)
        for room in firestore_connector.list_room:
            play_submenu.add.button(room.replace("-", "."), lambda:play_function_online("B",room.replace("-", ".")))
    draw_room(play_submenu)


    

    play_menu.add.button('Start',  # When pressing return -> play(DIFFICULTY[0], font)
                         play_function,
                         DIFFICULTY,
                         pygame.font.Font(pygame_menu.font.FONT_FRANCHISE, 30))
    play_menu.add.selector('Select difficulty ',
                           [('1 - Easy', 'EASY'),
                            ('2 - Medium', 'MEDIUM'),
                            ('3 - Hard', 'HARD')],
                           onchange=change_difficulty,
                           selector_id='select_difficulty')
    play_menu.add.button('Another menu', play_submenu)
    play_menu.add.button('Return to main menu', pygame_menu.events.BACK)

    # -------------------------------------------------------------------------
    # Create menus:About
    # -------------------------------------------------------------------------
    about_theme = pygame_menu.themes.THEME_DEFAULT.copy()
    about_theme.widget_margin = (0, 0)

    about_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.6,
        theme=about_theme,
        title='About',
        width=WINDOW_SIZE[0] * 0.6
    )

    for m in ABOUT:
        about_menu.add.label(m, align=pygame_menu.locals.ALIGN_LEFT, font_size=30)
    about_menu.add.vertical_margin(30)
    about_menu.add.button('Return to menu', pygame_menu.events.BACK)


    # -------------------------------------------------------------------------
    # Create menus: Profile
    # -------------------------------------------------------------------------
    profile_theme = pygame_menu.themes.THEME_DEFAULT.copy()
    profile_theme.title_offset = (5, -2)
    profile_theme.widget_alignment = pygame_menu.locals.ALIGN_LEFT
    profile_theme.widget_font = pygame_menu.font.FONT_OPEN_SANS_LIGHT
    profile_theme.background_color = (150, 150, 150, 180)
    profile_theme.widget_font_size = 40


    profile_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.6,
        theme=profile_theme,
        title='Profile',
        width=WINDOW_SIZE[0] * 0.6
    )

    profile_menu.add.label("Hello Thong", align=pygame_menu.locals.ALIGN_LEFT, font_size=30)
    profile_menu.add.text_input(
        'Last name: ',
        default='Rambo',
        maxchar=18,
        textinput_id='last_name',
        input_underline='.'
    )
    profile_menu.add.text_input(
        'Password: ',
        maxchar=18,
        password=True,
        textinput_id='pass',
        input_underline='_'
    )
    def data_fun() -> None:
        """
        Print data of the menu.
        """
        print('Settings data:')
        data = profile_menu.get_input_data()
        print(data)
    # Add final buttons
    profile_menu.add.button('Store data', data_fun, button_id='store')  # Call function

    profile_menu.add.vertical_margin(30)
    profile_menu.add.button('Return to menu', pygame_menu.events.BACK)


    # ---------------------------------------------------------------------
    # ----
    # Create menus: sigup menu
    # -------------------------------------------------------------------------
    sigup_theme = pygame_menu.themes.THEME_DEFAULT.copy()
    sigup_theme.title_offset = (5, -2)
    sigup_theme.widget_alignment = pygame_menu.locals.ALIGN_LEFT
    sigup_theme.widget_font = pygame_menu.font.FONT_OPEN_SANS_LIGHT
    sigup_theme.widget_font_size = 30
    sigup_theme.background_color = (150, 150, 150, 180)


    sigup_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.6,
        theme=sigup_theme,
        title='Sigup',
        width=WINDOW_SIZE[0] * 0.6
    )

    # sigup_menu.add.label("Dang nhap", align=pygame_menu.locals.ALIGN_LEFT, font_size=30)
    sigup_menu.add.text_input(
        'Username: ',
        maxchar=20,
        textinput_id='user',
        input_underline='.'
    )
    sigup_menu.add.text_input(
        'Email: ',
        maxchar=24,
        textinput_id='email',
        input_underline='_'
    )
    sigup_menu.add.text_input(
        'Password: ',
        maxchar=28,
        password=True,
        textinput_id='pass',
        input_underline='_'
    )
    sigup_menu.add.text_input(
        'Re-password: ',
        maxchar=26,
        password=True,
        textinput_id='re-pass',
        input_underline='_'
    )
    def Sig_up() -> None:
        """
        Print data of the menu.
        """
        ##dang ki tai day
        data = sigup_menu.get_input_data()
        global firestore_connector
        firestore_connector.create_account(data["user"], data["pass"], data["email"])
        print(data)
        pygame_menu.events.BACK
    # Add final buttons
    sigup_menu.add.button('Store data', Sig_up)  # Call function
    sigup_menu.add.vertical_margin(30)
    sigup_menu.add.button('Return to Login', pygame_menu.events.BACK)

    # ---------------------------------------------------------------------
    # ----
    # Create menus: login menu
    # -------------------------------------------------------------------------
    login_theme = pygame_menu.themes.THEME_DEFAULT.copy()
    login_theme.title_offset = (5, -2)
    login_theme.widget_alignment = pygame_menu.locals.ALIGN_LEFT
    login_theme.widget_font = pygame_menu.font.FONT_OPEN_SANS_LIGHT
    login_theme.widget_font_size = 40
    login_theme.background_color = (150, 150, 150, 180)

    login_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.7,
        theme=login_theme,
        title='Login',
        width=WINDOW_SIZE[0] * 0.7
    )
    login_menu.add.text_input(
        'Username: ',
        maxchar=18,
        password=False,
        textinput_id='username',
        input_underline='_'
    )
    login_menu.add.text_input(
        'Password: ',
        maxchar=26,
        password=True,
        textinput_id='password',
        input_underline='_'
    )
    def login_data():
        data = login_menu.get_input_data()
        global firestore_connector
        authenticated, user_info = firestore_connector.authenticate(data["username"], data["password"])
        # print(data)
        if authenticated:
            global UsernameThis
            UsernameThis = data["username"]
            # Đóng menu đăng nhập
            login_menu.disable()
            # Mở menu chính và đặt nó là menu chính
            main_menu.enable()
        
        
    login_menu.add.vertical_margin(30)
    # login_menu.add.horizontal_margin(200)  # Thay đổi giá trị 200 nếu cầns
    login_menu.add.button('Login', login_data, align=pygame_menu.locals.ALIGN_CENTER)
    login_menu.add.button('Sigup', sigup_menu, align=pygame_menu.locals.ALIGN_CENTER)
    login_menu.add.vertical_margin(30)
    login_menu.add.button('Quit', pygame_menu.events.EXIT,align=pygame_menu.locals.ALIGN_CENTER)


    # ---------------------------------------------------------------------
    # ----
    # Create menus: Main
    # -------------------------------------------------------------------------
    main_theme = pygame_menu.themes.THEME_DEFAULT.copy()
    main_theme.background_color = (150, 150, 150, 180)
    main_theme.widget_font_size = 55

    main_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.8,
        theme=main_theme,
        title='Main Menu',
        width=WINDOW_SIZE[0] * 0.8
    )
    
    main_menu.add.label(f"Xin chao {UsernameThis}" , align=pygame_menu.locals.ALIGN_CENTER, font_size=40)
    main_menu.add.vertical_margin(30)
    main_menu.add.button('Play', play_menu)
    main_menu.add.button('About', about_menu)
    main_menu.add.button('Profile',profile_menu)
    main_menu.add.button('Quit', pygame_menu.events.EXIT)


    # -------------------------------------------------------------------------
    # Main loop
    # -------------------------------------------------------------------------


    while True:

        # Tick
        clock.tick(FPS)

        # Paint background
        main_background()

        # Application events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        # Main menu
        if login_menu.is_enabled():
            login_menu.mainloop(surface, main_background, disable_loop=test, fps_limit=FPS)
        if main_menu.is_enabled():
            main_menu.mainloop(surface, main_background, disable_loop=test, fps_limit=FPS)

        # Flip surface
        pygame.display.flip()

        # At first loop returns
        if test:
            break


if __name__ == '__main__':
    main()