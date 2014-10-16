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
import time
import pygame, pygame.time
from pygame.locals import *

# Bring in game modules
import countdown
import gamecontrol
import tracking

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
        global timechanged
        timechanged = True
    elif key == 'a':
        print 'Audio check playing...'
        pygame.mixer.Sound('soundcheck.wav').play()
    elif key == 't':
        global training
        if training:
            training = None
            print 'Training off.'
        else:
            training = sys.argv[2]
            print 'Training for',training
        tracker.train(training)

def log(msg):
    """Write msg to the logfile for this run."""
    global logfile
    global timer
    logfile.write(str(timer)+' '+msg+'\n')

#
#
#  Program starts here.
#
#

print 'Pygame version',pygame.version.ver
print do_command.__doc__
if len(sys.argv) not in [2,3]:
    print 'Usage: roomcontrol audiopath [trainWORD]'
    sys.exit(1)

# Initialize
pygame.init()

pygame.mixer.init()

pygame.display.set_mode((800,800))

pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

datadir = sys.argv[1]
if not os.path.isdir(datadir):
    raise ValueError('Not a directory: '+datadir)

# Create logfile.  Very lazy - global, and not closed on exit.
logfilename = 'roomlog'+time.strftime('%m-%d %H-%M.txt')
logfile = open(os.path.join(datadir,logfilename),'w')

# Create spirit game control
game = gamecontrol.Game(datadir)

# Create mouse tracking
training = None
tracker = tracking.MouseTrack(game.recognizers)

# Create a pygame Clock to track elapsed time
pyclock = pygame.time.Clock()
timer = countdown.CountdownTimer(10)

# Flag true if countdown is running
running = False

# How much time left on last ESC key pressed (ms)
escape = 0

# Flag to tell if screen needs refresh
timechanged = True

# main loop
while 1:
    elapsed = pyclock.tick(50);

    # Timeout escape key press
    escape = max(0,escape - elapsed)

    if running:
        # Advance the countdown clock
        timechanged = timer.tick(elapsed)

        # Track mouse movement, if no sound is playing
        if not pygame.mixer.get_busy():
            spirit = tracker.tick(elapsed)
            if spirit:
                log(spirit.name + ' invoked')
                game.detected(spirit)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                escape = 1000
            elif escape > 0:
                escape = 0
                do_command(chr(event.key))
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not running:
                log('Clock started')
                running = True
        elif event.type == pygame.USEREVENT:
            game.winEvent()
        elif event.type == pygame.USEREVENT+1:
            log('Out of time')
            pygame.mixer.Sound('timeout.wav').play(loops=4)

    if timechanged:
        screen = pygame.display.get_surface()
        screen.fill((0,0,0))
        timer.draw(screen)
        pygame.display.flip()
        timechanged = False
