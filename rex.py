import pygame
import os
import neat
import random

# Initialization
pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.display.init()
LOCAL_DIR = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(LOCAL_DIR, 'NEAT_config.txt')
IMG_DIR = os.path.join(LOCAL_DIR, 'img')
MUSIC_DIR = os.path.join(LOCAL_DIR, 'sound')

# Clock
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont("comicsans", 24)
title_font = pygame.font.SysFont("comicsans", 60, italic=True, bold=True)
font2 = pygame.font.SysFont("comicsans", 32)
font3 = pygame.font.SysFont("comicsans", 20)

# Window Parameters
WIN_WIDTH = 1000
WIN_HEIGHT = 400
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.HWSURFACE)
BG_COLOR = (235, 235, 235)
pygame.display.set_caption("Rex.AI")
WIN.fill(BG_COLOR)

# Parameters
FLOOR = 300
BASE_LINE = 320
BASE_VEL_INI = 7
BASE_VEL = BASE_VEL_INI
HIGH_SCORE = 0
GEN = 0
REX_X = 50
AI_HIGH_SCORE = 0
GAME = 0
DRAW_LINE = True

# Load music
MUSIC = []
for song in os.listdir(MUSIC_DIR):
    if song.endswith('.mp3'):
        MUSIC.append(str(song))

# Shuffle Music
CURRENT_MUSIC = 'Harder Better Faster Stronger.mp3'
pygame.mixer.music.load(os.path.join('sound', CURRENT_MUSIC))
pygame.mixer.music.play(-1)

# Load images
IMG_BASE = pygame.image.load(os.path.join('img', 'background.png')).convert_alpha()
IMG_BIRD1 = pygame.image.load(os.path.join('img', 'bird1.png')).convert_alpha()
IMG_BIRD2 = pygame.image.load(os.path.join('img', 'bird2.png')).convert_alpha()
IMG_BADBIRD1 = pygame.image.load(os.path.join('img', 'bad_bird1.png')).convert_alpha()
IMG_BADBIRD2 = pygame.image.load(os.path.join('img', 'bad_bird2.png')).convert_alpha()
IMG_SCACTUS1 = pygame.image.load(os.path.join('img', 'scactus1.png')).convert_alpha()
IMG_SCACTUS2 = pygame.image.load(os.path.join('img', 'scactus2.png')).convert_alpha()
IMG_SCACTUS3 = pygame.image.load(os.path.join('img', 'scactus3.png')).convert_alpha()
IMG_SCACTUS4 = pygame.image.load(os.path.join('img', 'scactus4.png')).convert_alpha()
IMG_SCACTUS5 = pygame.image.load(os.path.join('img', 'scactus5.png')).convert_alpha()
IMG_SCACTUS6 = pygame.image.load(os.path.join('img', 'scactus6.png')).convert_alpha()
IMG_SCACTI = [IMG_SCACTUS1, IMG_SCACTUS2, IMG_SCACTUS3, IMG_SCACTUS4, IMG_SCACTUS5, IMG_SCACTUS6]
IMG_BCACTUS1 = pygame.image.load(os.path.join('img', 'bcactus1.png')).convert_alpha()
IMG_BCACTUS2 = pygame.image.load(os.path.join('img', 'bcactus2.png')).convert_alpha()
IMG_BCACTUS3 = pygame.image.load(os.path.join('img', 'bcactus3.png')).convert_alpha()
IMG_BCACTUS4 = pygame.image.load(os.path.join('img', 'bcactus4.png')).convert_alpha()
IMG_BCACTUS5 = pygame.image.load(os.path.join('img', 'bcactus5.png')).convert_alpha()
IMG_BCACTUS6 = pygame.image.load(os.path.join('img', 'bcactus6.png')).convert_alpha()
IMG_BCACTI = [IMG_BCACTUS1, IMG_BCACTUS2, IMG_BCACTUS3, IMG_BCACTUS4, IMG_BCACTUS5, IMG_BCACTUS6]
IMG_CLOUD = pygame.image.load(os.path.join('img', 'cloud.png')).convert_alpha()
IMG_MOON = pygame.image.load(os.path.join('img', 'moon.png')).convert_alpha()
IMG_REX1 = pygame.image.load(os.path.join('img', 'rex1.png')).convert_alpha()
IMG_REX2 = pygame.image.load(os.path.join('img', 'rex2.png')).convert_alpha()
IMG_REX3 = pygame.image.load(os.path.join('img', 'rex3.png')).convert_alpha()
IMG_REX_D1 = pygame.image.load(os.path.join('img', 'rex_ducked1.png')).convert_alpha()
IMG_REX_D2 = pygame.image.load(os.path.join('img', 'rex_ducked2.png')).convert_alpha()
IMG_REX1_H = pygame.image.load(os.path.join('img', 'rex1_hurt.png')).convert_alpha()
IMG_REX2_H = pygame.image.load(os.path.join('img', 'rex2_hurt.png')).convert_alpha()
IMG_REX3_H = pygame.image.load(os.path.join('img', 'rex3_hurt.png')).convert_alpha()
IMG_REX_D1_H = pygame.image.load(os.path.join('img', 'rex_ducked1_hurt.png')).convert_alpha()
IMG_REX_D2_H = pygame.image.load(os.path.join('img', 'rex_ducked2_hurt.png')).convert_alpha()
IMG_STAR1 = pygame.image.load(os.path.join('img', 'star1.png')).convert_alpha()
IMG_STAR2 = pygame.image.load(os.path.join('img', 'star2.png')).convert_alpha()
IMG_STAR3 = pygame.image.load(os.path.join('img', 'star3.png')).convert_alpha()
IMG_SUN = pygame.image.load(os.path.join('img', 'sun.png')).convert_alpha()
IMG_THUG = pygame.image.load(os.path.join('img', 'thug_glasses.png')).convert_alpha()
IMG_HEALTH = pygame.image.load(os.path.join('img', 'health.png')).convert_alpha()
IMG_ARROW = pygame.image.load(os.path.join('img', 'arrow.png')).convert_alpha()

