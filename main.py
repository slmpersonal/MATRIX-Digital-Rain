import pygame
import sys
import os
import json
from random import randrange, choice

settings = {  # Hardcoded default settings
    'debug_overlay': True,  # add debug overlay fps/cpu/log
    'resolution.x': 800,
    'resolution.y': 600,
    'font_loc': 'font/ms mincho.ttf',
    'font_size': 40,
    'scale_font': True,
    'color_green': (20, 240, 20),  # Green
    'color_light_green': (180, 250, 180),  # Light green
    'color_red': (245, 20, 20),  # Red
    'color_blue': (40, 40, 140),  # Blue
    'color_black': (0, 0, 0),  # Blue
    'alpha_value': 0,
    'max_fps': 60,
    'game_clock': 15,
    'matrix_multiplier': 1,
    'eng_u_multiplier': 1,
    'eng_l_multiplier': 1,
    'num_multiplier': 1,
    'sym_mid_multiplier': 1,
    'sym_top_multiplier': 1
}

try:  # Load or create settings.json
    with open('settings.json', 'r') as text_file:
        print("settings.json found.")
        settings = json.load(text_file)
except FileNotFoundError:  # than write new settings.json with defaults
    print("settings.json not found. Creating default file")
    with open('settings.json', 'w') as text_file:
        json.dump(settings, text_file)
with open("settings.json", "r") as text_file:
    print(f'settings loaded:{json.load(text_file)}')  # for debugging

run = True
game_clock = settings['game_clock']
timer_1 = str(game_clock).rjust(3)
resolution = res_width, res_height = (settings['resolution.x']), (settings['resolution.y'])
surface_x_offset = int(res_width / 16)
surface_y_offset = int(res_height / 5)
surface_res = (res_width - (surface_x_offset * 2)), (res_height - (surface_y_offset * 2))

os.environ['SDL_VIDEO_CENTERED'] = '1'

if settings['scale_font']:
    settings['font_size'] = int(surface_y_offset / 3.14)

top_symbols = [33, 35, 36, 37, 38, 40, 41, 42, 43, 45, 61, 64, 94, 95, 96, 126]
middle_symbols = [34, 39, 44, 46, 47, 58, 59, 60, 62, 63, 91, 92, 93, 123, 124, 125]
chr_set_matrix = [chr(int('0x30a0', 16) + i) for i in range(96)]  # Original Matrix chr_set
chr_set_pt_2 = [chr(int(65) + i) for i in range(26)]  # English Upper chr_set
chr_set_pt_3 = [chr(int(97) + i) for i in range(26)]  # English lower chr_set
chr_set_pt_4 = [chr(int(48) + i) for i in range(10)]  # Numbers
chr_set_pt_5 = [chr(middle_symbols[i]) for i in range(0, len(middle_symbols) - 1)]  # Middle keyboard symbols
chr_set_pt_6 = [chr(top_symbols[i]) for i in range(0, len(top_symbols) - 1)]  # Top keyboard symbols
chr_set = [chr(int(32))]  # NEED function/nav keycodes


def add2sets(set_1, set_2, set_multi):  # Function to combined chr_set(s) list
    for i in range(0, set_multi):
        set_1 += set_2


add2sets(chr_set, chr_set_pt_2, (settings['eng_u_multiplier']))
add2sets(chr_set, chr_set_pt_3, (settings['eng_l_multiplier']))
add2sets(chr_set, chr_set_pt_4, (settings['num_multiplier']))
add2sets(chr_set, chr_set_pt_5, (settings['sym_mid_multiplier']))
add2sets(chr_set, chr_set_pt_6, (settings['sym_top_multiplier']))


