import os, sys
from platform import platform

import pygame, pygame_menu
import random


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

player_image_left = load_image('lik-left.png')
player_image_right = load_image('lik-left.png')
platform_image = load_image('platform.png')


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(platforms_group, all_sprites)
        self.image = platform_image
        self.rect = self.image.get_rect(center=(x, y))


class Doodle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player_group, all_sprites)
        self.image = player_image_left
        self.rect = self.image.get_rect().move(200, 300)
        self.velocity = 0
        self.gravity = 0.6

    def update(self):
        self.velocity += self.gravity
        self.rect.y += self.velocity

    def move(self, speed):
        self.rect = self.rect.move(speed, 0)

    def exit_from_field(self):
        if self.rect.centerx >= WIDTH:
            self.rect = self.rect.move(-WIDTH, 0)
        if self.rect.centerx <= 0:
            self.rect = self.rect.move(WIDTH, 0)


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


def generate_platforms():
    platforms_group.add(Platform(WIDTH // 2, HEIGHT - 10))

    y = HEIGHT - 50
    for _ in range(10):
        x = random.randint(30, WIDTH - 30)
        platforms_group.add(Platform(x, y))
        y -= random.randint(80, 120)
    return platforms_group


def scroll_screen(player, platforms, scroll):
    if player.rect.top <= HEIGHT // 3:
        player.rect.top = HEIGHT // 3
        scroll += player.velocity

        for platform in platforms:
            platform.rect.y -= player.velocity

            if platform.rect.y > HEIGHT:
                platform.kill()

        while len(platforms) < 10:
            new_platform = Platform(random.randint(30, WIDTH - 30), -random.randint(50, 100))
            platforms.add(new_platform)

    return scroll


def check_collisions(player, platforms):
    if player.velocity > 0:
        hits = pygame.sprite.spritecollide(player, platforms, False)
        if hits:
            player.velocity = -15


def show_statistic():
    pass


def start_the_game():
    global run
    run = True
    menu.disable()

all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
platforms_group = pygame.sprite.Group()
scroll = 0
doodle_speed = 0
player_acceleration = 0.5
player_deceleration = 0.4
max_speed = 6
doodle = Doodle()
platforms = generate_platforms()
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
                doodle.image = player_image_right
                move_right = True
            if event.key == pygame.K_LEFT:
                doodle.image = player_image_left
                move_left = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                move_right = False
            if event.key == pygame.K_LEFT:
                move_left = False

    scroll = scroll_screen(doodle, platforms, scroll)
    check_collisions(doodle, platforms)
    doodle_move()
    doodle.exit_from_field()
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
