import pygame
import os

pygame.init()
pygame.mixer.init()

# initialise some values
WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Level A Demo")
FPS = 60

BG_COLOUR = (125, 125, 125)

def draw(timer):
    # Draws the scene frame by frame

    # get the mouse position
    MOUSE_X, MOUSE_Y = pygame.mouse.get_pos()

    if MOUSE_X > 370:
        MOUSE_X = 370
        SOUND1 = pygame.mixer.Sound(os.path.join('sound_effect1.wav'))
        if timer == 0:
            pygame.mixer.Sound.play(SOUND1)
    # if the mouse passes the red line, trigger sound effect
    elif MOUSE_X < 20:
        MOUSE_X = 20
    if MOUSE_Y > 700:
        MOUSE_Y = 700
    elif MOUSE_Y < 20:
        MOUSE_Y = 20
    # bound the mouse to only part of the screen

    WIN.fill(BG_COLOUR) # make background
    pygame.draw.rect(WIN, (0, 50, 200), (MOUSE_X - 20, MOUSE_Y - 20, 40, 40))
    # making "player" rectangle
    pygame.draw.rect(WIN, (200, 50, 0), (390, 0, 20, 720))
    # making red line
    pygame.display.update()
    # to update the frames


def main():
    clock = pygame.time.Clock()
    running = True
    k = 0
    # this allows the program to run continuously
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # for the timing of the sound effect
        if pygame.mouse.get_pos()[0] > 370:
            k += 1
        else:
            k = 9999999999999
        draw(k % 10000000000000)

    # once the program stops running, quit program
    pygame.quit()

if __name__ == "__main__":
    main()