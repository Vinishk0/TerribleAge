import os
from random import choice
import pygame

pygame.init()
size = width, height = 1200, 800
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

# колада (временно так, позже переделаем)
deck = [(1, 1), (1, 2), (1, 3)]
inventory_player = []
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
                continue_button = pygame.draw.rect(screen, (255, 0, 0), (990, 250, 200, 300))



image = load_image('background.jpg')
image1 = pygame.transform.scale(image, (width, height))
screen.blit(image1, (0, 0))
continue_button = pygame.draw.rect(screen, (0, 255, 0), (990, 250, 200, 300))

close = False
while not close:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = close = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if (mouse_pos[0] >= 990 and not 1190 < mouse_pos[0]) and (mouse_pos[1] >= 250 and not 550 < mouse_pos[1]):
                give_card(deck, inventory_player)
                # move = True
                print(inventory_player)


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
