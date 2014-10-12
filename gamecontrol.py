"""
gamecontrol

Handles the spirit data, decides how to respond to detected mouse motions.

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
import sound
from tracking import Recognizer

class Game:
    def __init__(self,datafile):
        """Reset game state and load data from datafile."""
        self.played = []
        self.got5 = False
        self.playedHoudini = False

        self.people = []
        self.readpeople(datafile)

    def detected(self,who):
        """Called when a mouse sequence is detected.
           who is the Recognizer for that sequence."""
        print 'Going to play: '+who.name
        if who.name not in self.played:
            self.played.append(who.name)
            print 'Playing part 1.'
            sound.player.play(who.name + '.ogg')
        else:
            print 'Playing part 2.'
            sound.player.play(who.name + '2.ogg')
        
        if not self.got5 and len(self.played) == 5:
            print 'Got all five.  Wait a sec...'
            self.got5 = True
            # trigger an event 90 seconds later
            pygame.time.set_timer(pygame.USEREVENT,90000)

    def winEvent(self):
        """Called when the pygame.USEREVENT is triggered."""
        if not self.playedHoudini:
            self.playedHoudini = True
            sound.player.play('Houdini.ogg')
            
    def readpeople(self,file):
        """
        File format:
           Line 1: Integer number of records in file
          For each record, three lines.
           R1: Name
           R2: Fit threshhold float.  Lower requires closer fit.
           R3: Pair () of lists [,] which give distances and angles.
               Copy this from training output.
        """
        f = open(file)
        numpeople = int(f.readline())
        print numpeople,'people'
        for p in range(numpeople):
            name = f.readline().strip()
            thresh = float(f.readline())
            data = eval(f.readline())
            print 'Creating recognizer for',name
            self.people.append(Recognizer(name,thresh,data))
        f.close()

"""
Sample file format:
1
HOUDINI
5.0
([6630.671836247063, 4979.341422316811, 4653.158067377467, 5948.995629515961, 7189.5479691007, 8080.3948542134995], [-0.9493428417617078, -0.8602213269097301, -0.9136929390456537, -0.9359798057071793, -0.9998822190220981])
"""
