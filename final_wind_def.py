import os
import sys
import pygame


class Lose:
    def __init__(self):
        pygame.init()
        self.size = self.WIDTH, self.HEIGHT = 1200, 800
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()

        self.but_sound = pygame.mixer.Sound('data/but_sound.mp3')
        pygame.mixer.music.load('data/def_mus.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)

        self.sound_count = 1
        self.FPS = 60

        self.start_screen()

    '''Выбор изображения с папки проекта data'''

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

    '''Функционал и анимация кнопок окна'''

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
                        from main import Levels
                        Levels()
            else:
                fon = pygame.transform.scale(self.load_image(photo_name2), (width, height))
                self.screen.blit(fon, (x, y))
        else:
            fon = pygame.transform.scale(self.load_image(photo_name2), (width, height))
            self.screen.blit(fon, (x, y))

    '''Включение и выключение музыки'''

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

    '''Перерисовка изображения окна'''

    def update_image(self):
        fon = pygame.transform.scale(self.load_image('def_back.jpg'), (self.WIDTH, self.HEIGHT))
        self.screen.blit(fon, (0, 0))
        text = pygame.transform.scale(self.load_image('defeat_img.png'), (500, 250))
        self.screen.blit(text, (360, -10))
        font = pygame.font.Font(None, 70)
        text = font.render(f"Ваш результат: {0}", True, (137, 129, 118))
        self.screen.blit(text, (425, 220))
        self.buttons(1000, 700, 170, 90, 'def_cont_2.png', 'def_cont.png', 0)
        if self.sound_count % 2 == 0:
            sound_icon = pygame.transform.scale(self.load_image('sound2.png'), (25, 25))
            self.screen.blit(sound_icon, (1150, 30))
        else:
            sound_icon = pygame.transform.scale(self.load_image('sound1.png'), (25, 25))
            self.screen.blit(sound_icon, (1150, 30))

    '''Основной цикл окна'''

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