# Image info
BADBIRD_WIDTH = IMG_BADBIRD1.get_width()
HEALTH_WIDTH = IMG_HEALTH.get_width()


class Base:
    WIDTH = IMG_BASE.get_width()
    IMG = IMG_BASE

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
        self.vel = BASE_VEL

    def move(self):
        self.x1 -= self.vel
        self.x2 -= self.vel

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def update_speed(self):
        self.vel = BASE_VEL

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


class Cloud:
    IMG = IMG_CLOUD
    IMG_GLASS = IMG_THUG

    def __init__(self):
        self.x = WIN_WIDTH
        self.y = random.randint(60, 80)
        self.vel = random.randint(1, 2)
        self.wearGlass = 1 == random.randint(1, 7)

    def move(self):
        self.x -= self.vel

    def draw(self, win):
        win.blit(self.IMG, (self.x, self.y))

        # Draw thug life glasses
        if self.wearGlass:
            win.blit(self.IMG_GLASS, (self.x + 5, self.y - 3))


class Moon:
    IMG = IMG_MOON

    def __init__(self):
        self.x = 850
        self.y = 50

    def draw(self, win):
        win.blit(self.IMG, (self.x, self.y))


class Star:
    IMG1 = IMG_STAR1
    IMG2 = IMG_STAR2
    IMG3 = IMG_STAR3

    def __init__(self):
        self.x = random.randint(0, WIN_WIDTH)
        self.y = random.randint(0, 150)
        self.ANIMATION_TIME = random.randint(6, 15)
        self.image_count = 0

    def draw(self, win):
        # Animation
        if self.image_count <= self.ANIMATION_TIME:
            win.blit(self.IMG1, (self.x, self.y))
        elif self.image_count <= self.ANIMATION_TIME * 2:
            win.blit(self.IMG2, (self.x, self.y))
        elif self.image_count <= self.ANIMATION_TIME * 3:
            win.blit(self.IMG3, (self.x, self.y))

        self.image_count += 1

        if self.image_count > self.ANIMATION_TIME * 3:
            self.image_count = 0


class Bird:
    def __init__(self):
        self.IMG1 = pygame.transform.flip(IMG_BIRD1, True, False)
        self.IMG2 = pygame.transform.flip(IMG_BIRD2, True, False)
        self.x = -self.IMG1.get_width()
        self.y = random.randint(100, 150)
        self.ANIMATION_TIME = random.randint(6, 16)
        self.vel = self.getVel()
        self.image_count = 0

    def move(self):
        self.x += self.vel

    def getVel(self):
        if self.ANIMATION_TIME <= 10:
            return 5
        elif self.ANIMATION_TIME <= 12:
            return 4
        elif self.ANIMATION_TIME <= 14:
            return 3
        else:
            return 2

    def draw(self, win):
        # Animation
        if self.image_count <= self.ANIMATION_TIME:
            win.blit(self.IMG1, (self.x, self.y))
        elif self.image_count <= self.ANIMATION_TIME * 2:
            win.blit(self.IMG2, (self.x, self.y))

        self.image_count += 1

        if self.image_count > self.ANIMATION_TIME * 2:
            self.image_count = 0


