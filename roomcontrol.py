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
from pygame.locals import *

def toggle_fullscreen():
    screen = pygame.display.get_surface()
    tmp = screen.convert()
    w,h = screen.get_width(),screen.get_height()
    flags = screen.get_flags()

    pygame.display.quit()
    pygame.display.init()

    if flags & FULLSCREEN:
        screen = pygame.display.set_mode((w,h))
    else:
        screen = pygame.display.set_mode((w,h),FULLSCREEN)
    screen.blit(tmp,(0,0))
 
# Command handlers
def do_command(key):
    """
    Commands are ESC-key, where key is one of:
    q: Quit
    p: Pause/resume
    f: Toggle fullscreen
    """
    if key == 'q':
        sys.exit()
    if key == 'p':
        global running
        running = not running
    if key == 'f':
        toggle_fullscreen()

print 'Pygame version',pygame.version.ver
print do_command.__doc__

# Bring in game modules
from countdown import CountdownTimer
from tracking import MouseTrack
import sound

# Initialize
pygame.init()

sound.player.set_path(sys.argv[1])
pygame.display.set_mode((800,800))

pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

# Create mouse tracking AI stuff
tracker = MouseTrack()

# Create a pygame Clock to track elapsed time
pyclock = pygame.time.Clock()
countdown = CountdownTimer(3600)

running = False
escape = False

# main loop
while 1:
    elapsed = pyclock.tick();

    if running:
        # Advance the countdown clock
        countdown.tick(elapsed)

        # Track mouse movement, if no sound is playing
        if not sound.player.isbusy():
            detected = tracker.tick(elapsed)
            if detected:
                print 'Going to play: '+detected
                sound.player.play('success.ogg')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                escape = True
            elif escape:
                escape = False
                do_command(chr(event.key))
        if event.type == pygame.MOUSEBUTTONDOWN:
            running = True

    screen = pygame.display.get_surface()
    screen.fill((0,0,0))
    countdown.draw(screen)
    pygame.display.flip()

