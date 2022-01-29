import os
import sys
import pygame
from random import choice
from easybot import EasyBot
from normalbot import NormalBot
from hardbot import HardBot


class Levels:
    def __init__(self):
        self.size = self.WIDTH, self.HEIGHT = 1200, 800
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.but_sound = pygame.mixer.Sound('data/musics/but_sound.mp3')
        self.FPS = 60
        self.sound_count = 1
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
                        BaseGame('easy').run()
                    if num == 1:
                        BaseGame('normal').run()
                    if num == 2:
                        BaseGame('hard').run()
                    if num == 3:
                        from start_window import Start
                        Start()
            else:
                fon = pygame.transform.scale(self.load_image(f'buttons_img/{photo_name2}'), (width, height))
                self.screen.blit(fon, (x, y))
        else:
            fon = pygame.transform.scale(self.load_image(f'buttons_img/{photo_name2}'), (width, height))
            self.screen.blit(fon, (x, y))

    '''Включение и выклчюение звука'''

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

    '''Перирисовка изображения'''

    def update_image(self):
        fon = pygame.transform.scale(self.load_image('backgrounds_img/start_back.jpg'), (self.WIDTH, self.HEIGHT))
        self.screen.blit(fon, (0, 0))
        fon = pygame.transform.scale(self.load_image('icons_img/levels.png'), (250, 100))
        self.screen.blit(fon, (480, 30))
        self.buttons(500, 165, 200, 80, 'easy2.png', 'easy.png', 0)
        self.buttons(500, 265, 200, 80, 'normal_lvl2.png', 'normal_lvl.png', 1)
        self.buttons(500, 365, 200, 80, 'hard_vlv2.png', 'hard_lvl.png', 2)
        self.buttons(500, 465, 200, 80, 'menu_lvl2.png', 'menu_lvl.png', 3)
        if self.sound_count % 2 == 0:
            sound_icon = pygame.transform.scale(self.load_image('buttons_img/sound2.png'), (25, 25))
            self.screen.blit(sound_icon, (1150, 30))
        else:
            sound_icon = pygame.transform.scale(self.load_image('buttons_img/sound1.png'), (25, 25))
            self.screen.blit(sound_icon, (1150, 30))

        '''Основной цикл окна'''

    def start_screen(self):
        pygame.mixer.music.load('data/musics/start_mus.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)
        while True:
            for event in pygame.event.get():
                self.update_image()
                self.sounds_point()
                if event.type == pygame.QUIT:
                    sys.exit()
            pygame.display.flip()
            self.clock.tick(self.FPS)


class BaseGame:
    def __init__(self, level):
        self.size = self.width, self.height = 1200, 800
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.inventory_card = pygame.sprite.Group()
        self.vil_x, self.vil_y, self.x_old, self.y_old, self.x_new, self.y_new = 1000, 550, 0, 0, 0, 0
        pygame.display.set_caption('TerriableAge')
        self.my_hp = 30
        self.bot_hp = 30
        self.new_place = 0
        self.new_card = (0, 0)
        self.but_sound = pygame.mixer.Sound('data/musics/but_sound.mp3')
        self.sound_count = 1
        self.vil = ()
        self.move = False
        self.movement = False
        self.bot = level
        self.close = False
        self.ch = False
        self.deck = [(3, 4, 'card_1_1'), (2, 2, 'card_1_2'), (3, 1, 'card_1_3'), (1, 3, 'card_1_4'), (3, 2, 'card_1_5'),
                     (1, 1, 'card_1_1'), (3, 3, 'card_1_2'), (2, 3, 'card_1_3'), (1, 4, 'card_1_4'), (2, 4, 'card_1_5'),
                     (3, 4, 'card_1_1'), (2, 2, 'card_1_2'), (3, 1, 'card_1_3'), (1, 3, 'card_1_4'), (3, 2, 'card_1_5'),
                     (1, 1, 'card_1_1'), (3, 3, 'card_1_2'), (2, 3, 'card_1_3'), (1, 4, 'card_1_4'), (2, 4, 'card_1_5')]
        self.my_cards = []
        self.bot_cards = []
        self.list = []
        self.bot_place_occupied = []
        self.my_place_occupied = []
        self.inventory_player = []

        self.eb = EasyBot()
        self.nb = NormalBot()
        self.hb = HardBot()
        self.updete_image()

    def load_image(self, name):
        # ф-ция открывания картинок
        fullname = os.path.join('data/', name)
        image = pygame.image.load(fullname)
        return image

    def give_card(self, desk, inventory_player):
        # ф-ция добовления карт в инвентарь игрока
        if desk:
            if len(inventory_player) < 6 and not self.move:
                card = choice(desk)
                del self.deck[desk.index(card)]
                inventory_player.append(card)
                self.updete_image(self.deck, card, None)

    def updete_image(self, desk=False, cart=None, index=None):
        image = self.load_image('backgrounds_img/background.jpg')
        image1 = pygame.transform.scale(image, (self.width, self.height))
        self.screen.blit(image1, (0, 0))

        if None != index:
            self.vil = self.inventory_player[index]
            del self.inventory_player[index]
        if self.vil and not self.movement:
            image = self.load_image(f'cards_img/{self.vil[2]}.png')
            image1 = pygame.transform.scale(image, (150, 225))
            self.spr = self.screen.blit(image1, (1000, 550))
            dm, hp, img = self.vil
            font = pygame.font.Font(None, 30)
            text = font.render(f"{dm}                 {hp}", True, (0, 0, 0))
            self.screen.blit(text, (1015, 745))
            self.vil_x, self.vil_y = 1000, 550
        image = self.load_image('icons_img/pole.png')
        image1 = pygame.transform.scale(image, (150, 225))

        for i in range(150, 950, 200):
            self.screen.blit(image1, (i, 100))
            pole = self.screen.blit(image1, (i, 450))
            if pole not in self.list:
                self.list.append(pole)
        if self.my_cards:
            for i in self.my_cards:
                name_image = i[2]
                image = self.load_image(f'cards_img/{name_image}.png')
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
                    del self.list[self.list.index(i)]
        if self.bot_cards:
            for i in self.bot_cards:
                name_image = i[2]
                image = self.load_image(f'cards_img/{name_image}.png')
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
                    del self.list[self.list.index(i)]

        for i in range(len(self.inventory_player)):
            x = 400 + i * 30
            y = 650
            # исправить когда будут нарисованны текстуры
            name_image = self.inventory_player[i][2]
            image = self.load_image(f'cards_img/{name_image}.png')
            image1 = pygame.transform.scale(image, (150, 225))
            self.screen.blit(image1, (x, y))
        if None != cart:
            pass
        if self.deck:
            image = self.load_image('icons_img/carta3.png')
            image1 = pygame.transform.scale(image, (200, 300))
            self.screen.blit(image1, (990, 200))
            font = pygame.font.Font(None, 30)
            text = font.render(f"{len(self.deck)}/35", True, (255, 255, 255))
            self.screen.blit(text, (1100, 530))
        if self.my_hp > 0 and self.bot_hp > 0:
            font = pygame.font.Font(None, 30)
            text = font.render(f"{self.my_hp}/{self.bot_hp}", True, (255, 255, 255))
            self.screen.blit(text, (1000, 30))
            image = self.load_image('icons_img/heart.png')
            image1 = pygame.transform.scale(image, (25, 25))
            self.screen.blit(image1, (1055, 25))

        elif self.my_hp < 0:
            from final_wind_def import Lose
            Lose()
        elif self.bot_hp < 0:
            self.counts()
            from final_window_win import Winner
            Winner()
        if self.movement:
            self.dragging()

        if self.sound_count % 2 == 0:
            sound_icon = pygame.transform.scale(self.load_image('buttons_img/sound2.png'), (25, 25))
            self.screen.blit(sound_icon, (1150, 30))
        else:
            sound_icon = pygame.transform.scale(self.load_image('buttons_img/sound1.png'), (25, 25))
            self.screen.blit(sound_icon, (1150, 30))

        pygame.display.flip()
        self.clock.tick(60)

    def inventory_show(self):
        # затемнение фона
        s = pygame.Surface((self.width, self.height))
        s.set_alpha(180)
        s.fill((30, 27, 24))
        self.screen.blit(s, (0, 0))

        for i in range(2, len(self.inventory_player) + 2):
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

            name_image = self.inventory_player[i - 2][2]
            image = self.load_image(f'cards_img/{name_image}.png')
            image1 = pygame.transform.scale(image, (150, 225))
            self.screen.blit(image1, (x, y))
            dm, hp, img = self.inventory_player[i - 2]
            font = pygame.font.Font(None, 30)
            text = font.render(f"{dm}                 {hp}", True, (0, 0, 0))
            self.screen.blit(text, (x + 15, y + 195))

    def click_card(self):
        index = None
        mouse_pos = self.mouse_pos
        if (mouse_pos[0] >= 10 and not 90 < mouse_pos[0]) and (
                mouse_pos[1] >= 360 and not 400 < mouse_pos[1]):
            self.ch = False
            self.updete_image(self.deck, None, None)
        elif (mouse_pos[0] >= 200 and not 350 < mouse_pos[0]) and (
                mouse_pos[1] >= 100 and not 325 < mouse_pos[1]) and len(self.inventory_player) >= 1:
            index = 0
        elif (mouse_pos[0] >= 500 and not 650 < mouse_pos[0]) and (
                mouse_pos[1] >= 100 and not 325 < mouse_pos[1]) and len(self.inventory_player) >= 2:
            index = 1
        elif (mouse_pos[0] >= 800 and not 950 < mouse_pos[0]) and (
                mouse_pos[1] >= 100 and not 325 < mouse_pos[1]) and len(self.inventory_player) >= 3:
            index = 2
        elif (mouse_pos[0] >= 200 and not 350 < mouse_pos[0]) and (
                mouse_pos[1] >= 400 and not 625 < mouse_pos[1]) and len(self.inventory_player) >= 4:
            index = 3
        elif (mouse_pos[0] >= 500 and not 650 < mouse_pos[0]) and (
                mouse_pos[1] >= 400 and not 625 < mouse_pos[1]) and len(self.inventory_player) >= 5:
            index = 4
        elif (mouse_pos[0] >= 800 and not 950 < mouse_pos[0]) and (
                mouse_pos[1] >= 400 and not 625 < mouse_pos[1]) and len(self.inventory_player) >= 6:
            index = 5
        if index != None:
            self.ch = False
            self.movement = False
            self.updete_image(self.deck, None, index)

    def dragging(self, new_vil=None):
        if self.vil:
            image = self.load_image(f'cards_img/{self.vil[2]}.png')
            image1 = pygame.transform.scale(image, (150, 225))
            self.spr = self.screen.blit(image1, (self.vil_x, self.vil_y))
            font = pygame.font.Font(None, 30)
            text = font.render(f"{self.vil[0]}                 {self.vil[1]}", True, (0, 0, 0))
            self.screen.blit(text, (self.vil_x + 15, self.vil_y + 195))

    def functions(self):
        mouse_pos = self.mouse_pos
        if (mouse_pos[0] >= 990 and not 1190 < mouse_pos[0]) and (
                mouse_pos[1] >= 250 and not 550 < mouse_pos[1]):
            self.give_card(self.deck, self.inventory_player)
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
                    if self.spr.collidelist(self.list) + 1:
                        if self.spr.collidelist(self.list) not in self.my_place_occupied:
                            self.my_place_occupied.append(self.spr.collidelist(self.list))
                            self.new_place = self.spr.collidelist(self.list)
                            dm, hp, img = self.vil
                            self.new_card = dm, hp
                            self.my_cards.append((dm, hp, img, self.spr.collidelist(self.list)))
                            self.vil = ()
                    self.movement = False
                    self.updete_image()

    def easy_bot(self):
        self.bot_card, self.place_bot, new_deck = self.eb.return_func(self.deck)
        if self.bot_card != None and self.place_bot != None:
            dm, hp, img = self.bot_card
            self.bot_cards.append((dm, hp, img, self.place_bot))
            self.bot_place_occupied.append(self.place_bot)
            self.deck = new_deck
        self.attack('bot')

    def normal_bot(self):
        self.bot_card, self.place_bot, new_deck = self.nb.return_func(self.deck, self.new_place, self.new_card)
        if self.bot_card != None and self.place_bot != None:
            dm, hp, img = self.bot_card
            self.bot_cards.append((dm, hp, img, self.place_bot))
            self.bot_place_occupied.append(self.place_bot)
            self.deck = new_deck
        self.attack('bot')

    def hard_bot(self):
        self.bot_card, self.place_bot, new_deck = self.hb.return_func(self.deck, self.new_place, self.new_card)
        if self.bot_card != None and self.place_bot != None:
            dm, hp, img = self.bot_card
            self.bot_cards.append((dm, hp, img, self.place_bot))
            self.bot_place_occupied.append(self.place_bot)
            self.deck = new_deck
        self.attack('bot')

    def attack(self, side):
        if side == 'bot':
            for i in self.bot_place_occupied:
                bot_dm, bot_hp, bot_img, bot_ind = self.bot_cards[self.bot_place_occupied.index(i)]
                if i in self.my_place_occupied:
                    try:
                        my_dm, my_hp, my_img, my_ind = self.my_cards[self.my_place_occupied.index(i)]
                        if my_hp - bot_dm <= 0:
                            del self.my_cards[self.my_place_occupied.index(i)]
                            del self.my_place_occupied[self.my_place_occupied.index(i)]
                        else:
                            self.my_cards[self.my_place_occupied.index(i)] = my_dm, my_hp - bot_dm, my_img, my_ind
                    except IndexError:
                        self.my_hp -= bot_dm
                else:
                    self.my_hp -= bot_dm
        elif side == 'player':
            for i in self.my_place_occupied:
                my_dm, my_hp, my_img, my_ind = self.my_cards[self.my_place_occupied.index(i)]
                if i in self.bot_place_occupied:
                    try:
                        bot_dm, bot_hp, bot_img, bot_ind = self.bot_cards[self.bot_place_occupied.index(i)]
                        if bot_hp - my_dm <= 0:
                            if self.bot == 'easy':
                                self.eb.choice_card(self.bot_place_occupied.index(i))
                                del self.bot_cards[self.bot_place_occupied.index(i)]
                                del self.bot_place_occupied[self.bot_place_occupied.index(i)]
                            elif self.bot == 'normal':
                                self.nb.choice_card(self.bot_place_occupied.index(i))
                                del self.bot_cards[self.bot_place_occupied.index(i)]
                                del self.bot_place_occupied[self.bot_place_occupied.index(i)]
                            elif self.bot == 'hard':
                                self.hb.choice_card(self.bot_place_occupied.index(i))
                                del self.bot_cards[self.bot_place_occupied.index(i)]
                                del self.bot_place_occupied[self.bot_place_occupied.index(i)]
                        else:
                            self.bot_cards[self.bot_place_occupied.index(i)] = bot_dm, bot_hp - my_dm, bot_img, bot_ind
                    except IndexError:
                        self.bot_hp -= my_dm
                else:
                    self.bot_hp -= my_dm
        self.updete_image()

    def pause(self):
        self.paused = True
        while self.paused:
            for self.event in pygame.event.get():
                if self.event.type == pygame.QUIT:
                    pygame.quit()

            font = pygame.font.Font(None, 70)
            text = font.render(f'Нажмите пробел, чтобы продолжить', True, (255, 255, 255))
            self.screen.blit(text, (180, 220))
            pygame.mixer.music.pause()

            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                self.paused = False
                pygame.mixer.music.unpause()

            pygame.display.update()
            self.clock.tick(15)
        self.updete_image()

    def sounds_point(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if 1150 < mouse[0] < 1150 + 25:
            if 30 < mouse[1] < 30 + 25:
                if click[0] == 1:
                    self.sound_count += 1
                    if self.sound_count % 2 == 0:
                        pygame.mixer.music.pause()
                        self.updete_image()
                    else:
                        pygame.mixer.music.unpause()
                        self.updete_image()

    def counts(self):
        f = open("Results.txt", encoding="utf8")
        data = f.readlines()
        count = int(data[0])
        f.close()
        f = open("Results.txt", 'w')
        count += 10
        f.write(str(count))
        f.close()

    def buttons(self, x, y, width, height, photo_name1, photo_name2):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + width:
            if y < mouse[1] < y + height:
                fon = pygame.transform.scale(self.load_image(f'buttons_img/{photo_name1}'), (width, height))
                self.screen.blit(fon, (x, y))
                if click[0] == 1:
                    pygame.mixer.Sound.play(self.but_sound)
                    pygame.time.delay(300)
            else:
                fon = pygame.transform.scale(self.load_image(f'buttons_img/{photo_name2}'), (width, height))
                self.screen.blit(fon, (x, y))
        else:
            fon = pygame.transform.scale(self.load_image(f'buttons_img/{photo_name2}'), (width, height))
            self.screen.blit(fon, (x, y))

    def run(self, update=False):
        pygame.mixer.music.load('data/musics/play_mus.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)
        if update == False:
            self.updete_image(self.deck)
        while not self.close:
            for self.event in pygame.event.get():
                self.sounds_point()
                self.buttons(10, 360, 100, 50, 'complite2.png', 'compite.png')
                if self.event.type == pygame.QUIT:
                    sys.exit()
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
                        self.updete_image()

            pygame.display.flip()
            self.clock.tick(200)

