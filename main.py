import os
from random import choice
import pygame

pygame.init()
size = width, height = 1200, 800
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

# колада (временно так, позже переделаем)
deck = [(5, 6), (3, 4), (5, 8), (4, 3), (6, 2), (3, 5)]
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
                desk_button = pygame.draw.rect(screen, (255, 0, 0), (990, 250, 200, 300))
                # перенести в отдельную ф-цию обновления
            for i in range(len(inventory_player)):
                x = 400 + i * 30
                y = 650
                # исправить когда будут нарисованны текстуры
                pygame.draw.rect(screen, (inventory_player[i][0] * 30, inventory_player[i][1] * 30, 255), (x, y, 150, 225))



image = load_image('background.jpg')
image1 = pygame.transform.scale(image, (width, height))
screen.blit(image1, (0, 0))

desk_button = pygame.draw.rect(screen, (0, 255, 0), (990, 250, 200, 300))
move_button = pygame.draw.rect(screen, (0, 255, 255), (10, 360, 80, 40))

place_card_opponent_1 = pygame.draw.rect(screen, (0, 255, 0), (150, 100, 150, 225), 8)
place_card_opponent_2 = pygame.draw.rect(screen, (0, 255, 0), (350, 100, 150, 225), 8)
place_card_opponent_3 = pygame.draw.rect(screen, (0, 255, 0), (550, 100, 150, 225), 8)
place_card_opponent_4 = pygame.draw.rect(screen, (0, 255, 0), (750, 100, 150, 225), 8)
place_card_player_1 = pygame.draw.rect(screen, (0, 255, 0), (150, 425, 150, 225), 8)
place_card_player_2 = pygame.draw.rect(screen, (0, 255, 0), (350, 425, 150, 225), 8)
place_card_player_3 = pygame.draw.rect(screen, (0, 255, 0), (550, 425, 150, 225), 8)
place_card_player_4 = pygame.draw.rect(screen, (0, 255, 0), (750, 425, 150, 225), 8)

close = False
while not close:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = close = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if (mouse_pos[0] >= 990 and not 1190 < mouse_pos[0]) and (mouse_pos[1] >= 250 and not 550 < mouse_pos[1]):
                give_card(deck, inventory_player)
                move = True
            if (mouse_pos[0] >= 10 and not 90 < mouse_pos[0]) and (
                    mouse_pos[1] >= 360 and not 400 < mouse_pos[1]):
                move = False


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