class BadBird:
    def __init__(self):
        self.IMG1 = IMG_BADBIRD1
        self.IMG2 = IMG_BADBIRD2
        self.x = WIN_WIDTH
        self.y = self.getY()
        self.ANIMATION_TIME = 8
        self.vel = BASE_VEL
        self.image_count = 0
        self.mask = pygame.mask.from_surface(self.IMG1)
        self.IMG = self.IMG1

    def move(self):
        self.x -= self.vel

    def getY(self):
        chance = random.randint(1, 4)
        if chance <= 1:
            return 275
        elif chance <= 3:
            return 245
        else:
            return 180

    def update_speed(self):
        self.vel = BASE_VEL

    def draw(self, win):
        # Animation
        if self.image_count <= self.ANIMATION_TIME:
            win.blit(self.IMG1, (self.x, self.y))
        elif self.image_count <= self.ANIMATION_TIME * 2:
            win.blit(self.IMG2, (self.x, self.y))

        self.image_count += 1

        if self.image_count > self.ANIMATION_TIME * 2:
            self.image_count = 0


class Cactus:
    SCACTI = IMG_SCACTI
    BCACTI = IMG_BCACTI

    def __init__(self):
        self.vel = BASE_VEL
        self.size = random.randint(1, 2)
        self.num = random.randint(1, 12)
        self.IMG = self.getIMG(self.size, self.num)
        self.x = WIN_WIDTH
        self.y = BASE_LINE - self.IMG.get_height()
        self.gap = self.getGap(self.vel)
        self.mask = pygame.mask.from_surface(self.IMG)

    def getGap(self, vel):
        chance = random.randint(2, 8)

        # Short Gap: Low Speed 150 - 250, High Speed 200 - 350
        if chance <= 2:
            num1 = 150 + (vel - BASE_VEL_INI) / 10 * 50
            num2 = 250 + (vel - BASE_VEL_INI) / 10 * 100

        # Short Gap: Low Speed 250 - 400, High Speed 350 - 550
        elif chance <= 6:
            num1 = 250 + (vel - BASE_VEL_INI) / 10 * 100
            num2 = 400 + (vel - BASE_VEL_INI) / 10 * 150

        # Short Gap: Low Speed 400 - 600, High Speed 550 - 900
        elif chance <= 8:
            num1 = 400 + (vel - BASE_VEL_INI) / 10 * 150
            num2 = 600 + (vel - BASE_VEL_INI) / 10 * 300

        return random.randint(int(num1), int(num2))

    def getIMG(self, size, num):
        # Small cactus
        if size == 1:
            if num <= 3:
                return self.SCACTI[1]
            if num <= 6:
                return self.SCACTI[1]
            if num <= 8:
                if self.vel >= 6:
                    return self.SCACTI[2]
                else:
                    return self.SCACTI[1]
            if num <= 10:
                if self.vel >= 7:
                    return self.SCACTI[3]
                else:
                    return self.SCACTI[2]
            if num <= 11:
                if self.vel >= 10:
                    return self.SCACTI[4]
                else:
                    return self.SCACTI[2]
            if num <= 12:
                if self.vel >= 14:
                    return self.SCACTI[5]
                else:
                    return self.SCACTI[2]

        # Big cactus
        elif size == 2:
            if num <= 3:
                return self.BCACTI[0]
            if num <= 6:
                if self.vel >= 7:
                    return self.BCACTI[1]
                else:
                    return self.BCACTI[0]
            if num <= 8:
                if self.vel >= 9:
                    return self.BCACTI[2]
                else:
                    return self.BCACTI[1]
            if num <= 10:
                if self.vel >= 11:
                    return self.BCACTI[3]
                else:
                    return self.BCACTI[1]
            if num <= 11:
                if self.vel >= 13:
                    return self.BCACTI[4]
                else:
                    return self.BCACTI[1]
            if num <= 12:
                if self.vel >= 15:
                    return self.BCACTI[5]
                else:
                    return self.BCACTI[1]

    def move(self):
        self.x -= self.vel

    def update_speed(self):
        self.vel = BASE_VEL

    def draw(self, win):
        win.blit(self.IMG, (self.x, self.y))


