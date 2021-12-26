import os
from random import choice
import pygame

pygame.init()
size = width, height = 1200, 800
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
inventory_card = pygame.sprite.Group()

# колада (временно так, позже переделаем)
deck = [(5, 6), (3, 4), (5, 8), (4, 3), (6, 2), (3, 5), (5, 6), (3, 4), (5, 8), (4, 3),
        (6, 2), (3, 5), (5, 6), (3, 4), (5, 8), (4, 3), (6, 2), (3, 5), (5, 6), (3, 4), (5, 8),
        (4, 3), (6, 2), (3, 5), (5, 6), (3, 4), (5, 8), (4, 3), (6, 2), (3, 5), (5, 6), (3, 4),
        (5, 8), (4, 3), (6, 2)]
inventory_player = [(5, 6), (3, 4), (5, 8), (4, 3)]
move = False

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
            if not desk:
                updete_image()
            updete_image(card)




def updete_image(cart=None):
    if cart == None:
        desk_button = pygame.draw.rect(screen, (255, 0, 0), (990, 250, 200, 300))

    image = load_image('background.jpg')
    image1 = pygame.transform.scale(image, (width, height))
    screen.blit(image1, (0, 0))
    image = load_image('carta3.png')
    image1 = pygame.transform.scale(image, (200, 300))
    screen.blit(image1, (990, 250))

    for i in range(len(inventory_player)):
        x = 400 + i * 30
        y = 650
        # исправить когда будут нарисованны текстуры
        name_image = 'carta_2.png'
        image = load_image(name_image)
        image1 = pygame.transform.scale(image, (150, 225))
        screen.blit(image1, (x, y))

    image = load_image('pole.png')
    image1 = pygame.transform.scale(image, (150, 225))
    screen.blit(image1, (150, 100))
    screen.blit(image1, (350, 100))
    screen.blit(image1, (550, 100))
    screen.blit(image1, (750, 100))
    screen.blit(image1, (150, 425))
    screen.blit(image1, (350, 425))
    screen.blit(image1, (550, 425))
    screen.blit(image1, (750, 425))

    image = load_image('move.png')
    image1 = pygame.transform.scale(image, (80, 70))
    screen.blit(image1, (10, 330))

    font = pygame.font.Font(None, 30)
    text = font.render(f"{len(deck)}/35", True, (227, 37, 107))
    screen.blit(text, (1000, 560))
    pygame.display.flip()
    clock.tick(60)

def inventory_show():
    # затемнение фона
    s = pygame.Surface((width, height))
    s.set_alpha(180)
    s.fill((30, 27, 24))
    screen.blit(s, (0, 0))

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

        # исправить когда будут нарисованны текстуры
        name_image = 'carta_2.png'
        image = load_image(name_image)
        image1 = pygame.transform.scale(image, (150, 225))
        screen.blit(image1, (x, y))

updete_image()
close = False
choice = False
while not close:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if (mouse_pos[0] >= 990 and not 1190 < mouse_pos[0]) and (
                    mouse_pos[1] >= 250 and not 550 < mouse_pos[1]) and not choice:
                give_card(deck, inventory_player)
                move = True
            if (mouse_pos[0] >= 10 and not 90 < mouse_pos[0]) and (
                    mouse_pos[1] >= 360 and not 400 < mouse_pos[1]) and not choice:
                move = False
            if (mouse_pos[0] >= 400 and not 700 < mouse_pos[0]) and (
                    mouse_pos[1] >= 650 and not 800 < mouse_pos[1]) and not choice:
                choice = True
                inventory_show()
            if choice:
                pass



    pygame.display.flip()
    clock.tick(60)

pygame.quit()
