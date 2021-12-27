import os
import sys
import pygame

pygame.init()
size = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
but_sound = pygame.mixer.Sound('data/but_sound.mp3')

FPS = 50


def load_image(name, colorkey=None):
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


def buttons(x, y, width, height, photo_name1, photo_name2):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x < mouse[0] < x + width:
        if y < mouse[1] < y + height:
            fon = pygame.transform.scale(load_image(photo_name1), (width, height))
            screen.blit(fon, (x, y))
            if click[0] == 1:
                pygame.mixer.Sound.play(but_sound)
                pygame.time.delay(300)
        else:
            fon = pygame.transform.scale(load_image(photo_name2), (width, height))
            screen.blit(fon, (x, y))
    else:
        fon = pygame.transform.scale(load_image(photo_name2), (width, height))
        screen.blit(fon, (x, y))


def start_screen():
    fon = pygame.transform.scale(load_image('start_back.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    fon = pygame.transform.scale(load_image('1.png'), (250, 100))
    screen.blit(fon, (275, 30))

    while True:
        for event in pygame.event.get():
            buttons(300, 165, 200, 80, 'play2.png', 'play1.png')
            buttons(300, 265, 200, 80, 'train2.png', 'train1.png')
            buttons(300, 365, 200, 80, 'exit1.png', 'exit2.png')

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.flip()
        clock.tick(FPS)


start_screen()