class Rex:
    GRAVITY = 1
    IMG1 = IMG_REX1
    IMG2 = IMG_REX2
    IMG3 = IMG_REX3
    IMG_D1 = IMG_REX_D1
    IMG_D2 = IMG_REX_D2
    IMG1H = IMG_REX1_H
    IMG2H = IMG_REX2_H
    IMG3H = IMG_REX3_H
    IMG_D1H = IMG_REX_D1_H
    IMG_D2H = IMG_REX_D2_H

    def __init__(self):
        self.x = REX_X
        self.Y_INITIAL = BASE_LINE - self.IMG1.get_height()
        self.y = self.Y_INITIAL
        self.image_count = 0
        self.ANIMATION_TIME = 3
        self.jump_time = 0
        self.drop_time = 0
        self.distance = 0
        self.jumped = False
        self.ducked = False
        self.peak = 130
        self.y_peak = self.Y_INITIAL - self.peak
        self.fast_drop = False
        self.mask1 = pygame.mask.from_surface(self.IMG1)
        self.mask2 = pygame.mask.from_surface(self.IMG_D1)
        self.ducked_y = BASE_LINE - self.IMG_D1.get_height()
        self.hurt = False
        self.IMG = None

    def jump(self):
        # Jump
        # Reach peak or ducked
        if self.Y_INITIAL - self.y == self.peak or self.ducked is True:
            self.jumped = False
            self.jump_time = 0
        else:
            self.distance = 5 + abs(25 * self.GRAVITY - 4 * self.jump_time)
            self.jump_time += 1
            if self.y - self.distance < self.y_peak:
                self.y = self.y_peak
            else:
                self.y -= self.distance

    def drop(self):
        # Fast drop when ducked
        if self.fast_drop:
            if self.y < self.Y_INITIAL:
                self.distance = 2 + 1 * self.GRAVITY * self.drop_time + 1 * self.drop_time ** 2

                if self.y + self.distance >= self.Y_INITIAL:
                    self.y = self.Y_INITIAL
                    self.drop_time = 0
                    self.jumped = False
                    self.fast_drop = False
                else:
                    self.y += self.distance
                    self.drop_time += 1

        # Normal drop
        else:
            if self.y < self.Y_INITIAL:
                self.distance = 0.1 + 0.01 * self.GRAVITY * self.drop_time + 0.1 * self.drop_time ** 2

                if self.y + self.distance > self.Y_INITIAL:
                    self.y = self.Y_INITIAL
                    self.drop_time = 0
                    self.jumped = False
                else:
                    self.y += self.distance
                    self.drop_time += 1

    def collide(self, object):
        if self.ducked:
            offset = (round(self.x - object.x), round(self.ducked_y - object.y))
            overlap = object.mask.overlap(self.mask2, offset)
        else:
            offset = (round(self.x - object.x), round(self.y - object.y))
            overlap = object.mask.overlap(self.mask1, offset)

        if overlap:
            return True
        return False

    def draw(self, win):
        # Animation
        if self.hurt:
            if self.y != self.Y_INITIAL:
                win.blit(self.IMG1H, (self.x, self.y))

            # Running not ducking
            elif self.y == self.Y_INITIAL and self.ducked is not True:
                if self.image_count <= self.ANIMATION_TIME:
                    win.blit(self.IMG2H, (self.x, self.y))
                elif self.image_count <= self.ANIMATION_TIME * 2:
                    win.blit(self.IMG3H, (self.x, self.y))

                self.image_count += 1

                if self.image_count > self.ANIMATION_TIME * 2:
                    self.image_count = 0

            # Running and Ducking
            elif self.y == self.Y_INITIAL and self.ducked is True:
                if self.image_count <= self.ANIMATION_TIME:
                    win.blit(self.IMG_D1H, (self.x, BASE_LINE - self.IMG_D1.get_height()))
                elif self.image_count <= self.ANIMATION_TIME * 2:
                    win.blit(self.IMG_D2H, (self.x, BASE_LINE - self.IMG_D1.get_height()))

                self.image_count += 1

                if self.image_count > self.ANIMATION_TIME * 2:
                    self.image_count = 0

        # Jumped in the air
        else:
            if self.y != self.Y_INITIAL:
                win.blit(self.IMG1, (self.x, self.y))

            # Running not ducking
            elif self.y == self.Y_INITIAL and self.ducked is not True:
                if self.image_count <= self.ANIMATION_TIME:
                    win.blit(self.IMG2, (self.x, self.y))
                elif self.image_count <= self.ANIMATION_TIME * 2:
                    win.blit(self.IMG3, (self.x, self.y))

                self.image_count += 1

                if self.image_count > self.ANIMATION_TIME * 2:
                    self.image_count = 0

            # Running and Ducking
            elif self.y == self.Y_INITIAL and self.ducked is True:
                if self.image_count <= self.ANIMATION_TIME:
                    win.blit(self.IMG_D1, (self.x, BASE_LINE - self.IMG_D1.get_height()))
                elif self.image_count <= self.ANIMATION_TIME * 2:
                    win.blit(self.IMG_D2, (self.x, BASE_LINE - self.IMG_D1.get_height()))

                self.image_count += 1

                if self.image_count > self.ANIMATION_TIME * 2:
                    self.image_count = 0


class Healthpack:
    IMG = IMG_HEALTH

    def __init__(self):
        self.x = WIN_WIDTH
        self.y = BASE_LINE - self.IMG.get_height()
        self.vel = BASE_VEL
        self.collected = False
        self.mask = pygame.mask.from_surface(self.IMG)

    def move(self):
        self.x -= self.vel

    def update_speed(self):
        self.vel = BASE_VEL

    def draw(self, win):
        win.blit(self.IMG, (self.x, self.y))


