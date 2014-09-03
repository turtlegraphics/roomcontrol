#
# Virtual Ouija
#
#   Program to detect motion by a mouse on a Ouija board.
#   Also displays a timer
#
#   Bryan Clair
#   2014
#
import sys
import pygame, pygame.time
from countdown import CountdownTimer

pygame.init()
print 'Pygame version',pygame.version.ver

size = width, height = 800, 800
speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

# Create a pygame Clock to track elapsed time
pyclock = pygame.time.Clock()

countdown = CountdownTimer()

while 1:
    timepassed = pyclock.tick();

    if countdown.tick(timepassed):
        # exit if out of time
        sys.exit()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            print event.rel

    screen.fill(black)
    countdown.draw(screen)
    pygame.display.flip()
