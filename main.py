import os
import sys
import pygame
import pygame_menu
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
player_image_right = load_image('lik-right.png')
player_image_up = load_image('lik-up.png')
monsters_image = (load_image('monster1.png'),
                  load_image('monster2.png'),
                  load_image('monster3.png'))
bullet_image = load_image('bullet.png')
spring_normal_image = load_image('spring1.png')
spring_activate_image = load_image('spring2.png')
propeller_normal_image = load_image('propeller_normal.png')
propeller_animation_images = (load_image('propeller1.png'),
                              load_image('propeller2.png'),
                              load_image('propeller3.png'))
platform_image = load_image('platform.png')
moving_platform_image = load_image('moving_platform.png')
vanishing_platform_image = load_image('vanishing_platform.png')
breaking_platform_images = (load_image('breaking_platform1.png'),
                            load_image('breaking_platform2.png'),
                            load_image('breaking_platform3.png'),
                            load_image('breaking_platform4.png'))


class Spring(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(bonuses_group, all_sprites)
        self.image = spring_normal_image
        self.rect = self.image.get_rect(center=(x, y))
        self.is_active = False

    def activate(self):
        self.is_active = True
        self.image = spring_activate_image
        self.rect = self.rect.move(0, -15)

    def update(self):
        if self.is_active:
            self.image = spring_activate_image


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(platforms_group, all_sprites)
        self.image = platform_image
        self.rect = self.image.get_rect(center=(x, y))


class VanishingPlatform(Platform):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = vanishing_platform_image

    def vanish(self):
        self.kill()


class BreakingPlatform(Platform):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = breaking_platform_images[0]
        self.breaking_stage = 0
        self.is_broken = False

    def update(self):
        if self.is_broken:
            self.breaking_stage += 1
            if self.breaking_stage < len(breaking_platform_images):
                self.image = breaking_platform_images[self.breaking_stage]
            else:
                self.rect = self.rect.move(0, 9)

    def break_platform(self):
        self.is_broken = True


class MovingPlatform(Platform):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = moving_platform_image
        self.direction = random.choice([-1, 1])
        self.speed = 2

    def update(self):
        self.rect.x += self.direction * self.speed
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.direction *= -1


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(bullets_group, all_sprites)
        self.image = bullet_image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -25

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < -200:
            self.kill()


class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(monsters_group, all_sprites)
        self.image = random.choice(monsters_image)
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = random.choice([-1, 1])
        self.speed = 3

    def update(self):
        self.rect.x += self.direction * self.speed
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.direction *= -1


class Doodle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player_group, all_sprites)
        self.image = player_image_left
        self.rect = self.image.get_rect().move(200, 300)
        self.velocity = 0
        self.gravity = 0.6
        self.is_dead = False
        self.has_helicopter = False

    def update(self):
        if not self.is_dead:
            if self.has_helicopter:
                self.rect.y -= 8
            else:
                self.velocity += self.gravity
                self.rect.y += self.velocity
        else:
            self.velocity += self.gravity
            self.rect.y += self.velocity

    def activate_helicopter(self):
        self.has_helicopter = True

    def deactivate_helicopter(self):
        self.has_helicopter = False

    def move(self, speed):
        self.rect = self.rect.move(speed, 0)

    def exit_from_field(self):
        if self.rect.centerx >= WIDTH:
            self.rect = self.rect.move(-WIDTH, 0)
        if self.rect.centerx <= 0:
            self.rect = self.rect.move(WIDTH, 0)


def doodle_move():
    global doodle_speed
    if doodle.is_dead:
        return
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
    for _ in range(20):
        x = random.randint(30, WIDTH - 30)
        Platform(x, y)
        y -= random.randint(80, 120)

    return platforms_group


def scroll_screen(player, platforms, scroll):
    global score, safe_platform_spawn, spawn_platforms
    if player.rect.top <= HEIGHT // 3:
        player.rect.top = HEIGHT // 3
        scroll += player.velocity

        for platform in platforms:
            platform.rect.y -= player.velocity
            if platform.rect.y > HEIGHT:
                platform.kill()

        for monster in monsters_group:
            monster.rect.y -= player.velocity
            if monster.rect.y > HEIGHT:
                monster.kill()

        for bonus in bonuses_group:
            bonus.rect.y -= player.velocity
            if bonus.rect.y > HEIGHT:
                bonus.kill()

        score += abs(player.velocity)
        safe_platform_spawn += abs(player.velocity)
        if int(safe_platform_spawn) >= 150:
            safe_platform_spawn = 0
            Platform(random.randint(30, WIDTH - 30), -50)

        if score >= difficulty_change:
            spawn_platforms = 10

        if score > 6000 and random.random() < 0.004 and len(monsters_group) < 3:
            Monster(random.randint(50, WIDTH - 50), -50)

        while len(platforms) < spawn_platforms:
            x = random.randint(30, WIDTH - 30)
            y = -random.randrange(0, 400, 20)
            Platform(x, y)
            if random.random() < 0.15:
                if random.random() < 0.8:
                    Spring(x, y - 10)
                else:
                    pass
            if random.random() < 0.3:
                x = random.randint(30, WIDTH - 30)
                MovingPlatform(x, -random.randint(50, 100))
            if random.random() < 0.6:
                x = random.randint(30, WIDTH - 30)
                BreakingPlatform(x, -random.randint(50, 100))
            if random.random() < 0.3 and score > 0:
                x = random.randint(30, WIDTH - 30)
                VanishingPlatform(x, -random.randint(50, 100))