def bound_remove(birds, clouds, cacti, badbirds, healthpacks):
    # Remove bird if out of bound
    for bird in birds:
        if bird.x > WIN_WIDTH:
            birds.remove(bird)

    # Remove cloud if out of bound
    for cloud in clouds:
        if cloud.x + cloud.IMG.get_width() < 0:
            clouds.remove(cloud)

    # Remove cacti if out of bound
    for cactus in cacti:
        if cactus.x + cactus.IMG.get_width() < 0:
            cacti.remove(cactus)

    # Remove bad bird if out of bound
    for badbird in badbirds:
        if badbird.x + badbird.IMG1.get_width() < 0:
            badbirds.remove(badbird)

    # Remove healthpack if out of bound
    for healthpack in healthpacks:
        if healthpack.x + healthpack.IMG.get_width() < 0 or healthpack.collected:
            healthpacks.remove(healthpack)


def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = font.render('FPS: ' + fps, 1, pygame.Color("gray50"))
    return fps_text


def update_score(score):
    score_text = font.render('SCORE: ' + str(int(score)), 1, pygame.Color("gray50"))
    return score_text


def update_speed(base, badbirds, cacti, healthpacks):
    global BASE_VEL

    if BASE_VEL < 15:
        BASE_VEL += 1 / 300

    base.update_speed()

    for badbird in badbirds:
        badbird.update_speed()

    for cactus in cacti:
        cactus.update_speed()

    for healthpack in healthpacks:
        healthpack.update_speed()


def draw_window(win, score, base, moon, stars, clouds, birds, rex, cacti, badbirds, health, healthpacks, high_score,
                rexes):
    # Fill background
    win.fill(BG_COLOR)

    # Base
    base.draw(win)

    # Moon
    moon.draw(win)

    # Stars
    for star in stars:
        star.draw(win)

    # Birds
    for bird in birds:
        bird.move()
        bird.draw(win)

    # Clouds
    for cloud in clouds:
        cloud.move()
        cloud.draw(win)

    # Cacti
    for cactus in cacti:
        cactus.move()
        cactus.draw(win)

    # Bad birds
    for badbird in badbirds:
        badbird.move()
        badbird.draw(win)

    # Rex
    rex.draw(win)

    # Healthpack
    for healthpack in healthpacks:
        healthpack.move()
        healthpack.draw(win)

    # Show FPS
    win.blit(update_fps(), (WIN_WIDTH - 70, 5))

    # Show Score
    win.blit(update_score(score), (5, 5))

    # Show High Score
    high_text = font.render('HI: ' + str(high_score), 1, pygame.Color("gray50"))
    win.blit(high_text, (5, 25))

    # Show Health
    health_text = font.render('LIFE: ', 1, pygame.Color("gray50"))
    win.blit(health_text, (5, 45))
    for i in range(health):
        win.blit(IMG_HEALTH, (45 + 20 * i, 35))

    # Show Texts
    c1 = font3.render('SPACE: Jump', 1, pygame.Color('gray 50'))
    c2 = font3.render('DOWN ARROW: Duck/Fast Drop', 1, pygame.Color('gray 50'))
    c3 = font3.render('Press N to Play Next Song', 1, pygame.Color('gray 50'))
    text_quit = font3.render('Press ESC to Return', 1, pygame.Color('gray 50'))
    win.blit(text_quit, (800, 380))
    win.blit(c1, (420, 360))
    win.blit(c2, (420, 380))
    win.blit(c3, (800, 360))

    # Update
    pygame.display.update()


