import os, sys
import pygame, pygame_menu


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


pygame.display.set_icon(load_image("icon.ico"))
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)
SIZE = WIDTH, HEIGHT = (400, 600)


def doodle_move():
    global doodle_speed
    if move_right:
        doodle_speed += player_acceleration
    if move_left:
        doodle_speed -= player_acceleration
    if not move_left and not move_right:
        if doodle_speed > 0:
            doodle_speed -= player_deceleration
            if doodle_speed < 0:
                doodle_speed = 0
        elif doodle_speed < 0:
            doodle_speed += player_deceleration
            if doodle_speed > 0:
                doodle_speed = 0
    if doodle_speed > max_speed:
        doodle_speed = max_speed
    elif doodle_speed < -max_speed:
        doodle_speed = -max_speed
    doodle.move(doodle_speed)


player_image = load_image('lik-left.png')


class Doodle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(200, 300)

    def move(self, speed):
        self.rect = self.rect.move(speed, 0)

    def exit_from_field(self):
        if self.rect.centerx >= WIDTH:
            self.rect = self.rect.move(-WIDTH, 0)
        if self.rect.centerx <= 0:
            self.rect = self.rect.move(WIDTH, 0)



def show_statistic():
    pass


def start_the_game():
    global run
    run = True
    menu.disable()

all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
doodle_speed = 0
player_acceleration = 0.5
player_deceleration = 0.25
max_speed = 6
doodle = Doodle()
move_right = False
move_left = False
run = False
pygame.init()
screen = pygame.display.set_mode(SIZE)

menu = pygame_menu.Menu('Doodle Jump', WIDTH, HEIGHT, theme=pygame_menu.themes.THEME_GREEN)
menu.add.button('Играть', start_the_game)
menu.add.button('Статистика', show_statistic)
menu.add.button('Выход из игры', pygame_menu.events.EXIT)

clock = pygame.time.Clock()
FPS = 60
menu.mainloop(screen)
bg = pygame.transform.scale(load_image('bck.png'), (WIDTH, HEIGHT))
while run:
    screen.fill(BLACK)
    screen.blit(bg, (0, 0))
    for event in pygame.event.get():
        run = event.type != pygame.QUIT
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                move_right = True
            if event.key == pygame.K_LEFT:
                move_left = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                move_right = False
            if event.key == pygame.K_LEFT:
                move_left = False


    doodle_move()
    doodle.exit_from_field()
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
