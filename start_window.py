import os
import sys
import pygame
from random import choice
from easybot import EasyBot
from normalbot import NormalBot
from hardbot import HardBot

my_cards = []
bot_cards = []
list = []
bot_place_occupied = []
my_place_occupied = []
inventory_player = [(7, 3, 'card_1_1'), (2, 6, 'card_1_2'), (3, 3, 'card_1_3')]


class Start:
    def __init__(self):
        pygame.init()
        self.size = self.WIDTH, self.HEIGHT = 1200, 800
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.but_sound = pygame.mixer.Sound('data/but_sound.mp3')
        pygame.display.set_caption('TerriableAge')
        self.FPS = 60
        self.sound_count = 1
        self.start_music = 'data/start_mus.mp3'
        self.def_music = 'data/def_mus.mp3'
        self.win_music = 'data/winn_mus.mp3'

        self.inventory_card = pygame.sprite.Group()
        self.vil_x, self.vil_y, self.x_old, self.y_old, self.x_new, self.y_new = 1000, 550, 0, 0, 0, 0
        self.my_hp = 30
        self.bot_hp = 30
        self.new_place = 0
        self.new_card = (0, 0)
        self.vil = ()
        self.sound_count = 1
        self.move = False
        self.movement = False
        self.bot = 'hard'
        self.close = False
        self.ch = False
        self.deck = [(3, 4, 'card_1_1'), (2, 2, 'card_1_2'), (3, 1, 'card_1_3'), (1, 3, 'card_1_4'), (3, 2, 'card_1_5'),
                     (1, 1, 'card_1_1'), (3, 3, 'card_1_2'), (2, 3, 'card_1_3'), (1, 4, 'card_1_4'), (2, 4, 'card_1_5'),
                     (3, 4, 'card_1_1'), (2, 2, 'card_1_2'), (3, 1, 'card_1_3'), (1, 3, 'card_1_4'), (3, 2, 'card_1_5'),
                     (1, 1, 'card_1_1'), (3, 3, 'card_1_2'), (2, 3, 'card_1_3'), (1, 4, 'card_1_4'), (2, 4, 'card_1_5')]

        # self.deck = [(1, 1, 'card_1_1'), (1, 2, 'card_1_2'), (1, 3, 'card_1_3'), (1, 4, 'card_1_4'), (1, 5, 'card_1_5'),
        # (2, 1, 'card_2_1'), (2, 2, 'card_2_2'), (2, 3, 'card_2_3'), (2, 4, 'card_2_4'), (2, 5, 'card_2_5'),
        # (3, 1, 'card_3_1'), (3, 2, 'card_3_2'), (3, 3, 'card_3_3'), (3, 4, 'card_3_4'), (3, 5, 'card_3_5')]
        self.eb = EasyBot()
        self.nb = NormalBot()
        self.hb = HardBot()
        self.paused = False
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
                        self.start_screen2()
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
        self.buttons(500, 265, 200, 80, 'train2.png', 'train1.png', 1)
        self.buttons(500, 365, 200, 80, 'shop2.png', 'shop1.png', 2)
        self.buttons(500, 465, 200, 80, 'exit1.png', 'exit2.png', 3)
        if self.sound_count % 2 == 0:
            sound_icon = pygame.transform.scale(self.load_image('sound2.png'), (25, 25))
            self.screen.blit(sound_icon, (1150, 30))
        else:
            sound_icon = pygame.transform.scale(self.load_image('sound1.png'), (25, 25))
            self.screen.blit(sound_icon, (1150, 30))

    '''Отображение окна выбора сложности(уровень)'''

    def update_image2(self):
        fon = pygame.transform.scale(self.load_image('start_back.jpg'), (self.WIDTH, self.HEIGHT))
        self.screen.blit(fon, (0, 0))
        fon = pygame.transform.scale(self.load_image('levels.png'), (250, 100))
        self.screen.blit(fon, (480, 30))
        self.buttons2(500, 165, 200, 80, 'normal_lvl2.png', 'normal_lvl.png', 0)
        self.buttons2(500, 265, 200, 80, 'hard_vlv2.png', 'hard_lvl.png', 1)
        self.buttons2(500, 365, 200, 80, 'rules_lvl2.png', 'rules_lvl.png', 2)
        self.buttons2(500, 465, 200, 80, 'menu_lvl2.png', 'menu_lvl.png', 3)
        if self.sound_count % 2 == 0:
            sound_icon = pygame.transform.scale(self.load_image('sound2.png'), (25, 25))
            self.screen.blit(sound_icon, (1150, 30))
        else:
            sound_icon = pygame.transform.scale(self.load_image('sound1.png'), (25, 25))
            self.screen.blit(sound_icon, (1150, 30))

    '''Кнопки на окне проигрыша'''

    def buttons_def(self, x, y, width, height, photo_name1, photo_name2, num):
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
                        self.start_screen2()
            else:
                fon = pygame.transform.scale(self.load_image(photo_name2), (width, height))
                self.screen.blit(fon, (x, y))
        else:
            fon = pygame.transform.scale(self.load_image(photo_name2), (width, height))
            self.screen.blit(fon, (x, y))

    def buttons2(self, x, y, width, height, photo_name1, photo_name2, num):
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
                        self.run()
            else:
                fon = pygame.transform.scale(self.load_image(photo_name2), (width, height))
                self.screen.blit(fon, (x, y))
        else:
            fon = pygame.transform.scale(self.load_image(photo_name2), (width, height))
            self.screen.blit(fon, (x, y))

    '''Отображение окна проигрыша'''

    def update_image_def(self):
        fon = pygame.transform.scale(self.load_image('def_back.jpg'), (self.WIDTH, self.HEIGHT))
        self.screen.blit(fon, (0, 0))
        text = pygame.transform.scale(self.load_image('defeat_img.png'), (500, 250))
        self.screen.blit(text, (360, -10))
        font = pygame.font.Font(None, 70)
        text = font.render(f"Ваш результат: {0}", True, (137, 129, 118))
        self.screen.blit(text, (425, 220))
        self.buttons_def(1000, 700, 170, 90, 'def_cont_2.png', 'def_cont.png', 0)
        if self.sound_count % 2 == 0:
            sound_icon = pygame.transform.scale(self.load_image('sound2.png'), (25, 25))
            self.screen.blit(sound_icon, (1150, 30))
        else:
            sound_icon = pygame.transform.scale(self.load_image('sound1.png'), (25, 25))
            self.screen.blit(sound_icon, (1150, 30))

    '''Цикл окна меню'''

    def start_screen(self):
        pygame.mixer.music.load(self.start_music)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)
        while True:
            for event in pygame.event.get():
                self.update_image()
                self.sounds_point()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.flip()
            self.clock.tick(self.FPS)

    '''Цикл окна с уровнями'''
    def start_screen2(self):
        pygame.mixer.music.load(self.start_music)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)
        while True:
            for event in pygame.event.get():
                self.update_image2()
                self.sounds_point()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.flip()
            self.clock.tick(self.FPS)

    '''Цикл окна проигрыша'''

    def start_screen_def(self):
        pygame.mixer.music.load(self.def_music)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)
        while True:
            for event in pygame.event.get():
                self.update_image_def()
                self.sounds_point()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.flip()
            self.clock.tick(self.FPS)

    def buttons_win(self, x, y, width, height, photo_name1, photo_name2, num):
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
                        self.start_screen2()
            else:
                fon = pygame.transform.scale(self.load_image(photo_name2), (width, height))
                self.screen.blit(fon, (x, y))
        else:
            fon = pygame.transform.scale(self.load_image(photo_name2), (width, height))
            self.screen.blit(fon, (x, y))

    def update_image_win(self):
        fon = pygame.transform.scale(self.load_image('win_back.jpg'), (self.WIDTH, self.HEIGHT))
        self.screen.blit(fon, (0, 0))
        text = pygame.transform.scale(self.load_image('victory_img.png'), (500, 250))
        self.screen.blit(text, (360, -10))

        font = pygame.font.Font(None, 70)
        n = 10
        text = font.render(f"Ваш результат: {n}", True, (216, 112, 147))
        self.screen.blit(text, (420, 220))
        self.buttons_win(1000, 700, 170, 90, 'cont_win_2.png', 'cont_win.png', 0)
        if self.sound_count % 2 == 0:
            sound_icon = pygame.transform.scale(self.load_image('sound2.png'), (25, 25))
            self.screen.blit(sound_icon, (1150, 30))
        else:
            sound_icon = pygame.transform.scale(self.load_image('sound1.png'), (25, 25))
            self.screen.blit(sound_icon, (1150, 30))

    def start_screen_win(self):
        pygame.mixer.music.load(self.win_music)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)
        self.update_image_win()
        while True:
            for event in pygame.event.get():
                self.update_image_win()
                self.sounds_point()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.flip()
            self.clock.tick(self.FPS)


    '''Основная часть игры'''
    def give_card(self, desk, inventory_player):
        # ф-ция добовления карт в инвентарь игрока
        if desk:
            if len(inventory_player) < 6 and not self.move:
                card = choice(desk)
                del self.deck[desk.index(card)]
                inventory_player.append(card)
                self.updete_image_main(self.deck, card, None)

    def updete_image_main(self, desk=False, cart=None, index=None):
        image = self.load_image('background.jpg')
        image1 = pygame.transform.scale(image, (self.WIDTH, self.HEIGHT))
        self.screen.blit(image1, (0, 0))

        if None != index:
            self.vil = inventory_player[index]
            del inventory_player[index]
        if self.vil and not self.movement:
            image = self.load_image(self.vil[2] + '.png')
            image1 = pygame.transform.scale(image, (150, 225))
            self.spr = self.screen.blit(image1, (1000, 550))
            dm, hp, img = self.vil
            font = pygame.font.Font(None, 30)
            text = font.render(f"{dm}                 {hp}", True, (0, 0, 0))
            self.screen.blit(text, (1015, 745))
            self.vil_x, self.vil_y = 1000, 550
        image = self.load_image('pole.png')
        image1 = pygame.transform.scale(image, (150, 225))

        for i in range(150, 950, 200):
            self.screen.blit(image1, (i, 100))
            pole = self.screen.blit(image1, (i, 450))
            if pole not in list:
                list.append(pole)
        if my_cards:
            for i in my_cards:
                name_image = i[2]
                image = self.load_image(name_image + '.png')
                image1 = pygame.transform.scale(image, (150, 225))
                if i[-1] == 0:
                    self.screen.blit(image1, (150, 450))
                    font = pygame.font.Font(None, 30)
                    text = font.render(f"{i[0]}                 {i[1]}", True, (0, 0, 0))
                    self.screen.blit(text, (165, 645))
                elif i[-1] == 1:
                    self.screen.blit(image1, (350, 450))
                    font = pygame.font.Font(None, 30)
                    text = font.render(f"{i[0]}                 {i[1]}", True, (0, 0, 0))
                    self.screen.blit(text, (365, 645))
                elif i[-1] == 2:
                    self.screen.blit(image1, (550, 450))
                    font = pygame.font.Font(None, 30)
                    text = font.render(f"{i[0]}                 {i[1]}", True, (0, 0, 0))
                    self.screen.blit(text, (565, 645))
                elif i[-1] == 3:
                    self.screen.blit(image1, (750, 450))
                    font = pygame.font.Font(None, 30)
                    text = font.render(f"{i[0]}                 {i[1]}", True, (0, 0, 0))
                    self.screen.blit(text, (765, 645))
                else:
                    del list[list.index(i)]
        if bot_cards:
            for i in bot_cards:
                name_image = i[2]
                image = self.load_image(name_image + '.png')
                image1 = pygame.transform.scale(image, (150, 225))
                if i[-1] == 0:
                    self.screen.blit(image1, (150, 100))
                    font = pygame.font.Font(None, 30)
                    text = font.render(f"{i[0]}                 {i[1]}", True, (0, 0, 0))
                    self.screen.blit(text, (165, 295))
                elif i[-1] == 1:
                    self.screen.blit(image1, (350, 100))
                    font = pygame.font.Font(None, 30)
                    text = font.render(f"{i[0]}                 {i[1]}", True, (0, 0, 0))
                    self.screen.blit(text, (365, 295))
                elif i[-1] == 2:
                    self.screen.blit(image1, (550, 100))
                    font = pygame.font.Font(None, 30)
                    text = font.render(f"{i[0]}                 {i[1]}", True, (0, 0, 0))
                    self.screen.blit(text, (565, 295))
                elif i[-1] == 3:
                    self.screen.blit(image1, (750, 100))
                    font = pygame.font.Font(None, 30)
                    text = font.render(f"{i[0]}                 {i[1]}", True, (0, 0, 0))
                    self.screen.blit(text, (765, 295))
                else:
                    del list[list.index(i)]

        for i in range(len(inventory_player)):
            x = 400 + i * 30
            y = 650
            # исправить когда будут нарисованны текстуры
            name_image = inventory_player[i][2]
            image = self.load_image(name_image + '.png')
            image1 = pygame.transform.scale(image, (150, 225))
            self.screen.blit(image1, (x, y))
        image = self.load_image('move.png')
        image1 = pygame.transform.scale(image, (100, 50))
        self.screen.blit(image1, (10, 360))
        if None != cart:
            pass
        if self.deck:
            image = self.load_image('carta3.png')
            image1 = pygame.transform.scale(image, (200, 300))
            self.screen.blit(image1, (990, 200))
            font = pygame.font.Font(None, 30)
            text = font.render(f"{len(self.deck)}/35", True, (255, 255, 255))
            self.screen.blit(text, (1100, 530))
        if self.my_hp > 0 and self.bot_hp > 0:
            font = pygame.font.Font(None, 30)
            text = font.render(f"{self.my_hp}/{self.bot_hp}", True, (255, 255, 255))
            self.screen.blit(text, (1100, 30))
        elif self.my_hp < 0:
            self.start_screen_def()
        elif self.bot_hp < 0:
            self.start_screen_win()
        if self.movement:
            self.dragging()

        if self.sound_count % 2 == 0:
            sound_icon = pygame.transform.scale(self.load_image('sound2.png'), (25, 25))
            self.screen.blit(sound_icon, (1155, 30))
        else:
            sound_icon = pygame.transform.scale(self.load_image('sound1.png'), (25, 25))
            self.screen.blit(sound_icon, (1155, 30))

        pygame.display.flip()
        self.clock.tick(60)

    def inventory_show(self):
        # затемнение фона
        s = pygame.Surface((self.WIDTH, self.HEIGHT))
        s.set_alpha(180)
        s.fill((30, 27, 24))
        self.screen.blit(s, (0, 0))

        image = self.load_image('cancle.png')
        image1 = pygame.transform.scale(image, (100, 50))
        self.screen.blit(image1, (10, 360))

        for i in range(2, len(inventory_player) + 2):
            if i <= 4:
                y = 100
            else:
                y = 400
            if i == 2 or i == 5:
                x = 200
            elif i == 3 or i == 6:
                x = 500
            elif i == 4 or i == 7:
                x = 800

            name_image = inventory_player[i - 2][2]
            image = self.load_image(name_image + '.png')
            image1 = pygame.transform.scale(image, (150, 225))
            self.screen.blit(image1, (x, y))
            dm, hp, img = inventory_player[i - 2]
            font = pygame.font.Font(None, 30)
            text = font.render(f"{dm}                 {hp}", True, (0, 0, 0))
            self.screen.blit(text, (x + 15, y + 195))

    def click_card(self):
        index = None
        mouse_pos = self.mouse_pos
        if (mouse_pos[0] >= 10 and not 90 < mouse_pos[0]) and (
                mouse_pos[1] >= 360 and not 400 < mouse_pos[1]):
            self.ch = False
            self.updete_image_main(self.deck, None, None)
        elif (mouse_pos[0] >= 200 and not 350 < mouse_pos[0]) and (
                mouse_pos[1] >= 100 and not 325 < mouse_pos[1]) and len(inventory_player) >= 1:
            index = 0
        elif (mouse_pos[0] >= 500 and not 650 < mouse_pos[0]) and (
                mouse_pos[1] >= 100 and not 325 < mouse_pos[1]) and len(inventory_player) >= 2:
            index = 1
        elif (mouse_pos[0] >= 800 and not 950 < mouse_pos[0]) and (
                mouse_pos[1] >= 100 and not 325 < mouse_pos[1]) and len(inventory_player) >= 3:
            index = 2
        elif (mouse_pos[0] >= 200 and not 350 < mouse_pos[0]) and (
                mouse_pos[1] >= 400 and not 625 < mouse_pos[1]) and len(inventory_player) >= 4:
            index = 3
        elif (mouse_pos[0] >= 500 and not 650 < mouse_pos[0]) and (
                mouse_pos[1] >= 400 and not 625 < mouse_pos[1]) and len(inventory_player) >= 5:
            index = 4
        elif (mouse_pos[0] >= 800 and not 950 < mouse_pos[0]) and (
                mouse_pos[1] >= 400 and not 625 < mouse_pos[1]) and len(inventory_player) >= 6:
            index = 5
        if index != None:
            self.ch = False
            self.movement = False
            self.updete_image_main(self.deck, None, index)

    def dragging(self, new_vil=None):
        if self.vil:
            image = self.load_image(self.vil[2] + '.png')
            image1 = pygame.transform.scale(image, (150, 225))
            self.spr = self.screen.blit(image1, (self.vil_x, self.vil_y))
            font = pygame.font.Font(None, 30)
            text = font.render(f"{self.vil[0]}                 {self.vil[1]}", True, (0, 0, 0))
            self.screen.blit(text, (self.vil_x + 15, self.vil_y + 195))

    def functions(self):
        mouse_pos = self.mouse_pos
        if (mouse_pos[0] >= 990 and not 1190 < mouse_pos[0]) and (
                mouse_pos[1] >= 250 and not 550 < mouse_pos[1]):
            self.give_card(self.deck, inventory_player)
            self.move = True
        if (mouse_pos[0] >= 10 and not 90 < mouse_pos[0]) and (
                mouse_pos[1] >= 360 and not 400 < mouse_pos[1]):
            self.move = False
            self.attack('player')
            if self.bot == 'easy':
                self.easy_bot()
            elif self.bot == 'normal':
                self.normal_bot()
            elif self.bot == 'hard':
                self.hard_bot()
        if (mouse_pos[0] >= 400 and not 700 < mouse_pos[0]) and (
                mouse_pos[1] >= 650 and not 800 < mouse_pos[1]):
            self.ch = True
            self.inventory_show()
        if self.vil:
            if self.vil_x < self.event.pos[0] < self.vil_x + 150 and self.vil_y < self.event.pos[
                1] < self.vil_y + 225 and self.vil[2]:
                if self.movement == False:
                    self.movement = True
                else:
                    if self.spr.collidelist(list) + 1:
                        if self.spr.collidelist(list) not in my_place_occupied:
                            my_place_occupied.append(self.spr.collidelist(list))
                            self.new_place = self.spr.collidelist(list)
                            dm, hp, img = self.vil
                            self.new_card = dm, hp
                            my_cards.append((dm, hp, img, self.spr.collidelist(list)))
                            self.vil = ()
                    self.movement = False
                    self.updete_image_main()

    def easy_bot(self):
        self.bot_card, self.place_bot, new_deck = self.eb.return_func(self.deck)
        if self.bot_card != None and self.place_bot != None:
            dm, hp, img = self.bot_card
            bot_cards.append((dm, hp, img, self.place_bot))
            bot_place_occupied.append(self.place_bot)
            self.deck = new_deck
        self.attack('bot')

    def normal_bot(self):
        self.bot_card, self.place_bot, new_deck = self.nb.return_func(self.deck, self.new_place, self.new_card)
        if self.bot_card != None and self.place_bot != None:
            dm, hp, img = self.bot_card
            bot_cards.append((dm, hp, img, self.place_bot))
            bot_place_occupied.append(self.place_bot)
            self.deck = new_deck
        self.attack('bot')

    def hard_bot(self):
        self.bot_card, self.place_bot, new_deck = self.hb.return_func(self.deck, self.new_place, self.new_card)
        if self.bot_card != None and self.place_bot != None:
            dm, hp, img = self.bot_card
            bot_cards.append((dm, hp, img, self.place_bot))
            bot_place_occupied.append(self.place_bot)
            self.deck = new_deck
        self.attack('bot')

    def attack(self, side):
        if side == 'bot':
            for i in bot_place_occupied:
                bot_dm, bot_hp, bot_img, bot_ind = bot_cards[bot_place_occupied.index(i)]
                if i in my_place_occupied:
                    try:
                        my_dm, my_hp, my_img, my_ind = my_cards[my_place_occupied.index(i)]
                        if my_hp - bot_dm <= 0:
                            del my_cards[my_place_occupied.index(i)]
                            del my_place_occupied[my_place_occupied.index(i)]
                        else:
                            my_cards[my_place_occupied.index(i)] = my_dm, my_hp - bot_dm, my_img, my_ind
                    except IndexError:
                        self.my_hp -= bot_dm
                else:
                    self.my_hp -= bot_dm
        elif side == 'player':
            for i in my_place_occupied:
                my_dm, my_hp, my_img, my_ind = my_cards[my_place_occupied.index(i)]
                if i in bot_place_occupied:
                    try:
                        bot_dm, bot_hp, bot_img, bot_ind = bot_cards[bot_place_occupied.index(i)]
                        if bot_hp - my_dm <= 0:
                            if self.bot == 'easy':
                                self.eb.choice_card(bot_place_occupied.index(i))
                                del bot_cards[bot_place_occupied.index(i)]
                                del bot_place_occupied[bot_place_occupied.index(i)]
                            elif self.bot == 'normal':
                                self.nb.choice_card(bot_place_occupied.index(i))
                                del bot_cards[bot_place_occupied.index(i)]
                                del bot_place_occupied[bot_place_occupied.index(i)]
                            elif self.bot == 'hard':
                                self.hb.choice_card(bot_place_occupied.index(i))
                                del bot_cards[bot_place_occupied.index(i)]
                                del bot_place_occupied[bot_place_occupied.index(i)]
                        else:
                            bot_cards[bot_place_occupied.index(i)] = bot_dm, bot_hp - my_dm, bot_img, bot_ind
                    except IndexError:
                        self.bot_hp -= my_dm
                else:
                    self.bot_hp -= my_dm
        self.updete_image_main()

    def pause(self):
        self.paused = True
        while self.paused:
            for self.event in pygame.event.get():
                if self.event.type == pygame.QUIT:
                    pygame.quit()

            font = pygame.font.Font(None, 70)
            text = font.render(f'Нажмите пробел, чтобы продолжить', True, (255, 255, 255))
            self.screen.blit(text, (180, 220))

            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                self.paused = False

            pygame.display.update()
            self.clock.tick(15)
        self.updete_image_main()

    def sounds_point_main(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if 1150 < mouse[0] < 1150 + 25:
            if 30 < mouse[1] < 30 + 25:
                if click[0] == 1:
                    self.sound_count += 1
                    if self.sound_count % 2 == 0:
                        pygame.mixer.music.pause()
                        self.updete_image_main()
                    else:
                        pygame.mixer.music.unpause()
                        self.updete_image_main()

    def buttons_main(self, x, y, width, height, photo_name1, photo_name2):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + width:
            if y < mouse[1] < y + height:
                fon = pygame.transform.scale(self.load_image(photo_name1), (width, height))
                self.screen.blit(fon, (x, y))
                if click[0] == 1:
                    pygame.mixer.Sound.play(self.but_sound)
                    pygame.time.delay(300)
            else:
                fon = pygame.transform.scale(self.load_image(photo_name2), (width, height))
                self.screen.blit(fon, (x, y))
        else:
            fon = pygame.transform.scale(self.load_image(photo_name2), (width, height))
            self.screen.blit(fon, (x, y))

    def run(self, update=False):
        pygame.mixer.music.load('data/play_mus.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)
        if update == False:
            self.updete_image_main(self.deck)
        while not self.close:
            for self.event in pygame.event.get():
                self.sounds_point_main()
                if self.event.type == pygame.QUIT:
                    self.close = True
                if self.event.type == pygame.KEYDOWN:
                    if self.event.key == pygame.K_ESCAPE:
                        self.pause()
                if self.event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_pos = pygame.mouse.get_pos()
                    if not self.ch:
                        self.functions()
                    if self.ch:
                        self.click_card()
                if self.event.type == pygame.MOUSEMOTION:
                    if self.movement:
                        self.x_new, self.y_new = self.event.rel
                        self.vil_x, self.vil_y = self.vil_x + self.x_new, self.vil_y + self.y_new
                        self.updete_image_main()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()


Start()