def draw_ai(win, score, base, moon, stars, clouds, birds, cacti, badbirds, rexes, ai_high_score):
    # Fill background
    win.fill(BG_COLOR)

    # Base
    base.draw(win)

    # Draw Line
    line_width = 1
    if DRAW_LINE:
        if len(cacti) > 0 and len(badbirds) > 0:
            if cacti[0].x < badbirds[0].x:
                for rex in rexes:
                    pygame.draw.line(win, (100, 200, 100),
                                     (rex.x + rex.IMG.get_width() / 2, rex.y + rex.IMG.get_height() / 2), \
                                     (cacti[0].x + cacti[0].IMG.get_width() / 2,
                                      cacti[0].y + cacti[0].IMG.get_height() / 2), line_width)
            else:
                for rex in rexes:
                    pygame.draw.line(win, (200, 100, 100),
                                     (rex.x + rex.IMG.get_width() / 2, rex.y + rex.IMG.get_height() / 2), \
                                     (badbirds[0].x + badbirds[0].IMG.get_width() / 2,
                                      badbirds[0].y + badbirds[0].IMG.get_height() / 2), line_width)
        elif len(cacti) > 0:
            for rex in rexes:
                pygame.draw.line(win, (100, 200, 100),
                                 (rex.x + rex.IMG.get_width() / 2, rex.y + rex.IMG.get_height() / 2), \
                                 (
                                     cacti[0].x + cacti[0].IMG.get_width() / 2,
                                     cacti[0].y + cacti[0].IMG.get_height() / 2),
                                 line_width)
        elif len(badbirds) > 0:
            for rex in rexes:
                pygame.draw.line(win, (200, 100, 100),
                                 (rex.x + rex.IMG.get_width() / 2, rex.y + rex.IMG.get_height() / 2), \
                                 (badbirds[0].x + badbirds[0].IMG.get_width() / 2,
                                  badbirds[0].y + badbirds[0].IMG.get_height() / 2), line_width)

    # Moon
    moon.draw(win)

    # Stars
    for star in stars:
        star.draw(win)

    # Birds
    for bird in birds:
        bird.move()
        bird.draw(win)

    # Clouds
    for cloud in clouds:
        cloud.move()
        cloud.draw(win)

    # Cacti
    for cactus in cacti:
        cactus.move()
        cactus.draw(win)

    # Bad birds
    for badbird in badbirds:
        badbird.move()
        badbird.draw(win)

    # Show FPS
    win.blit(update_fps(), (WIN_WIDTH - 70, 5))

    # Show Score
    win.blit(update_score(score), (5, 5))

    # Show High Score
    high_text = font.render('HI: ' + str(int(ai_high_score)), 1, pygame.Color("gray50"))
    win.blit(high_text, (5, 25))

    # Show Generation
    gen_text = font.render('GEN: ' + str(GEN), 1, pygame.Color("gray50"))
    win.blit(gen_text, (5, 45))

    # Show Alive
    alive_text = font.render('ALIVE: ' + str(len(rexes)), 1, pygame.Color("gray50"))
    win.blit(alive_text, (5, 65))

    # Rexes
    for rex in rexes:
        rex.draw(win)

    # Texts
    c3 = font3.render('Press N to Play Next Song', 1, pygame.Color('gray 50'))
    text_quit = font3.render('Press ESC to Return', 1, pygame.Color('gray 50'))
    win.blit(c3, (800, 360))
    win.blit(text_quit, (800, 380))

    # Update
    pygame.display.update()


def draw_menu(win, base, moon, stars, clouds, birds, rex, game_mode):
    # Fill background
    win.fill(BG_COLOR)

    # Texts
    title_text1 = title_font.render('REX.AI', 1, pygame.Color("gray45"))
    title_text2 = title_font.render('REX.AI', 1, pygame.Color("gray60"))
    win.blit(title_text1, (422, 28))
    win.blit(title_text2, (417, 30))
    menu1 = font2.render('SINGLE PLAYER', 1, pygame.Color("gray45"))
    win.blit(menu1, (420, 150))
    menu2 = font2.render('WATCH AI PLAY', 1, pygame.Color("gray45"))
    win.blit(menu2, (420, 210))

    text1 = font3.render('Press N to Play Next Song', 1, pygame.Color('gray 50'))
    text2 = font3.render('SELECT MODE', 1, pygame.Color('gray 70'))
    text_quit = font3.render('Press ESC to Quit', 1, pygame.Color('gray 50'))
    win.blit(text1, (800, 360))
    win.blit(text2, (460, 130))
    win.blit(text_quit, (800, 380))

    # Show Arrow
    if game_mode == 1:
        win.blit(IMG_ARROW, (385, 143))
    else:
        win.blit(IMG_ARROW, (385, 203))

    # Base
    base.draw(win)

    # Moon
    moon.draw(win)

    # Stars
    for star in stars:
        star.draw(win)

    # Birds
    for bird in birds:
        bird.move()
        bird.draw(win)

    # Clouds
    for cloud in clouds:
        cloud.move()
        cloud.draw(win)

    # Rex
    win.blit(rex.IMG1, (rex.x, rex.y))

    # Update
    pygame.display.update()


def next_song():
    global CURRENT_MUSIC

    next_song = random.choice(MUSIC)
    while next_song == CURRENT_MUSIC:
        next_song = random.choice(MUSIC)
    CURRENT_MUSIC = next_song
    pygame.mixer.music.load(os.path.join('sound', next_song))
    pygame.mixer.music.play(-1)


