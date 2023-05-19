import csv
from objects import *


def enemy_spawn(*args):
    borders = ((-200, -100), (1380, 1480)), ((-200, -100), (820, 920))
    spawn_pos = []

    def make_list(enemy_type):
        x_or_y = random.randint(0, 1)
        l_bound, u_bound = random.choice(borders[x_or_y])
        if x_or_y == 0:
            spawn_pos.append((random.randint(l_bound, u_bound),
                             random.randint(-200, 920), enemy_type))
        else:
            spawn_pos.append((random.randint(-200, 1480),
                             random.randint(l_bound, u_bound), enemy_type))

    for i in range(5):
        for _ in range(args[i]):
            make_list(i)

    return spawn_pos


def read_csv(filename):
    try:
        with open(filename, 'r', encoding='utf8', newline='') as f:
            rf = csv.reader(f)
            raw_dat = [row for row in rf if row != []]
            lev_dat = []
            for i in range(len(raw_dat)):
                for j in range(len(raw_dat[i])):
                    raw_dat[i][j] = int(raw_dat[i][j])
            for x in range(len(raw_dat)):
                lev_dat.append(enemy_spawn(raw_dat[x][0], raw_dat[x][1],
                                           raw_dat[x][2], raw_dat[x][3],
                                           raw_dat[x][4]))
            return lev_dat

    except FileNotFoundError:
        pass


LEVEL1 = read_csv("level1.csv")
LEVEL2 = read_csv("level2.csv")
LEVEL3 = read_csv("level3.csv")
LEVEL4 = read_csv("level4.csv")
LEVEL5 = read_csv("level5.csv")


def blit_alpha(target, source, location, opacity):
    # https://nerdparadise.com/programming/pygameblitopacity
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)
    target.blit(temp, location)


class Menu:

    def __init__(self):
        pygame.mixer.music.load(f'menu.wav')
        pygame.mixer.music.play(-1)
        self.button_col = 10, 10, 10

    def draw(self):
        WIN.fill(BG_COLOUR)
        MOUSE_X, MOUSE_Y = pygame.mouse.get_pos()

        menu_font =

        pygame.draw.rect(WIN, self.button_col, (400, 425, 480, 160))
        pygame.display.update()
        if 400 < MOUSE_X < 880 and 225 < MOUSE_Y < 385:
            if pygame.mouse.get_pressed()[0]:
                pygame.mixer.music.load('music1.wav')
                pygame.mixer.music.play(-1)
                return 0
            else:
                self.button_col = 50, 50, 50
        else:
            self.button_col = 10, 10, 10


class Game:

    LASER_COLOUR = 125, 125, 125
    def __init__(self, level_data, level_num):
        self.wave = 1
        self.level_data = level_data
        self.level_num = level_num
        self.enemies = []
        self.new_wave()
        self.player = Player(640, 360, 4)
        self.firing = False
        self.LASER_COLOUR = 125, 125, 125
        self.timer = 0
        pygame.mixer.music.load(f'music{level_num}.wav')
        pygame.mixer.music.play(-1)


    def new_wave(self):
        for coord in self.level_data[self.wave - 1]:
            if coord[2] == 0:
                self.enemies.append(NormalEnemy(coord[0], coord[1]))
            elif coord[2] == 1:
                self.enemies.append(FastEnemy(coord[0], coord[1]))
            elif coord[2] == 2:
                self.enemies.append(TankyEnemy(coord[0], coord[1]))
            elif coord[2] == 3:
                self.enemies.append(RegenEnemy(coord[0], coord[1]))
            else:
                self.enemies.append(BossEnemy(coord[0], coord[1]))


    def draw(self):
        # Draws the scene frame by frame
        WIN.fill(BG_COLOUR)
        MOUSE_X, MOUSE_Y = pygame.mouse.get_pos()
        ke = pygame.key.get_pressed()
        shooting = pygame.mouse.get_pressed()[0] or ke[pygame.K_SPACE]
        fx = pygame.mixer.Sound(f"laser_sound{random.randint(1, 4)}.mp3")
        self.firing = shooting and self.timer % 40 in range(0, 14)

        if self.firing:
            if self.timer % 40 in range(0, 1):
                pygame.mixer.Sound.play(fx)
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
                    if abs(coords[0] - e.x) < 24 and abs(coords[1] - e.y) < 24:
                        e.health -= 1
                        if e.health <= 0:
                            try:
                                self.enemies.remove(e)
                            except ValueError:
                                pass
            if abs(self.player.x - e.x) < 19 and abs(self.player.y - e.y) < 19:
                self.player.health -= 1
            e.move(self.player.x, self.player.y)
            e.display()


        if ke[pygame.K_a] and self.player.x > 20:
            self.player.move_left()
        if ke[pygame.K_w] and self.player.y > 20:
            self.player.move_up()
        if ke[pygame.K_d] and self.player.x < 1260:
            self.player.move_right()
        if ke[pygame.K_s] and self.player.y < 700:
            self.player.move_down()

        level_font = pygame.font.SysFont('Arial', 30)
        level_surface = level_font.render(f'Level {self.level_num}', False, "white")

        wave_font = pygame.font.SysFont('Arial', 24)
        wave_surface = wave_font.render(f'Wave #{self.wave}', False, "white")

        pygame.draw.rect(WIN, (244, 150, 20, 120), (1040, 650, 200, 40))
        pygame.draw.rect(WIN, (244, 244, 20, 120),
                         (1040, 650, 200 * (len(self.enemies) / len(self.level_data[self.wave - 1])), 40))

        blit_alpha(WIN, level_surface, (600, 680), 127)
        blit_alpha(WIN, wave_surface, (1100, 600), 126)

        self.timer += 1

        pygame.display.update()

        if len(self.enemies) == 0:
            if self.wave == len(self.level_data):
                return 0
            else:
                self.wave += 1
                self.new_wave()

        # to update the frames


def main():
    clock = pygame.time.Clock()
    running = True
    g = Game(LEVEL1, 1)
    m = Menu()
    # this allows the program to run continuously

    def play(screen, r):
        while running:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
            num = screen.draw()
            if num == 0 or not r:
                break

    play(m, running)
    play(g, running)
    g = Game(LEVEL2, 2)
    play(g, running)
    g = Game(LEVEL3, 3)
    play(g, running)
    g = Game(LEVEL4, 4)
    play(g, running)
    g = Game(LEVEL5, 5)
    play(g, running)

    # once the program stops running, quit program
    pygame.quit()

if __name__ == "__main__":
    main()