def check_collisions(player, platforms):
    if player.is_dead:
        return
    if player.velocity > 0:
        player_bottom = player.rect.bottom
        for platform in platforms:
            platform_top = platform.rect.top
            if player.rect.colliderect(platform.rect) and player_bottom >= platform_top:
                overlap = player_bottom - platform_top
                if overlap < platform.rect.h + 10:
                    if isinstance(platform, BreakingPlatform):
                        platform.break_platform()
                    else:
                        player.velocity = -15
                    if isinstance(platform, VanishingPlatform):
                        platform.vanish()
                break
        for monster in monsters_group:
            if player.rect.colliderect(monster.rect):
                if player.rect.bottom <= monster.rect.top + 15:
                    monster.kill()
                    player.velocity = -15
                else:
                    player.is_dead = True
                    global move_left, move_right
                    move_left = False
                    move_right = False

        for bonus in bonuses_group:
            if isinstance(bonus, Spring):
                if player.rect.colliderect(bonus.rect):
                    if player.rect.bottom <= bonus.rect.top + 15:
                        player.velocity = -30
                        bonus.activate()
                        break


def reset_game():
    global all_sprites, player_group, platforms_group, bullets_group, spawn_platforms, difficulty_change, \
        safe_platform_spawn, score, scroll, doodle_speed, doodle, platforms, move_right, move_left, run, monsters_group

    all_sprites.empty()
    player_group.empty()
    platforms_group.empty()
    bullets_group.empty()
    monsters_group.empty()

    doodle = Doodle()
    platforms = generate_platforms()

    score = 0
    safe_platform_spawn = 0
    scroll = 0
    doodle_speed = 0
    move_right = False
    move_left = False
    run = False


def save_score(score):
    with open('records.txt', 'a') as f:
        f.write(f"{int(score)}\n")


def show_statistic():
    try:
        with open('records.txt', 'r') as f:
            scores = [int(line.strip()) for line in f if line.strip().isdigit()]
    except FileNotFoundError:
        scores = []

    scores = sorted(scores, reverse=True)[:10]

    statistic_menu = pygame_menu.Menu('Статистика', WIDTH, HEIGHT, theme=pygame_menu.themes.THEME_GREEN)
    statistic_menu.add.label('Последние 10 рекордов:')
    if not scores:
        statistic_menu.add.label('Рекордов пока нет')
    else:
        for idx, score in enumerate(scores, 1):
            statistic_menu.add.label(f'{idx}. {score}')
    statistic_menu.add.button('Назад', reset_game)
    statistic_menu.mainloop(screen)


def start_the_game():
    reset_game()
    global run
    run = True
    menu.disable()


all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
platforms_group = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()
monsters_group = pygame.sprite.Group()
bonuses_group = pygame.sprite.Group()
spawn_platforms = 20
difficulty_change = 10000
safe_platform_spawn = 0
score = 0
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

font = pygame.font.Font(None, 36)

while True:
    if not run:
        menu.mainloop(screen)
    clock = pygame.time.Clock()
    while run:
        screen.fill(BLACK)
        screen.blit(bg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if doodle.is_dead:
                    continue
                if event.key == pygame.K_RIGHT:
                    doodle.image = player_image_right
                    move_right = True
                if event.key == pygame.K_LEFT:
                    doodle.image = player_image_left
                    move_left = True
                if event.key == pygame.K_UP:
                    doodle.image = player_image_up
                    Bullet(doodle.rect.centerx, doodle.rect.top)
            if event.type == pygame.KEYUP:
                if doodle.is_dead:
                    continue
                if event.key == pygame.K_RIGHT:
                    move_right = False
                if event.key == pygame.K_LEFT:
                    move_left = False
                if event.key == pygame.K_UP:
                    doodle.image = player_image_left

        pygame.sprite.groupcollide(bullets_group, monsters_group, True, True)
        scroll_screen(doodle, platforms, scroll)
        check_collisions(doodle, platforms)
        doodle_move()
        doodle.exit_from_field()
        all_sprites.draw(screen)
        all_sprites.update()
        if doodle.rect.top >= HEIGHT:
            run = False

        score_text = font.render(f"Очки: {int(score)}", True, 'darkgreen')
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    if score > 0:
        save_score(score)
        score = 0

    menu.enable()