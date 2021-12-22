import os
import sys

import pygame

pygame.init()
size = width, height = 900, 800
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

image = load_image('background.jpg')
image1 = pygame.transform.scale(image, (width, height))

close = False
while not close:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = close = True
    pygame.display.flip()
    screen.blit(image1, (0, 0))
    clock.tick(60)

pygame.quit()