def single_player(clouds, stars, birds):
    global BASE_VEL, HIGH_SCORE, GAME
    BASE_VEL = BASE_VEL_INI
    base = Base(FLOOR)
    moon = Moon()
    win = WIN
    badbirds = []
    rex = Rex()
    cacti = [Cactus()]
    cacti[0].x = WIN_WIDTH + 100
    score = 0
    run = True
    health = 3
    timer = 0
    damage_timer = 0
    healthpacks = []
    rex.y = -rex.IMG1.get_height()
    GAME += 1

    while run and health > 0:
        # Clock and timers
        timer += 1
        clock.tick(60)
        score += 0.05 + BASE_VEL * 0.05

        # Update game speed
        update_speed(base, badbirds, cacti, healthpacks)
        base.move()

        # Variables
        rex.hurt = False

        # Add birds
        if 1 >= random.randint(1, 300) and len(birds) < 3:
            birds.append(Bird())

        # Check cactus distance
        if cacti[-1].gap >= 500 and cacti[-1].x + cacti[-1].IMG.get_width() <= WIN_WIDTH - 200 \
                and cacti[-1].gap - (WIN_WIDTH - cacti[-1].x - cacti[-1].IMG.get_width()) - BADBIRD_WIDTH >= 200:
            # Add bad birds
            if 1 >= random.randint(1, 4):
                if len(badbirds) == 0:
                    badbirds.append(BadBird())
                else:
                    if WIN_WIDTH - (badbirds[-1].x + BADBIRD_WIDTH) >= 220:
                        badbirds.append(BadBird())

        # Add healthpacks
        if cacti[-1].gap >= 200 and cacti[-1].x + cacti[-1].IMG.get_width() <= WIN_WIDTH - 100 \
                and cacti[-1].gap - (WIN_WIDTH - cacti[-1].x - cacti[-1].IMG.get_width()) - HEALTH_WIDTH >= 100:
            if 1 >= random.randint(1, 600) and len(healthpacks) < 1:
                healthpacks.append(Healthpack())

        # Add clouds
        if 1 >= random.randint(1, 220) and len(clouds) < 4:
            clouds.append(Cloud())

        # Add cacti
        if len(cacti) > 0:
            if cacti[-1].gap <= WIN_WIDTH - (cacti[-1].x + cacti[-1].IMG.get_width()):
                cacti.append(Cactus())

        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Key press
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and rex.y >= rex.Y_INITIAL and rex.ducked is False:
                    rex.jumped = True
                    rex.ducked = False
                if event.key == pygame.K_DOWN:
                    if rex.y != rex.Y_INITIAL:
                        rex.fast_drop = True
                    rex.ducked = True
                if event.key == pygame.K_ESCAPE:
                    menu()
                if event.key == pygame.K_n:
                    next_song()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    rex.ducked = False

        # Check rex duck to change image
        if rex.ducked == True:
            rex.IMG = rex.IMG_D1
        else:
            rex.IMG = rex.IMG1

        # Rex Jump
        if rex.jumped:
            rex.jump()
        else:
            rex.drop()

        # Collision
        for cactus in cacti:
            if rex.collide(cactus):
                if timer - damage_timer >= 5:
                    health -= 1
                damage_timer = timer
                rex.hurt = True

        for badbird in badbirds:
            if rex.collide(badbird):
                if timer - damage_timer >= 5:
                    health -= 1
                damage_timer = timer
                rex.hurt = True

        for healthpack in healthpacks:
            if rex.collide(healthpack):
                health += 1
                healthpack.collected = True

        if health == 0:
            run = False
            if score > HIGH_SCORE:
                HIGH_SCORE = int(score)
            single_player(clouds, stars, birds)

        # Remove sprites if out of bound/collide
        bound_remove(birds, clouds, cacti, badbirds, healthpacks)

        # Draw window
        draw_window(win, score, base, moon, stars, clouds, birds, rex, cacti, badbirds, health, healthpacks, HIGH_SCORE,
                    rexes=None)


