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

import sys,os
import pygame, pygame.time
from pygame.locals import *

# Bring in game modules
import countdown
import gamecontrol
import tracking
from logging import logger

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

    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

class RoomController:
    def __init__(self):
        # Create a pygame Clock to track elapsed time
        self.pyclock = pygame.time.Clock()

        # Create spirit game control
        self.game = gamecontrol.Game(datadir)

        # Create mouse tracking
        self.training = None
        self.tracker = tracking.MouseTrack(self.game.recognizers)

        # Flag true if countdown is running
        self.running = False

        # How much time left on last ESC key pressed (ms)
        self.escape = 0

        # Flag to tell if screen needs refresh
        self.timechanged = True

    def run(self):
        # main loop
        while 1:
            elapsed = self.pyclock.tick(50);

            # Timeout escape key press
            self.escape = max(0,self.escape - elapsed)

            if self.running:
                # Advance the countdown clock
                self.timechanged = countdown.timer.tick(elapsed)

                # Track mouse movement, if no sound is playing
                if not pygame.mixer.get_busy():
                    spirit = self.tracker.tick(elapsed)
                    if spirit:
                        self.game.detected(spirit)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    logger.close()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.escape = 600
                    elif self.escape > 0:
                        self.escape = 0
                        self.do_command(chr(event.key))
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.running:
                        logger.log('Clock started')
                        self.running = True
                elif event.type == pygame.USEREVENT:
                    self.game.winEvent()
                elif event.type == pygame.USEREVENT+1:
                    logger.log('Out of time')
                    pygame.mixer.stop()
                    pygame.mixer.Sound('timeout.wav').play(loops=4)

            if self.timechanged:
                screen = pygame.display.get_surface()
                screen.fill((0,0,0))
                countdown.timer.draw(screen)
                pygame.display.flip()
                self.timechanged = False

    # Command handlers
    def do_command(self,key):
        """
        Commands are ESC-key, where key is one of:
        q: Quit
        p: Pause/resume
        f: Toggle fullscreen
        a: Audio test
        (Also note you only have 1 second after ESC to hit the key)
        """
        if key == 'q':
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        elif key == 'p':
            self.running = not self.running
        elif key == 'f':
            toggle_fullscreen()
            self.timechanged = True
        elif key == 'a':
            print 'Audio check playing...'
            pygame.mixer.Sound('soundcheck.wav').play()
        elif key == 't':
            if self.training:
                self.training = None
                print 'Training off.'
            else:
                self.training = sys.argv[2]
                print 'Training for',self.training
            self.tracker.train(self.training)

#
# Program begins here
#

print 'Pygame version',pygame.version.ver
print RoomController.do_command.__doc__
if len(sys.argv) not in [2,3]:
    print 'Usage: roomcontrol audiopath [trainWORD]'
    sys.exit(1)

datadir = sys.argv[1]
if not os.path.isdir(datadir):
    raise ValueError('Not a directory: '+datadir)

# create logfile
logger.open(datadir)

# Initialize
pygame.init()

pygame.mixer.init()

pygame.display.set_mode((800,800))

pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

RoomController().run()
