import os
from random import choice
import pygame

pygame.init()
size = width, height = 1200, 800
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
inventory_card = pygame.sprite.Group()
vil = ()
vil_x, vil_y, x_old, y_old, x_new, y_new = 1000, 550, 0, 0, 0, 0

# колада (временно так, позже переделаем)
deck = [(1, 1, 'card_1_1'), (1, 2, 'card_1_2'), (1, 3, 'card_1_3'), (1, 4, 'card_1_4'), (1, 5, 'card_1_5'),
        (2, 1, 'card_2_1'), (2, 2, 'card_2_2'), (2, 3, 'card_2_3'), (2, 4, 'card_2_4'), (2, 5, 'card_2_5'),
        (3, 1, 'card_3_1'), (3, 2, 'card_3_2'), (3, 3, 'card_3_3'), (3, 4, 'card_3_4'), (3, 5, 'card_3_5')]
inventory_player = [(1, 1, 'card_1_1'), (1, 2, 'card_2_1'), (1, 3, 'card_3_1')]
move = False
movement = False
my_card = []
list = []


def load_image(name):
    # ф-ция открывания картинок
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    return image



def give_card(desk, inventory_player):
    # ф-ция добовления карт в инвентарь игрока
    if desk:
        if len(inventory_player) < 6 and not move:
            card = choice(desk)
            del deck[desk.index(card)]
            inventory_player.append(card)
            updete_image(deck, card, None)


def updete_image(desk=False, cart=None, index=None):
    global vil, vil_x, vil_y, spr
    image = load_image('background.jpg')
    image1 = pygame.transform.scale(image, (width, height))
    screen.blit(image1, (0, 0))

    if None != index:
        vil = inventory_player[index]
        del inventory_player[index]
    if vil and not movement:
        image = load_image(vil[2] + '.png')
        image1 = pygame.transform.scale(image, (150, 225))
        spr = screen.blit(image1, (1000, 550))
        vil_x, vil_y = 1000, 550
    image = load_image('pole.png')
    image1 = pygame.transform.scale(image, (150, 225))

    for i in range(150, 950, 200):
        screen.blit(image1, (i, 100))
        pole = screen.blit(image1, (i, 450))
        if pole not in list:
            list.append(pole)
    if my_card:
        for i in my_card:
            name_image = i[2]
            image = load_image(name_image + '.png')
            image1 = pygame.transform.scale(image, (150, 225))
            if i[-1] == 0:
                screen.blit(image1, (150, 450))
            elif i[-1] == 1:
                screen.blit(image1, (350, 450))
            elif i[-1] == 2:
                screen.blit(image1, (550, 450))
            elif i[-1] == 3:
                screen.blit(image1, (750, 450))
            else:
                del list[list.index(i)]


    for i in range(len(inventory_player)):
        x = 400 + i * 30
        y = 650
        # исправить когда будут нарисованны текстуры
        name_image = inventory_player[i][2]
        image = load_image(name_image + '.png')
        image1 = pygame.transform.scale(image, (150, 225))
        screen.blit(image1, (x, y))
    image = load_image('move.png')
    image1 = pygame.transform.scale(image, (100, 50))
    screen.blit(image1, (10, 360))

    font = pygame.font.Font(None, 30)
    text = font.render(f"{len(deck)}/35", True, (227, 37, 107))
    screen.blit(text, (1000, 530))
    if None != cart:
        pass
    if deck:
        image = load_image('carta3.png')
        image1 = pygame.transform.scale(image, (200, 300))
        screen.blit(image1, (990, 200))
    if movement:
        dragging()

    pygame.display.flip()
    clock.tick(60)


def inventory_show():
    # затемнение фона
    s = pygame.Surface((width, height))
    s.set_alpha(180)
    s.fill((30, 27, 24))
    screen.blit(s, (0, 0))

    image = load_image('cancle.png')
    image1 = pygame.transform.scale(image, (100, 50))
    screen.blit(image1, (10, 360))

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
        image = load_image(name_image + '.png')
        image1 = pygame.transform.scale(image, (150, 225))
        screen.blit(image1, (x, y))



def click_card():
    global deck, ch, movement
    index = None
    if (mouse_pos[0] >= 10 and not 90 < mouse_pos[0]) and (
            mouse_pos[1] >= 360 and not 400 < mouse_pos[1]):
        ch = False
        updete_image(deck, None, None)
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
        ch = False
        movement = False
        updete_image(deck, None, index)


def dragging(new_vil=None):
    global spr
    if vil:
        image = load_image(vil[2] + '.png')
        image1 = pygame.transform.scale(image, (150, 225))
        spr = screen.blit(image1, (vil_x, vil_y))



def functions():
    global move, movement, ch, vil, spr, v
    if (mouse_pos[0] >= 990 and not 1190 < mouse_pos[0]) and (
            mouse_pos[1] >= 250 and not 550 < mouse_pos[1]):
        give_card(deck, inventory_player)
        move = True
    if (mouse_pos[0] >= 10 and not 90 < mouse_pos[0]) and (
            mouse_pos[1] >= 360 and not 400 < mouse_pos[1]):
        move = False
    if (mouse_pos[0] >= 400 and not 700 < mouse_pos[0]) and (
            mouse_pos[1] >= 650 and not 800 < mouse_pos[1]):
        ch = True
        inventory_show()
    if vil:
        if vil_x < event.pos[0] < vil_x + 150 and vil_y < event.pos[1] < vil_y + 225 and vil[2]:
            if movement == False:
                movement = True
            else:
                if spr.collidelist(list) + 1:
                    dm, hp, img = vil
                    my_card.append((dm, hp, img, spr.collidelist(list)))
                    vil = ()
                    updete_image()
                movement = False


updete_image(deck)
close = False
ch = False
while not close:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if not ch:
                functions()
            if ch:
                click_card()
        if event.type == pygame.MOUSEMOTION:
            if movement:
                x_new, y_new = event.rel
                vil_x, vil_y = vil_x + x_new, vil_y + y_new
                updete_image()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
