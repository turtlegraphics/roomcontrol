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
        self.timeleft = time

        pygame.font.init()
        self.font = pygame.font.Font(None, 64)  # 64 point
        self.render()

    def render(self):
        """Build the text image of the current time"""
        self.image = self.font.render(str(self.timeleft),True,pygame.Color('white'))

    def tick(self,timepassed):
        """Decrease current time by timepassed (ms) and rebuild image.
           Return True if no time is left."""
        self.timeleft -= float(timepassed)/1000.0
        self.render()
        return self.timeleft < 0

    def draw(self,surf):
        surf.blit(self.image,(0,0))
