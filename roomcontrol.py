"""
roomcontrol

Program to operate a locked room puzzle game.

- Displays the game's countdown timer.

- Handles mouse tracking for one of the game puzzles.
  The mouse is moved on a Ouija board and the program detects if certain
  words have been spelled, then plays a prerecorded sound.

Copyright (C) 2014 Bryan Clair (bryan@slu.edu)

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

import sys
import pygame, pygame.time
from countdown import CountdownTimer
from tracking import MouseTrack

pygame.init()
print 'Pygame version',pygame.version.ver

size = width, height = 800, 800
speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

# Create mouse tracking AI stuff
tracker = MouseTrack()

# Create a pygame Clock to track elapsed time
pyclock = pygame.time.Clock()
countdown = CountdownTimer(6000)

# main loop
started = False
while 1:
    elapsed = pyclock.tick();

    if started:
        # Advance the countdown clock
        if countdown.tick(elapsed):
            # exit if out of time
            sys.exit()
        # Track mouse movement
        tracker.tick(elapsed)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.key == pygame.K_RETURN:
                started = True

    screen.fill(black)
    countdown.draw(screen)
    pygame.display.flip()
