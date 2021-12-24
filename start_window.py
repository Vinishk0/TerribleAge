import os
import sys
import pygame

pygame.init()
size = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

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


def start_screen():
    intro_texts = ['Играть', 'Обучение', 'Выход']

    fon = pygame.transform.scale(load_image('start_back.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font1 = pygame.font.Font(None, 70)
    font2 = pygame.font.Font(None, 60)

    text1 = font1.render("TerribleAge", True, (255, 255, 255))
    screen.blit(text1, (270, 10))
    x, y = 330, 150

    for i in intro_texts:
        text = font2.render(i, True, (116, 219, 36))
        screen.blit(text, (x, y))
        y += 150

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


start_screen()
