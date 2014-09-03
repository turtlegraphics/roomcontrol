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

class MouseTrack:
    """Process mouse motion into discrete vectors separated by pauses"""
    def __init__(self):
        self.still = True
        self.stilltime = 0
        self.vector = (0,0)

    def tick(self,elapsed):
        """Call periodically."""
        rel = pygame.mouse.get_rel()
        if rel == (0,0):
            self.stilltime += elapsed
            if not self.still and self.stilltime > pause_threshhold:
                print 'moved by:',self.vector
                self.still = True
                self.vector = (0,0)
        else:
            self.vector = tuple(map(sum,zip(self.vector,rel))) # addition hack
            self.still = False
            self.stilltime = 0
