"""
countdown

Implements class CountdownTimer, which tracks and displays the time
remaining in the game.

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

import pygame
import pygame.font
import pygame.color

class CountdownTimer:
    """Create a countdown timer on screen"""
    def __init__(self,time):
        """Set up a timer with time seconds available."""
        # self.time tracks time left in full accuracy.
        self.time = time
        # self.oldtime is the last rendered time string
        self.oldtime = None

        self.outoftime = False

        pygame.font.init()
        self.font = pygame.font.Font(None, 256)  # 256 point
        self.render()
        
        # set 1/2 image width only once, at start, so it doesn't jitter
        (self.mx,self.my) = self.image.get_rect().center

    def __str__(self):
        t = round(self.time,1)
        minutes = int(t/60)
        seconds = t - 60*minutes
        return '%02d:%04.1f' % (minutes,seconds)

    def render(self):
        """Build the text image of the given time.  Return True if changed."""
        timestr = str(self)
        if timestr != self.oldtime:
            if self.outoftime:
                color = pygame.Color('red')
            else:
                color = pygame.Color('white')
            self.image = self.font.render(timestr,True,color)
            self.oldtime = timestr
            return True
        else:
            return False

    def tick(self,timepassed):
        """Decrease current time by timepassed (ms) and rebuild image.
           Return True if display has changed."""
        self.time -= float(timepassed)/1000.0
        if self.time < 0:
            self.time = 0
            if not self.outoftime:
                self.outoftime = True
                self.oldtime = None  # force re-render
                pygame.event.post(pygame.event.Event(pygame.USEREVENT+1))

        return self.render()

    def draw(self,surf):
        (cx,cy) = surf.get_rect().center
        surf.blit(self.image,(cx-self.mx,cy-self.my))

timer = CountdownTimer(3600)
