import pygame
import random

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Arial', 30)

# initialise some values
WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Level B Demo")
FPS = 60

BG_COLOUR = (125, 125, 125)

LEVEL1 = [(120, 200), (320, 200), (520, 200), (720, 200), (920, 200)]
LEVEL2 = [(120, 200), (320, 200), (520, 200), (720, 200), (920, 200),
          (120, 600), (320, 600), (520, 600), (720, 600), (920, 600)]
LEVEL3 = [(120, 200), (320, 200), (520, 200), (720, 200), (920, 200),
          (420, 200), (620, 200), (820, 200), (1020, 200), (1220, 200),
          (120, 600), (320, 600), (520, 600), (720, 600), (920, 600)]
LEVEL4 = [(120, 200), (320, 200), (520, 200), (720, 200), (920, 200),
          (420, 200), (620, 200), (820, 200), (1020, 200), (1220, 200),
          (120, 600), (320, 600), (520, 600), (720, 600), (920, 600),
          (420, 500), (620, 500), (820, 500), (1020, 500), (1220, 500)]
LEVEL5 = [(120, 100), (320, 100), (520, 100), (720, 100), (920, 100),
          (420, 200), (620, 200), (820, 200), (1020, 200), (1220, 200),
          (120, 600), (320, 600), (520, 600), (720, 600), (920, 600),
          (420, 500), (620, 500), (820, 500), (1020, 500), (1220, 500),
          (420, 650), (620, 650), (820, 650), (1020, 650), (1220, 650)]

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

    def display(self):
        pygame.draw.circle(WIN, (0, 50, 200), (self.x, self.y), 40)
        pygame.draw.circle(WIN, (200, 200, 200), (self.x, self.y), 30)


class Enemy(Entity):

    def __init__(self, x, y):
        super().__init__(x, y, 1)
        self.direction = "down"

    def display(self):
        pygame.draw.rect(WIN, (200, 120, 120), (self.x, self.y, 28, 28))
        if self.direction == "down" and self.y < 692:
            self.move_down()
        if self.direction == "up" and self.y > 0:
            self.move_up()
        if self.direction == "left" and self.x > 0:
            self.move_left()
        if self.direction == "right" and self.x < 1252:
            self.move_right()


    def change_dir(self):
        d = random.randint(0, 3)
        ls = ["down", "up", "left", "right"]
        self.direction = ls[d]


class Game:

    LASER_COLOUR = 125, 125, 125
    def __init__(self, level):
        self.enemies = []
        for coord in level:
            self.enemies.append(Enemy(coord[0], coord[1]))
        self.player = Player(640, 360, 4)
        self.firing = False
        self.LASER_COLOUR = 125, 125, 125
        self.timer = 0


    def draw(self):
        # Draws the scene frame by frame

        WIN.fill(BG_COLOUR)
        MOUSE_X, MOUSE_Y = pygame.mouse.get_pos()

        is_left = pygame.mouse.get_pressed()[0] # is left click

        self.firing = is_left and self.timer % 40 in range(0, 14)

        if self.firing:
            LASER_COLOUR = 210, 60, 60
        else:
            LASER_COLOUR = 125, 125, 125

        pygame.draw.line(WIN, LASER_COLOUR, (self.player.x, self.player.y),
                         (512 * (MOUSE_X - self.player.x),
                          512 * (MOUSE_Y - self.player.y)))


        self.player.display()

        laser_coords = [(20/i * (MOUSE_X - self.player.x) + self.player.x,
                         20/i * (MOUSE_Y - self.player.y) + self.player.y) for i in range(1, 200)]


        for e in self.enemies:
            if self.firing:
                for coords in laser_coords:
                    if abs(coords[0] - e.x) < 19 and abs(coords[1] - e.y) < 19:
                        try:
                            self.enemies.remove(e)
                        except ValueError:
                            print("Error handler")

            if self.timer % 50 == 0 or e.x < 1 or e.y < 1 or e.x > 1251 or e.y > 691:
                e.change_dir()
            e.display()


        ke = pygame.key.get_pressed()
        if ke[pygame.K_a]:
            self.player.move_left()
        if ke[pygame.K_w]:
            self.player.move_up()
        if ke[pygame.K_d]:
            self.player.move_right()
        if ke[pygame.K_s]:
            self.player.move_down()

        self.timer += 1

        pygame.display.update()
        print(len(self.enemies))
        return len(self.enemies)
        # to update the frames


def main():
    clock = pygame.time.Clock()
    running = True
    g = Game(LEVEL1)
    # this allows the program to run continuously

    def play(game, r):
        while running:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    r = False
            text = font.render(f'Level 1', False, (255, 255, 255))
            num = game.draw()
            WIN.blit(text, (50, 50))
            if num == 0:
                break

    play(g, running)
    g = Game(LEVEL2)
    play(g, running)
    g = Game(LEVEL3)
    play(g, running)
    g = Game(LEVEL4)
    play(g, running)
    g = Game(LEVEL5)
    play(g, running)
    g = Game(LEVEL1)

    # once the program stops running, quit program
    pygame.quit()

if __name__ == "__main__":
    main()