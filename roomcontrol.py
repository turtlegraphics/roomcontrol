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
    a: Audio test
    (Also note you only have 1 second after ESC to hit the key)
    """
    if key == 'q':
        sys.exit()
    elif key == 'p':
        global running
        running = not running
    elif key == 'f':
        toggle_fullscreen()
    elif key == 'a':
        print 'Audio check playing...'
        sound.player.play('soundcheck.ogg')
    elif key == 't':
        global training
        if training:
            training = None
            print 'Training off.'
        else:
            training = sys.argv[2]
            print 'Training for',training
        tracker.train(training)

print 'Pygame version',pygame.version.ver
print do_command.__doc__
if len(sys.argv) not in [2,3]:
    print 'Usage: roomcontrol audiopath [trainWORD]'
    sys.exit(1)

# Bring in game modules
import countdown
import gamecontrol
import tracking
import sound

# Initialize
pygame.init()

sound.player.set_path(sys.argv[1])
pygame.display.set_mode((800,800))

pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

# Create spirit game control
game = gamecontrol.Game()

# Create mouse tracking
training = None
tracker = tracking.MouseTrack(gamecontrol.people)

# Create a pygame Clock to track elapsed time
pyclock = pygame.time.Clock()
countdown = countdown.CountdownTimer(3600)

running = False
escape = 0

# main loop
while 1:
    elapsed = pyclock.tick();

    # Timeout escape key press
    escape = max(0,escape - elapsed)

    if running:
        # Advance the countdown clock
        countdown.tick(elapsed)

        # Track mouse movement, if no sound is playing
        if not sound.player.isbusy():
            spirit = tracker.tick(elapsed)
            if spirit:
                game.detected(spirit)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                escape = 1000
            elif escape > 0:
                escape = 0
                do_command(chr(event.key))
        if event.type == pygame.MOUSEBUTTONDOWN:
            running = True
        if event.type == pygame.USEREVENT:
            game.winEvent()

    screen = pygame.display.get_surface()
    screen.fill((0,0,0))
    countdown.draw(screen)
    pygame.display.flip()

