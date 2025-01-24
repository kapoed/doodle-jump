import pygame
import pygame_menu

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)
SIZE = WIDTH, HEIGHT = (600, 900)
run = False
pygame.init()
screen = pygame.display.set_mode(SIZE)


def show_statistic():
    pass


def start_the_game():
    global run
    run = True
    menu.disable()


menu = pygame_menu.Menu('Doodle Jump', WIDTH, HEIGHT, theme=pygame_menu.themes.THEME_GREEN)
menu.add.button('Играть', start_the_game)
menu.add.button('Статистика', show_statistic)
menu.add.button('Выход из игры', pygame_menu.events.EXIT)


clock = pygame.time.Clock()
FPS = 60
menu.mainloop(screen)
while run:
    clock.tick(FPS)
    screen.fill(BLACK)
    for event in pygame.event.get():
        run = event.type != pygame.QUIT


    pygame.display.update()

pygame.quit()
