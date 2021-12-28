import os
from random import choice
import pygame

deck = [(1, 1, 'card_1_1'), (1, 2, 'card_1_2'), (1, 3, 'card_1_3'), (1, 4, 'card_1_4'), (1, 5, 'card_1_5'),
        (2, 1, 'card_2_1'), (2, 2, 'card_2_2'), (2, 3, 'card_2_3'), (2, 4, 'card_2_4'), (2, 5, 'card_2_5'),
        (3, 1, 'card_3_1'), (3, 2, 'card_3_2'), (3, 3, 'card_3_3'), (3, 4, 'card_3_4'), (3, 5, 'card_3_5')]
inventory_player = [(1, 1, 'card_1_1'), (1, 2, 'card_2_1'), (1, 3, 'card_3_1')]
my_card = []
list = []


class BaseGame:
    def __init__(self):
        pygame.init()
        self.size = self.width, self.height = 1200, 800
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.inventory_card = pygame.sprite.Group()
        self.vil_x, self.vil_y, self.x_old, self.y_old, self.x_new, self.y_new = 1000, 550, 0, 0, 0, 0
        self.move = False
        self.movement = False
        self.vil = ()
        self.close = False
        self.ch = False
        self.updete_image()

    def load_image(self, name):
        # ф-ция открывания картинок
        fullname = os.path.join('data', name)
        image = pygame.image.load(fullname)
        return image

    def give_card(self, desk, inventory_player):
        # ф-ция добовления карт в инвентарь игрока
        if desk:
            if len(inventory_player) < 6 and not self.move:
                card = choice(desk)
                del deck[desk.index(card)]
                inventory_player.append(card)
                self.updete_image(deck, card, None)

    def updete_image(self, desk=False, cart=None, index=None):
        image = self.load_image('background.jpg')
        image1 = pygame.transform.scale(image, (self.width, self.height))
        self.screen.blit(image1, (0, 0))

        if None != index:
            self.vil = inventory_player[index]
            del inventory_player[index]
        if self.vil and not self.movement:
            image = self.load_image(self.vil[2] + '.png')
            image1 = pygame.transform.scale(image, (150, 225))
            self.spr = self.screen.blit(image1, (1000, 550))
            self.vil_x, self.vil_y = 1000, 550
        image = self.load_image('pole.png')
        image1 = pygame.transform.scale(image, (150, 225))

        for i in range(150, 950, 200):
            self.screen.blit(image1, (i, 100))
            pole = self.screen.blit(image1, (i, 450))
            if pole not in list:
                list.append(pole)
        if my_card:
            for i in my_card:
                name_image = i[2]
                image = self.load_image(name_image + '.png')
                image1 = pygame.transform.scale(image, (150, 225))
                if i[-1] == 0:
                    self.screen.blit(image1, (150, 450))
                elif i[-1] == 1:
                    self.screen.blit(image1, (350, 450))
                elif i[-1] == 2:
                    self.screen.blit(image1, (550, 450))
                elif i[-1] == 3:
                    self.screen.blit(image1, (750, 450))
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

        font = pygame.font.Font(None, 30)
        text = font.render(f"{len(deck)}/35", True, (227, 37, 107))
        self.screen.blit(text, (1000, 530))
        if None != cart:
            pass
        if deck:
            image = self.load_image('carta3.png')
            image1 = pygame.transform.scale(image, (200, 300))
            self.screen.blit(image1, (990, 200))
        if self.movement:
            self.dragging()

        pygame.display.flip()
        self.clock.tick(60)

    def inventory_show(self):
        # затемнение фона
        s = pygame.Surface((self.width, self.height))
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

    def click_card(self):
        index = None
        mouse_pos = self.mouse_pos
        if (mouse_pos[0] >= 10 and not 90 < mouse_pos[0]) and (
                mouse_pos[1] >= 360 and not 400 < mouse_pos[1]):
            self.ch = False
            self.updete_image(deck, None, None)
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
            self.updete_image(deck, None, index)

    def dragging(self, new_vil=None):
        if self.vil:
            image = self.load_image(self.vil[2] + '.png')
            image1 = pygame.transform.scale(image, (150, 225))
            self.spr = self.screen.blit(image1, (self.vil_x, self.vil_y))

    def functions(self):
        mouse_pos = self.mouse_pos
        if (mouse_pos[0] >= 990 and not 1190 < mouse_pos[0]) and (
                mouse_pos[1] >= 250 and not 550 < mouse_pos[1]):
            self.give_card(deck, inventory_player)
            self.move = True
        if (mouse_pos[0] >= 10 and not 90 < mouse_pos[0]) and (
                mouse_pos[1] >= 360 and not 400 < mouse_pos[1]):
            self.move = False
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
                        dm, hp, img = self.vil
                        my_card.append((dm, hp, img, self.spr.collidelist(list)))
                        self.vil = ()
                        self.updete_image()
                    self.movement = False

    def run(self, update=False):
        if update == False:
            self.updete_image(deck)
        while not self.close:
            for self.event in pygame.event.get():
                if self.event.type == pygame.QUIT:
                    self.close = True
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
            self.clock.tick(60)
        pygame.quit()


base_game = BaseGame()
base_game.run()