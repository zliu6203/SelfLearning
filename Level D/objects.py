from abc import ABC, abstractmethod
import random
import pygame

pygame.init()
pygame.font.init()
pygame.mixer.init()

# initialise some values
WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Level D Demo")
FPS = 60

BG_COLOUR = (125, 125, 125)

class Entity:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

    def move_up(self):
        self.y -= self.speed

    def move_down(self):
        self.y += self.speed

    def move_left(self):
        self.x -= self.speed

    def move_right(self):
        self.x += self.speed

class Player(Entity):

    def __init__(self, x, y, speed):
        super().__init__(x, y, speed)
        self.maxhealth = 200
        self.health = self.maxhealth


    def display(self):
        if self.health < self.maxhealth:
            pygame.draw.rect(WIN, "red", (self.x - 30, self.y - 35, 60, 10))
            pygame.draw.rect(WIN,
                             "green", (self.x - 30, self.y - 35,
                                       (self.health * 60) / self.maxhealth, 10))
        pygame.draw.circle(WIN, (237, 123, 36), (self.x, self.y), 20)
        pygame.draw.rect(WIN, (242, 212, 189), (self.x - 15, self.y - 8, 12, 12))
        pygame.draw.rect(WIN, (242, 212, 189), (self.x + 1, self.y - 8, 12, 12))
        pygame.draw.rect(WIN, (84, 37, 0), (self.x - 10, self.y - 2, 6, 6))
        pygame.draw.rect(WIN, (84, 37, 0), (self.x + 2, self.y - 2, 6, 6))


class Enemy(Entity):

    def __init__(self, x, y):
        super().__init__(x, y, 0)
        self.s = random.randrange(5, 21) / 10

    def show_healthbar(self, health, maxhealth, threshold_x = -6, threshold_y = 15):
        pygame.draw.rect(WIN,
                         "red", (self.x + threshold_x, self.y - threshold_y,
                                 40, 5))
        pygame.draw.rect(WIN,
                         "green", (self.x + threshold_x, self.y - threshold_y,
                                   (health * 40) / maxhealth, 5))

    @abstractmethod
    def display(self):
        pass

    def move(self, x, y):
        # follow player
        if self.x - x + 12 > 0:
            self.move_left()
        elif self.x - x + 12 < 0:
            self.move_right()
        if self.y - y + 11 > 0:
            self.move_up()
        elif self.y - y + 11 < 0:
            self.move_down()


class NormalEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.s = random.randint(5, 13) / 10
        self.maxhealth = random.randint(28, 38)
        self.health = self.maxhealth

    def display(self):
        pygame.draw.rect(WIN, (120, 200, 120), (self.x, self.y, 28, 28))
        if self.x <= -200 or self.x >= 1480 or self.y <= -200 or self.y >= 920:
            self.speed = 5
        else:
            self.speed = self.s
        if 0 < self.x + 14 < 1280 and 0 < self.y + 14 < 720:
            pygame.draw.circle(WIN, "white", (self.x + 14, self.y + 14), 10)
            pygame.draw.circle(WIN, (30, 200, 30), (self.x + 14, self.y + 14), 3)

        if self.health < self.maxhealth:
            self.show_healthbar(self.health, self.maxhealth)


class FastEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.s = random.randint(14, 20) / 10
        self.maxhealth = random.randint(18, 28)
        self.health = self.maxhealth

    def display(self):
        if self.x <= -200 or self.x >= 1480 or self.y <= -200 or self.y >= 920:
            self.speed = 5
        else:
            self.speed = self.s
        pygame.draw.rect(WIN, (200, 120, 120), (self.x, self.y, 28, 28))

        if 0 < self.x + 14 < 1280 and 0 < self.y + 14 < 720:
            pygame.draw.circle(WIN, "white", (self.x + 14, self.y + 14), 10)
            pygame.draw.circle(WIN, (255, 100, 100), (self.x + 14, self.y + 14), 2)
            pygame.draw.rect(WIN, (200, 120, 120), (self.x, self.y, 28, 8))


        if self.health < self.maxhealth:
            self.show_healthbar(self.health, self.maxhealth)


class TankyEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.s = random.randint(4, 8) / 10
        self.maxhealth = random.randint(80, 100)
        self.health = self.maxhealth

    def display(self):
        if self.x <= -200 or self.x >= 1480 or self.y <= -200 or self.y >= 920:
            self.speed = 5
        else:
            self.speed = self.s
        pygame.draw.rect(WIN, (120, 120, 200), (self.x, self.y, 28, 28))
        if 0 < self.x + 8 < 1280 and 0 < self.y + 8 < 720:
            if self.health / self.maxhealth < 0.5:
                pygame.draw.rect(WIN, (36, 237, 234), (self.x + 5, self.y + 14, 6, 14))
                pygame.draw.rect(WIN, (36, 237, 234), (self.x + 17, self.y + 14, 6, 14))
            pygame.draw.circle(WIN, (200, 200, 255), (self.x + 8, self.y + 14), 5)
            pygame.draw.circle(WIN, "blue", (self.x + 8, self.y + 14), 2)
            pygame.draw.circle(WIN, (200, 200, 255), (self.x + 20, self.y + 14), 5)
            pygame.draw.circle(WIN, "blue", (self.x + 20, self.y + 14), 2)

        if self.health < self.maxhealth:
            self.show_healthbar(self.health, self.maxhealth)


class RegenEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.s = random.randint(9, 18) / 10
        self.maxhealth = random.randint(50, 80)
        self.health = self.maxhealth
        self.timer = 0

    def display(self):
        self.timer += 1
        if self.x <= -200 or self.x >= 1480 or self.y <= -200 or self.y >= 920:
            self.speed = 5
        else:
            self.speed = self.s
        pygame.draw.rect(WIN, (176, 63, 144), (self.x, self.y, 28, 28))
        if 0 < self.x + 8 < 1280 and 0 < self.y + 8 < 720:
            pygame.draw.circle(WIN, (204, 161, 192), (self.x + 14, self.y + 14), 10)
            eye_font = pygame.font.SysFont('Arial', 30)
            eye_surface = eye_font.render(f'X', False, "Red")
            WIN.blit(eye_surface, (self.x + 6, self.y - 2))

        if self.health < self.maxhealth:
            self.show_healthbar(self.health, self.maxhealth)
            if self.timer % 2:
                self.health += 1


class BossEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.s = random.randint(12, 22) / 10
        self.maxhealth = random.randint(900, 1100)
        self.health = self.maxhealth
        self.timer = 0


    def display(self):
        self.timer += 1
        if self.x <= -200 or self.x >= 1480 or self.y <= -200 or self.y >= 920:
            self.speed = 5
        else:
            self.speed = self.s

        pygame.draw.rect(WIN, (10, 10, 10), (self.x, self.y, 60, 60))
        if 0 < self.x + 8 < 1280 and 0 < self.y + 8 < 720:
            pygame.draw.ellipse(WIN, (255, 100, 100), (self.x + 8, self.y + 10, 10, 30))
            pygame.draw.circle(WIN, "red", (self.x + 12, self.y + 24), 2)
            pygame.draw.circle(WIN, (200, 200, 255), (self.x + 48, self.y + 26), 5)
            pygame.draw.circle(WIN, "blue", (self.x + 48, self.y + 26), 2)
            pygame.draw.circle(WIN, (204, 161, 192), (self.x + 30, self.y + 30), 12)
            eye_font = pygame.font.SysFont('Comic Sans', 36)
            eye_surface = eye_font.render(f'X', False, "Red")
            WIN.blit(eye_surface, (self.x + 15, self.y))
        if self.health / self.maxhealth < 0.5:
            pygame.draw.rect(WIN, (36, 237, 234), (self.x + 46, self.y + 28, 6, 33))


        if self.health < self.maxhealth:
            self.show_healthbar(self.health, self.maxhealth, threshold_x=9, threshold_y=20)
            if self.timer % 20:
                if self.health / self.maxhealth > 0.5:
                    self.health += 1
                    self.speed = random.randint(18, 24) / 10
                else:
                    self.health += 2
                    self.speed = random.randint(24, 30) / 10