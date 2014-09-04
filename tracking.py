"""
tracking

Implements class MouseTrack, which converts mouse motion into discrete
vectors separated by pauses.

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

pause_threshhold = 100  # ms of no motion for the mouse to be 'stopped'

class Move:
    """Represents one continuous movement of the mouse"""
    def __init__(self, v = (0,0)):
        self.x,self.y = v
    def __iadd__(self,other):
        self.x += other.x
        self.y += other.y
        return self
    def __str__(self):
        return '('+str(self.x)+','+str(self.y)+')'

class MouseTrack:
    """Process mouse motion into discrete vectors separated by pauses"""
    def __init__(self):
        self.still = True
        self.stilltime = 0
        self.vector = Move()

    def tick(self,elapsed):
        """Call periodically."""
        rel = pygame.mouse.get_rel()
        if rel == (0,0):
            self.stilltime += elapsed
            if not self.still and self.stilltime > pause_threshhold:
                print 'moved by:',self.vector
                self.still = True
                self.vector = Move()
        else:
            self.vector += Move(rel)
            # self.vector = tuple(map(sum,zip(self.vector,rel))) # addition hack
            self.still = False
            self.stilltime = 0
