import os
import sys
import pygame


class Start:
    def __init__(self):
        pygame.init()
        self.size = self.WIDTH, self.HEIGHT = 1200, 800
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.but_sound = pygame.mixer.Sound('data/but_sound.mp3')
        pygame.display.set_caption('Меню')
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
                        pygame.quit()
                        import main
                    if num == 1:
                        pass
                    if num == 2:
                        pygame.quit()
                        import shop_window
                    if num == 3:
                        sys.exit()
                    if num == 4:
                        pygame.mixer.music.stop()

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
            if 750 < mouse[1] < 750 + 25:
                if click[0] == 1:
                    self.sound_count += 1

    def update_image(self):
        fon = pygame.transform.scale(self.load_image('start_back.jpg'), (self.WIDTH, self.HEIGHT))
        self.screen.blit(fon, (0, 0))
        fon = pygame.transform.scale(self.load_image('1.png'), (250, 100))
        self.screen.blit(fon, (480, 30))
        self.buttons(500, 165, 200, 80, 'play2.png', 'play1.png', 0)
        self.buttons(500, 265, 200, 80, 'train2.png', 'train1.png', 1)
        self.buttons(500, 365, 200, 80, 'shop2.png', 'shop1.png', 2)
        self.buttons(500, 465, 200, 80, 'exit1.png', 'exit2.png', 3)

    def start_screen(self):
        pygame.mixer.music.load('data/start_mus.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)

        fon = pygame.transform.scale(self.load_image('start_back.jpg'), (self.WIDTH, self.HEIGHT))
        self.screen.blit(fon, (0, 0))
        fon = pygame.transform.scale(self.load_image('1.png'), (250, 100))
        self.screen.blit(fon, (480, 30))

        while True:
            for event in pygame.event.get():
                self.buttons(500, 165, 200, 80, 'play2.png', 'play1.png', 0)
                self.buttons(500, 265, 200, 80, 'train2.png', 'train1.png', 1)
                self.buttons(500, 365, 200, 80, 'shop2.png', 'shop1.png', 2)
                self.buttons(500, 465, 200, 80, 'exit1.png', 'exit2.png', 3)
                self.sounds_point()

                if self.sound_count % 2 == 0:
                    self.update_image()
                    sound_icon = pygame.transform.scale(self.load_image('sound2.png'), (25, 25))
                    self.screen.blit(sound_icon, (1150, 750))
                    pygame.mixer.music.pause()
                else:
                    self.update_image()
                    sound_icon = pygame.transform.scale(self.load_image('sound1.png'), (25, 25))
                    self.screen.blit(sound_icon, (1150, 750))
                    pygame.mixer.music.unpause()

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.flip()
            self.clock.tick(self.FPS)


Start()
