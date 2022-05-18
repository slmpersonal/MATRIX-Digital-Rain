import pygame
import sys
import os
import json
from random import randrange, choice
import numpy

settings = {  # Hardcoded default settings
    'debug_overlay': True,  # add debug overlay fps/cpu/log
    'resolution.x': 800,
    'resolution.y': 600,
    'font': 'font/ms mincho.ttf',
    'font_size': 40,
    'scale_font': True,
    'color_green': (20, 240, 20),  # Green
    'color_light_green': (180, 250, 180),  # Light green
    'color_red': (245, 20, 20),  # Red
    'color_blue': (40, 40, 140),  # Blue
    'color_black': (0, 0, 0),  # Blue
    'alpha_value': 0,
    'max_fps': 60,
    'game_clock': 300,
    'matrix_multiplier': 1,
    'eng_u_multiplier': 1,
    'eng_l_multiplier': 1,
    'num_multiplier': 1,
    'sym_mid_multiplier': 1,
    'sym_top_multiplier': 1
}

try:  # load or create settings.json
    with open('settings.json', 'r') as text_file:
        print("settings.json found.")
        settings = json.load(text_file)
except FileNotFoundError:  # than write new setting.json with defaults
    print("settings.json not found. Creating default file")
    with open('settings.json', 'w') as text_file:  # NEED try/except for disk-permission-write error
        json.dump(settings, text_file)
with open("settings.json", "r") as text_file:
    print(f'settings loaded:{json.load(text_file)}')  # for debugging

max_fps = settings['max_fps']
game_clock = settings['game_clock']
resolution = (settings['resolution.x']), (settings['resolution.y'])
surface_x_offset = int(settings['resolution.x'] / 16)
surface_y_offset = (int(settings['resolution.y'] / 10) * 2)
surface_res = (
    ((settings['resolution.x']) - (surface_x_offset * 2)), ((settings['resolution.y']) - (surface_y_offset * 2)))

os.environ['SDL_VIDEO_CENTERED'] = '1'


if settings['scale_font']:
    font = (surface_y_offset / 25)


top_symbols = [96, 126, 33, 64, 35, 36, 37, 94, 38, 42, 40, 41, 95, 43, 61, 45]
middle_symbols = (91, 93, 92, 59, 39, 44, 46, 47, 123, 125, 124, 58, 34, 60, 62, 63)
chr_set_pt_1 = [chr(int('0x30a0', 16) + i) for i in range(96)]  # Original Matrix chr_set
chr_set_pt_2 = [chr(int(65) + i) for i in range(26)]  # English Upper chr_set
chr_set_pt_3 = [chr(int(97) + i) for i in range(26)]  # English lower chr_set
chr_set_pt_4 = [chr(int(48) + i) for i in range(57)]  # Numbers
chr_set_pt_5 = [chr(middle_symbols[i]) for i in range(0, len(middle_symbols) - 1)]  # Middle keyboard symbols
chr_set_pt_6 = [chr(top_symbols[i]) for i in range(0, len(top_symbols) - 1)]  # Top keyboard symbols
chr_set = [chr(int(32))]  # NEED function/nav keycodes

for i in range(0, (settings['matrix_multiplier'])):
    chr_set += chr_set_pt_1
for i in range(0, (settings['eng_u_multiplier'])):
    chr_set += chr_set_pt_2
for i in range(0, (settings['eng_l_multiplier'])):
    chr_set += chr_set_pt_3
for i in range(0, (settings['num_multiplier'])):
    chr_set += chr_set_pt_4
for i in range(0, (settings['sym_mid_multiplier'])):
    chr_set += chr_set_pt_5
for i in range(0, (settings['sym_top_multiplier'])):
    chr_set += chr_set_pt_6


class Symbol:
    def __init__(self, x, y, speed):
        self.x, self.y = x, y
        self.speed = speed
        self.value = choice(green_katakana)
        self.interval = randrange(5, 30)

    def draw(self, color):
        if color == 'green':
            coin = randrange(0, 20)  # Increasing this range reduces red frequency
            if coin == 0:
                color = 'red'
            black_coin = randrange(0, 10)  # Increasing this range reduces black frequency
            if black_coin == 0:
                color = 'black'

        frames = pygame.time.get_ticks()
        if not frames % self.interval:
            self.value = choice(green_katakana if color == 'green' else black_katakana if color == 'black'
            else red_katakana if color == 'red' else light_green_katakana)
        self.y = self.y + self.speed if self.y < settings['resolution.y'] else -settings['font_size']
        surface.blit(self.value, (self.x, self.y))


class SymbolColumn:
    def __init__(self, x, y):
        self.column_height = randrange(int((settings['resolution.y']) / 100), int((settings['resolution.x']) / 100))
        self.speed = randrange(3, 7)
        self.symbols = [Symbol(x, i, self.speed) for i in range(y, y - (settings['font_size']) * self.column_height, -(
            settings['font_size']))]

    def draw(self):
        [symbol.draw('green') if i else symbol.draw('light green') for i, symbol in enumerate(self.symbols)]


pygame.init()  # init pygame
font = pygame.font.Font(settings['font'], settings['font_size'])  # Set font
screen = pygame.display.set_mode(resolution)  # Display updater
background = pygame.image.load("assets/background.png").convert()  # Define background variables
background = pygame.transform.scale(background, resolution)  # Scale background image
textbox1 = pygame.image.load("assets/textbox.png").convert()
textbox1 = pygame.transform.scale(textbox1, (((settings['resolution.x']) - (surface_x_offset * 2)), int(surface_y_offset / 4)))
cli_cursor = pygame.image.load("assets/cli_cursor.png").convert()
cli_cursor = pygame.transform.scale(cli_cursor, (((settings['font_size']) / 2), int((settings['font_size']) / 10)))
surface = pygame.Surface(surface_res)
surface.set_alpha(settings['alpha_value'])
clock = pygame.time.Clock()

#  define choices
black_katakana = [font.render(char, True, (settings['color_black'])) for char in chr_set]
red_katakana = [font.render(char, True, (settings['color_red'])) for char in chr_set]
green_katakana = [font.render(char, True, (settings['color_green'])) for char in chr_set]
light_green_katakana = [font.render(char, True, (settings['color_light_green'])) for char in chr_set]

symbol_columns = [SymbolColumn(x, randrange(-settings['resolution.y'], 0)) for x in range(0, settings['resolution.x'],
                                                                                          settings['font_size'])]

while True:

    screen.blit(background, (0, 0))
    screen.blit(textbox1, (surface_x_offset, ((settings['resolution.y']) - surface_y_offset)))
    screen.blit(cli_cursor, (surface_x_offset + int((settings['font_size']) * 0.4), ((settings['resolution.y']) - surface_y_offset + int((settings['font_size']) * 0.5))))
    screen.blit(surface, (surface_x_offset, surface_y_offset))
    surface.fill(pygame.Color('black'))

    [symbol_column.draw() for symbol_column in symbol_columns]

    if not pygame.time.get_ticks() % 20 and settings['alpha_value'] < 170:
        settings['alpha_value'] += 6
        surface.set_alpha(settings['alpha_value'])
        pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open('settings.json', 'w') as text_file:  # NEED try/except for disk-permission-write error
                json.dump(settings, text_file)
            pygame.quit()
            sys.exit()
    pygame.display.flip()
    game_clock -= 1

    clock.tick(max_fps)
