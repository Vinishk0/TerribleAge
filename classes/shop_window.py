import os
import sys
import pygame


class Shop:
    def __init__(self):
        pygame.init()
        self.size = self.WIDTH, self.HEIGHT = 1200, 800
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()

        self.but_sound = pygame.mixer.Sound('data/musics/but_sound.mp3')
        pygame.mixer.music.load('data/musics/start_mus.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)

        self.sound_count = 1
        self.FPS = 60

        self.start_screen()

    '''Выбор изображения из папки проекта data'''

    def load_image(self, name, colorkey=None):
        fullname = os.path.join('data/', name)
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

    '''Функционал и анимация кнопок'''

    def buttons(self, x, y, width, height, photo_name1, photo_name2, num):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + width:
            if y < mouse[1] < y + height:
                fon = pygame.transform.scale(self.load_image(f'buttons_img/{photo_name1}'), (width, height))
                self.screen.blit(fon, (x, y))
                if click[0] == 1:
                    pygame.mixer.Sound.play(self.but_sound)
                    pygame.time.delay(300)
                    if num == 0:
                        from start_window import Start
                        Start()
            else:
                fon = pygame.transform.scale(self.load_image(f'buttons_img/{photo_name2}'), (width, height))
                self.screen.blit(fon, (x, y))
        else:
            fon = pygame.transform.scale(self.load_image(f'buttons_img/{photo_name2}'), (width, height))
            self.screen.blit(fon, (x, y))

    '''Перерисовка изображения'''

    def update_image(self):
        fon = pygame.transform.scale(self.load_image('backgrounds_img/shop_back.jpg'), (self.WIDTH, self.HEIGHT))
        self.screen.blit(fon, (0, 0))
        self.buttons(980, 700, 200, 80, 'menu_lvl2.png', 'menu_lvl.png', 0)
        self.buttons(200, 530, 100, 40, 'BUY2.png', 'BUY.png', 1)
        self.buttons(560, 530, 100, 40, 'BUY2.png', 'BUY.png', 2)
        self.buttons(910, 530, 100, 40, 'BUY2.png', 'BUY.png', 3)

        self.files()
        if self.sound_count % 2 == 0:
            sound_icon = pygame.transform.scale(self.load_image('buttons_img/sound2.png'), (25, 25))
            self.screen.blit(sound_icon, (1150, 30))
        else:
            sound_icon = pygame.transform.scale(self.load_image('buttons_img/sound1.png'), (25, 25))
            self.screen.blit(sound_icon, (1150, 30))

    ''' Включение и выключение музыки'''

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

    '''Очки из файла проекта'''

    def files(self):
        f = open("Results.txt", encoding="utf8")
        data = f.readlines()
        count = int(data[0])
        f.close()
        font = pygame.font.Font(None, 30)
        text = font.render(f'{count}', True, (255, 255, 255))
        self.screen.blit(text, (1000, 30))
        sound_img = pygame.transform.scale(self.load_image('icons_img/count_img.png'), (25, 25))
        self.screen.blit(sound_img, (1025, 25))

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