class Symbol:
    def __init__(self, x, y, speed):
        self.x, self.y = x, y
        self.speed = speed
        self.value = choice(green)
        self.interval = randrange(5, 30)

    def draw(self, color):
        if color == 'green':
            coin = randrange(0, 20)  # Increasing this range reduces red frequency
            if coin == 0:
                color = 'red'
            black_coin = randrange(0, 10)  # Increasing this range reduces black/flicker frequency
            if black_coin == 0:
                color = 'black'

        frames = pygame.time.get_ticks()
        if not frames % self.interval:
            self.value = choice(green if color == 'green' else black if color == 'black' else red if color == 'red' else light_green)
        self.y = self.y + self.speed if self.y < res_height else -settings['font_size']
        surface.blit(self.value, (self.x, self.y))


class SymbolColumn:
    def __init__(self, x, y):
        self.column_height = randrange(int(res_height / 100), int(res_width / 100))
        self.speed = randrange(3, 7)
        self.symbols = [Symbol(x, i, self.speed) for i in range(y, y - (settings['font_size']) * self.column_height, -(
            settings['font_size']))]

    def draw(self):
        [symbol.draw('green') if i else symbol.draw('light green') for i, symbol in enumerate(self.symbols)]


pygame.init()  # Init pygame
font = pygame.font.Font(settings['font_loc'], settings['font_size'])  # Set font
screen = pygame.display.set_mode(resolution)  # Display updater
clock = pygame.time.Clock()  # Create clock

#  Objects
background = pygame.image.load("assets/background.png").convert()  # Define background variables
background = pygame.transform.scale(background, resolution)  # Scale background image
textbox1 = pygame.image.load("assets/textbox.png").convert()
textbox1 = pygame.transform.scale(textbox1,
                                  ((res_width - (surface_x_offset * 2)), int(surface_y_offset / 4)))
cli_cursor = pygame.image.load("assets/cli_cursor.png").convert()  # NEEDs work on scaling
cli_cursor = pygame.transform.scale(cli_cursor, (((settings['font_size']) / 2), int((settings['font_size']) / 10)))
surface = pygame.Surface(surface_res)
surface.set_alpha(settings['alpha_value'])

#  Set in-game timer
pygame.time.set_timer(pygame.USEREVENT, 1000)

#  Define choices
black = [font.render(char, True, (settings['color_black'])) for char in chr_set_matrix]
red = [font.render(char, True, (settings['color_red'])) for char in chr_set]
green = [font.render(char, True, (settings['color_green'])) for char in chr_set_matrix]
light_green = [font.render(char, True, (settings['color_light_green'])) for char in chr_set_matrix]

#  Draw columns
symbol_columns = [SymbolColumn(x, randrange(-res_height, 0)) for x in range(0, res_width,
                                                                            settings['font_size'])]
#  In-Game messages
message_1 = font.render('[CORRUPTION]', False, (250, 40, 40))

while run:

    screen.blit(background, (0, 0))
    screen.blit(textbox1, (surface_x_offset, (res_height - surface_y_offset)))
    screen.blit(cli_cursor, (surface_x_offset + int((settings['font_size']) * 0.4),
                             (res_height - surface_y_offset + int((settings['font_size']) * 0.5))))
    screen.blit(surface, (surface_x_offset, surface_y_offset))

    surface.fill(pygame.Color('black'))

    [symbol_column.draw() for symbol_column in symbol_columns]

    if not pygame.time.get_ticks() % 20 and settings['alpha_value'] < 170:
        settings['alpha_value'] += 6
        surface.set_alpha(settings['alpha_value'])
        pygame.display.update()
    if game_clock == 0:  # NEED to add 'and' for win/lost messages
        screen.blit(message_1, (((res_width / 2) - surface_y_offset), ((res_height / 2) - surface_y_offset)))
    screen.blit(font.render(str(timer_1), True, (0, 0, 140)), ((surface_x_offset, surface_y_offset)))
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT:
            game_clock -= 1
            timer_1 = str(game_clock).rjust(3) if game_clock > 0 else 'GAME OVER!'
        if event.type == pygame.QUIT:
            with open('settings.json', 'w') as text_file:  # NEED try/except for disk-permission-write error
                json.dump(settings, text_file)
            run = False
    pygame.display.flip()
    clock.tick(settings['max_fps'])
pygame.quit()
sys.exit()
