import os
import sys
import pygame
from main import Levels
from shop_window import Shop
from rules import Rules

class Start:
    def __init__(self):
        pygame.init()
        self.size = self.WIDTH, self.HEIGHT = 1200, 800
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()

        pygame.display.set_caption('TerriableAge')  # название игры
        icon = pygame.image.load('data/logo.png')   # иконка игры
        pygame.display.set_icon(icon)

        self.but_sound = pygame.mixer.Sound('data/but_sound.mp3')  # звук нажатия кнопок
        self.start_music = 'data/start_mus.mp3'  # музыка

        pygame.mixer.music.load(self.start_music)
        pygame.mixer.music.play(-1)                 # настойка музыки
        pygame.mixer.music.set_volume(0.1)

        self.FPS = 60
        self.sound_count = 1

        self.start_screen()

    def load_image(self, name, colorkey=None):
        fullname = os.path.join('data', name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)

        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()

        return image

    def buttons(self, x, y, width, height, photo_name1, photo_name2, num):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + width:
            if y < mouse[1] < y + height:
                fon = pygame.transform.scale(self.load_image(photo_name1), (width, height))
                self.screen.blit(fon, (x, y))
                if click[0] == 1:
                    pygame.mixer.Sound.play(self.but_sound)
                    pygame.time.delay(300)
                    if num == 0:
                        Levels()
                    if num == 1:
                        Shop()
                    if num == 2:
                        Rules()
                    if num == 3:
                        sys.exit()

            else:
                fon = pygame.transform.scale(self.load_image(photo_name2), (width, height))
                self.screen.blit(fon, (x, y))
        else:
            fon = pygame.transform.scale(self.load_image(photo_name2), (width, height))
            self.screen.blit(fon, (x, y))

    def sounds_point(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if 1150 < mouse[0] < 1150 + 25:
            if 30 < mouse[1] < 30 + 25:
                if click[0] == 1:
                    self.sound_count += 1
                    if self.sound_count % 2 == 0:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()

    '''Отображение окна меню'''

    def update_image(self):
        fon = pygame.transform.scale(self.load_image('start_back.jpg'), (self.WIDTH, self.HEIGHT))
        self.screen.blit(fon, (0, 0))
        fon = pygame.transform.scale(self.load_image('1.png'), (250, 100))
        self.screen.blit(fon, (480, 30))
        self.buttons(500, 165, 200, 80, 'play2.png', 'play1.png', 0)
        self.buttons(500, 265, 200, 80, 'shop2.png', 'shop1.png', 1)
        self.buttons(500, 365, 200, 80, 'rules_lvl2.png', 'rules_lvl.png', 2)
        self.buttons(500, 465, 200, 80, 'exit1.png', 'exit2.png', 3)
        if self.sound_count % 2 == 0:
            sound_icon = pygame.transform.scale(self.load_image('sound2.png'), (25, 25))
            self.screen.blit(sound_icon, (1150, 30))
        else:
            sound_icon = pygame.transform.scale(self.load_image('sound1.png'), (25, 25))
            self.screen.blit(sound_icon, (1150, 30))

    def start_screen(self):
        while True:
            for event in pygame.event.get():
                self.update_image()
                self.sounds_point()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.flip()
            self.clock.tick(self.FPS)


Start()
