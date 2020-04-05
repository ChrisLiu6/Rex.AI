import pygame
import os
import neat
import random

pygame.font.init()
pygame.mixer.init()

# Window Parameters
WIN_WIDTH = 1000
WIN_HEIGHT = 700
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
BG_COLOR = (235, 235, 235)
pygame.display.set_caption("Rex.AI")
WIN.fill(BG_COLOR)

# Sprite Parameters
FLOOR = 470
BASE_LINE = 490
BASE_VEL = 15

# Load Pictures
IMG_BASE = pygame.image.load(os.path.join('img', 'background.png'))
IMG_BIRD1 = pygame.image.load(os.path.join('img', 'bird1.png'))
IMG_BIRD2 = pygame.image.load(os.path.join('img', 'bird2.png'))
IMG_CACTUS1 = pygame.image.load(os.path.join('img', 'cactus1.png'))
IMG_CACTUS2 = pygame.image.load(os.path.join('img', 'cactus2.png'))
IMG_CACTUS3 = pygame.image.load(os.path.join('img', 'cactus3.png'))
IMG_CACTUS4 = pygame.image.load(os.path.join('img', 'cactus4.png'))
IMG_CLOUD = pygame.image.load(os.path.join('img', 'cloud.png'))
IMG_DINO1 = pygame.image.load(os.path.join('img', 'dino1.png'))
IMG_DINO2 = pygame.image.load(os.path.join('img', 'dino2.png'))
IMG_MOON = pygame.image.load(os.path.join('img', 'moon.png'))
IMG_REX1 = pygame.image.load(os.path.join('img', 'rex1.png'))
IMG_REX2 = pygame.image.load(os.path.join('img', 'rex2.png'))
IMG_REX3 = pygame.image.load(os.path.join('img', 'rex3.png'))
IMG_STAR1 = pygame.transform.scale2x(pygame.image.load(os.path.join('img', 'star1.png')))
IMG_STAR2 = pygame.transform.scale2x(pygame.image.load(os.path.join('img', 'star2.png')))
IMG_SUN = pygame.image.load(os.path.join('img', 'sun.png'))
IMG_THUG = pygame.image.load(os.path.join('img', 'thug_glasses.png'))


class Base:
    VEL = BASE_VEL
    WIDTH = IMG_BASE.get_width()
    IMG = IMG_BASE

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


class Cloud:
    IMG = IMG_CLOUD
    IMG_GLASS = IMG_THUG

    def __init__(self):
        self.x = WIN_WIDTH
        self.y = random.randint(60, 180)
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
        self.y = 80

    def draw(self, win):
        win.blit(self.IMG, (self.x, self.y))


class Bird:
    def __init__(self):
        self.x = -26
        self.IMG1 = pygame.transform.flip(IMG_BIRD1, True, False)
        self.IMG2 = pygame.transform.flip(IMG_BIRD2, True, False)
        self.y = random.randint(180, 330)
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


class Rex:
    GRAVITY = 1
    IMG1 = IMG_REX1
    IMG2 = IMG_REX2
    IMG3 = IMG_REX3
    IMG_D1 = IMG_DINO1
    IMG_D2 = IMG_DINO2

    def __init__(self):
        self.x = 50
        self.Y_INITIAL = BASE_LINE - self.IMG1.get_height()
        self.y = self.Y_INITIAL
        self.image_count = 0
        self.ANIMATION_TIME = 2
        self.jump_time = 0
        self.drop_time = 0
        self.distance = 0
        self.jumped = False
        self.ducked = False
        self.peak = 150
        self.y_peak = self.Y_INITIAL - self.peak

    def jump(self):
        # Jump
        # Reach peak or ducked
        if self.Y_INITIAL - self.y == self.peak or self.ducked is True:
            self.jumped = False
            self.jump_time = 0
        else:
            self.distance = 5 + abs(40 * self.GRAVITY - 8 * self.jump_time)
            self.jump_time += 1
            if self.y - self.distance < self.y_peak:
                self.y = self.y_peak
            else:
                self.y -= self.distance

    def drop(self):
        # Fast drop when ducked
        if self.ducked is True:
            if self.y < self.Y_INITIAL:
                self.distance = 20 + 2 * self.GRAVITY * self.drop_time + 3 * self.drop_time ** 2

                if self.y + self.distance > self.Y_INITIAL:
                    self.y = self.Y_INITIAL
                    self.drop_time = 0
                    self.jumped = False
                else:
                    self.y += self.distance
                    self.drop_time += 1
        # Normal drop
        else:
            if self.y < self.Y_INITIAL:
                self.distance = 3 + 0.8 * self.GRAVITY * self.drop_time + 1 * self.drop_time ** 2

                if self.y + self.distance > self.Y_INITIAL:
                    self.y = self.Y_INITIAL
                    self.drop_time = 0
                    self.jumped = False
                else:
                    self.y += self.distance
                    self.drop_time += 1

    def draw(self, win):
        # Animation
        # Jumped in the air
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


def remove(birds, clouds):
    # Remove bird if out of bound
    for bird in birds:
        if bird.x > WIN_WIDTH:
            birds.remove(bird)

    # Remove cloud if out of bound
    for cloud in clouds:
        if cloud.x + cloud.IMG.get_width() < 0:
            clouds.remove(cloud)


def draw_window(win, base, moon, clouds, birds, rex):
    # Fill background
    win.fill(BG_COLOR)

    # Base
    base.draw(win)

    # Moon
    moon.draw(win)

    # Birds
    for bird in birds:
        bird.move()
        bird.draw(win)

    # Clouds
    for cloud in clouds:
        cloud.move()
        cloud.draw(win)

    # Rex
    rex.draw(win)

    # Update
    pygame.display.update()


def main_single():
    clouds = [Cloud()]
    base = Base(FLOOR)
    moon = Moon()
    clock = pygame.time.Clock()
    win = WIN
    birds = []
    chance = 1
    rex = Rex()

    while True:
        clock.tick(100)

        base.move()

        # Add birds
        if chance >= random.randint(1, 250) and len(birds) < 2:
            birds.append(Bird())

        # Add clouds
        if chance >= random.randint(1, 220) and len(clouds) < 4:
            clouds.append(Cloud())

        # Remove sprites if out of bound
        remove(birds, clouds)

        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Key press
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and rex.y == rex.Y_INITIAL and rex.ducked is False:
                    rex.jumped = True
                    rex.ducked = False
                if event.key == pygame.K_s:
                    rex.ducked = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    if rex.jumped is False:
                        rex.ducked = False

        # Rex Jump
        if rex.jumped:
            rex.jump()
        else:
            rex.drop()



        # Draw window
        draw_window(win, base, moon, clouds, birds, rex)


# def run(config_path):
#     config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
#                                 neat.DefaultSpeciesSet, neat.DefaultStagnation,
#                                 config_path)
#     p = neat.Population(config)
#     p.add_reporter(neat.StdOutReporter(True))
#     stats = neat.StatisticsReporter()
#     p.add_reporter(stats)
#
#     winner = p.run(main, 50)
#
#     print('\nBest genome:\n{!s}'.format(winner))

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'NEAT_config.txt')
    # run(config_path)
    main_single()
