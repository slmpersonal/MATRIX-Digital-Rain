import pygame
import sys
import os
import json
from random import randrange, choice
import numpy

settings = {  # Hardcoded default settings
    'resolution.x': 1600,
    'resolution.y': 900,
    'font': 'font/ms mincho.ttf',
    'font_size': 40,
    'color green': (40, 140, 40),  # Green
    'color red': (140, 40, 40),  # Red
    'color blue': (40, 40, 140),  # Blue
    'alpha_value': 0
}
resolution = (settings['resolution.x']), (settings['resolution.y'])
surface_x_offset = int(settings['resolution.x'] / 16)
surface_y_offset = (int(settings['resolution.y'] / 14) * 2)
surface_res = (((settings['resolution.x']) - (surface_x_offset * 2)), ((settings['resolution.y']) - (surface_y_offset * 2)))
os.environ['SDL_VIDEO_CENTERED'] = '1'
chr_set_pt_1 = [chr(int('0x30a0', 16) + i) for i in range(96)]  # Original Matrix chr_set
chr_set_pt_2 = [chr(int(65) + i) for i in range(26)]  # English Upper chr_set
chr_set_pt_3 = [chr(int(97) + i) for i in range(26)]  # English lower chr_set
chr_set = chr_set_pt_1 + chr_set_pt_2 + chr_set_pt_3  # Character set(s)

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


class Symbol:
    def __init__(self, x, y, speed):
        self.x, self.y = x, y
        self.speed = speed
        self.value = choice(green_katakana)
        self.interval = randrange(5, 30)

    def draw(self, color):
        frames = pygame.time.get_ticks()
        if not frames % self.interval:
            self.value = choice(green_katakana if color == 'green' else lightgreen_katakana)
            #  use choice for Red corrupt symbols
        self.y = self.y + self.speed if self.y < settings['resolution.y'] else -settings['font_size']
        surface.blit(self.value, (self.x, self.y))


class SymbolColumn:
    def __init__(self, x, y):
        self.column_height = randrange(8, 24)
        self.speed = randrange(3, 7)
        self.symbols = [Symbol(x, i, self.speed) for i in range(y, y - (settings['font_size']) * self.column_height, -(settings['font_size']))]

    def draw(self):
        [symbol.draw('green') if i else symbol.draw('lightgreen') for i, symbol in enumerate(self.symbols)]


pygame.init()  # init pygame
font = pygame.font.Font(settings['font'], settings['font_size'])  # Set font
screen = pygame.display.set_mode((resolution))  # Display updater
background = pygame.image.load("assets/background.png").convert()  # Define background variables
background = pygame.transform.scale(background, (resolution))  # Scale background image
surface = pygame.Surface(surface_res)
surface.set_alpha(settings['alpha_value'])
clock = pygame.time.Clock()

#  define choices
green_katakana = [font.render(char, True, (00, 160, 00)) for char in chr_set]
lightgreen_katakana = [font.render(char, True, pygame.Color('lightgreen')) for char in chr_set]

symbol_columns = [SymbolColumn(x, randrange(-settings['resolution.y'], 0)) for x in range(0, settings['resolution.x'], settings['font_size'])]

while True:

    screen.blit(background, (0, 0))
    screen.blit(surface, (surface_x_offset, (surface_y_offset + (surface_y_offset / 3))))
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
    clock.tick(60)