def ai_play(genomes, config):
    global AI_HIGH_SCORE, GEN
    base = Base(FLOOR)
    moon = Moon()
    win = WIN
    badbirds = [BadBird()]
    badbirds[0].x = WIN_WIDTH - 300
    cacti = [Cactus()]
    cacti[0].x = WIN_WIDTH
    birds = []
    clouds = [Cloud()]
    stars = []
    for i in range(random.randint(10, 15)): stars.append(Star())
    score = 0
    run = True
    timer = 0
    healthpacks = []

    GEN += 1

    # Create genomes and neural network
    nets = []
    rexes = []
    ge = []
    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        rexes.append(Rex())
        ge.append(genome)

    while run and len(rexes) > 0:
        # Clock and timers
        timer += 1
        clock.tick(200)
        score += 0.05 + BASE_VEL * 0.05

        # Update game speed
        base.move()

        # Check rex duck to change image
        for rex in rexes:
            if rex.ducked:
                rex.IMG = rex.IMG_D1
            else:
                rex.IMG = rex.IMG1

        # Add birds
        if 1 >= random.randint(1, 300):
            birds.append(Bird())

        # Check cactus distance
        if cacti[-1].gap >= 500 and cacti[-1].x + cacti[-1].IMG.get_width() <= WIN_WIDTH - 200 \
                and cacti[-1].gap - (WIN_WIDTH - cacti[-1].x - cacti[-1].IMG.get_width()) - BADBIRD_WIDTH >= 200:
            # Add bad birds
            if 1 >= random.randint(1, 5) and len(badbirds) < 3:
                if len(badbirds) == 0:
                    badbirds.append(BadBird())
                else:
                    if WIN_WIDTH - (badbirds[-1].x + BADBIRD_WIDTH) >= 220:
                        badbirds.append(BadBird())

        # Add clouds
        if 1 >= random.randint(1, 220) and len(clouds) < 4:
            clouds.append(Cloud())

        # Add cacti
        if len(cacti) > 0:
            if cacti[-1].gap <= WIN_WIDTH - (cacti[-1].x + cacti[-1].IMG.get_width()):
                cacti.append(Cactus())

        # Events
        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Key press
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu()
                if event.key == pygame.K_n:
                    next_song()

        # Bad birds and cacti remove list
        badbirds_rem = badbirds
        cacti_rem = cacti

        for x, rex in enumerate(rexes):
            ge[x].fitness += 0.01
            # Collision
            for cactus in cacti:
                if rex.collide(cactus):
                    ge[x].fitness -= 2  # Punish collision
                    # Remove rex
                    nets.pop(x)
                    ge.pop(x)
                    rexes.pop(x)

            for badbird in badbirds:
                if rex.collide(badbird):
                    ge[x].fitness -= 10  # Punish collision
                    # Remove rex
                    nets.pop(x)
                    ge.pop(x)
                    rexes.pop(x)

        # Remove bad birds and cacti if rex crossed
        if len(badbirds_rem) > 0:
            for badbird in badbirds_rem:
                if REX_X - 3 > badbird.x + badbird.IMG1.get_width():
                    badbirds_rem.remove(badbird)
                    # Reward for crossing
                    for x, rex in enumerate(rexes):
                        ge[x].fitness += 10

        if len(cacti_rem) > 0:
            for cactus in cacti_rem:
                if REX_X - 3 > cactus.x + cactus.IMG.get_width():
                    cacti_rem.remove(cactus)
                    # Reward for crossing
                    for x, rex in enumerate(rexes):
                        ge[x].fitness += 2

        # Magic AI stuff
        for x, rex in enumerate(rexes):
            # NN Inputs
            # If cacti and badbirds both exist:
            if len(cacti_rem) > 0 and len(badbirds_rem) > 0:
                if badbirds_rem[0].x < cacti_rem[0].x:
                    output = nets[x].activate(
                        (rex.x, rex.y, 0,
                         0, badbirds_rem[0].x, (rex.y - badbirds_rem[0].y) * 100))
                else:
                    output = nets[x].activate(
                        (rex.x, rex.y, cacti_rem[0].x,
                         cacti[0].y, 0, 0))
            else:
                output = nets[x].activate(
                    (rex.x, rex.y, cacti_rem[0].x,
                     cacti[0].y, 0, 0))

            # Output 0: Jump
            if output[0] > 0.8:
                if rex.y >= rex.Y_INITIAL:
                    rex.jumped = True
            if output[1] > 0.5:
                rex.ducked = False
            if output[2] > 0.5:
                rex.fast_drop = True
                rex.ducked = True

            if rex.jumped:
                rex.jump()
            else:
                rex.drop()

        # Remove sprites if out of bound/collide
        bound_remove(birds, clouds, cacti, badbirds, healthpacks)

        # Draw window
        draw_ai(win, score, base, moon, stars, clouds, birds, cacti, badbirds, rexes, AI_HIGH_SCORE)

    if score > AI_HIGH_SCORE:
        AI_HIGH_SCORE = score


def update_mode(num, game_mode):
    game_mode += num
    if game_mode == 0:
        return 2
    elif game_mode > 2:
        return 1
    return game_mode


def menu():
    global BASE_VEL, HIGH_SCORE
    BASE_VEL = BASE_VEL_INI
    clouds = [Cloud()]
    base = Base(FLOOR)
    moon = Moon()
    stars = []
    for i in range(random.randint(10, 15)): stars.append(Star())
    win = WIN
    birds = []
    rex = Rex()
    game_mode = 1

    while True:
        # Add birds
        if 1 >= random.randint(1, 300) and len(birds) < 3:
            birds.append(Bird())

        # Add clouds
        if 1 >= random.randint(1, 220) and len(clouds) < 4:
            clouds.append(Cloud())

        # Key press
        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Key press
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_n:
                    next_song()
                if event.key == pygame.K_DOWN:
                    game_mode = update_mode(-1, game_mode)
                if event.key == pygame.K_UP:
                    game_mode = update_mode(1, game_mode)
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if game_mode == 1:
                        single_player(clouds, stars, birds)
                    else:
                        BASE_VEL = 15
                        run(CONFIG_PATH)

        draw_menu(win, base, moon, stars, clouds, birds, rex, game_mode)


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(ai_play)

    print('\nBest genome:\n{!s}'.format(winner))

    menu()


if __name__ == '__main__':
    menu()
