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
import math

pause_threshold = 100  # ms of no motion for the mouse to be 'stopped'

class Move:
    """Represents one continuous movement of the mouse"""
    def __init__(self):
        self.x,self.y = (0,0)
        self.movetime = 0   # time mouse spent making this Move
        self.stilltime = 0  # time mouse was still before this Move

    def __iadd__(self,v):
        (x,y) = v
        self.x += x
        self.y += y
        return self

    def set_movetime(self,t):
        self.movetime = t

    def set_stilltime(self,t):
        self.stilltime = t

    def length(self):
        return math.sqrt(self.x*self.x+self.y*self.y)

    def angle(self,other):
        dot = self.x*other.x + self.y*other.y
        return dot/(self.length()*other.length())

    def __str__(self):
        ststr =  str(self.stilltime) + ' msec still, then ' 
        vstr = '('+str(self.x)+','+str(self.y)+')'
        mstr = ' in ' + str(self.movetime) + ' msec.' 
        return ststr + vstr + mstr

class MouseTrack:
    """Process mouse motion into discrete vectors separated by pauses"""
    def __init__(self):
        self.still = True
        self.stilltime = 0
        self.movetime = 0
        self.path = []

    def tick(self,elapsed):
        """Call periodically."""
        rel = pygame.mouse.get_rel()
        if self.still:
            if rel == (0,0):
                # haven't moved
                self.stilltime += elapsed
            else:
                # no longer still
                self.still = False
                self.current = Move()
                self.current.set_stilltime(self.stilltime)
                self.movetime = 0

        if not self.still:
            self.movetime += elapsed
            if rel == (0,0):
                # didn't move this tick
                self.stilltime += elapsed
                if self.stilltime > pause_threshold:
                    self.still = True
                    self.current.set_movetime(self.movetime - self.stilltime)
                    print 'moved by:',self.current
                    self.path.append(self.current)
                    analyze(self.path)
            else:
                # moved more
                self.stilltime = 0
                self.current += rel

class Recognizer:
    def __init__(self,name,target):
        self.dists,self.angles = target
        self.name = name
        assert(len(self.name) == len(self.dists)+1)

        print self.name,' created with ', len(self.dists), 'dists and', len(self.angles), 'angles.'

    def fit(self,path):
        d,a = path
        assert(len(d)==len(self.dists) and len(a)==len(self.angles))
        ssd = 0
        for i in range(len(d)):
            ssd += (d[i]-self.dists[i])**2
        ssa = 0
        for i in range(len(a)):
            ssa += (a[i]-self.angles[i])**2

        fit = math.log(ssd)+2*math.log(ssa)
        return fit < 10

    def __len__(self):
        """Return the number of moves (before polarization) needed to
        match this target, which is one less than the number of letters
        in the word."""
        return len(self.dists)

merlin = Recognizer('Merlin',([8093.606427298031, 2771.4871459200385, 7608.589948209852, 3496.6878613911194, 9112.136631987034], [0.06259612066161092, -0.3820833812868658, -0.9095979177385292, 0.8472026210790714]))

houdini = Recognizer('Houdini',([6630.671836247063, 4979.341422316811, 4653.158067377467, 5948.995629515961, 7189.5479691007, 8080.3948542134995], [-0.9493428417617078, -0.8602213269097301, -0.9136929390456537, -0.9359798057071793, -0.9998822190220981]))

people = [merlin,houdini]

def polarize(moves):
    """Take a list of Moves and return two lists, the first of distances,
    the second of angles."""
    dists = []
    for m in moves:
        dists.append(m.length())
    angles = []
    for i in range(len(moves)-1):
        angles.append(moves[i].angle(moves[i+1]))
    
    return (dists,angles)

def analyze(moves):
    for person in people:
        if len(moves) >= len(person):
            p = polarize(moves[-len(person):])
            if person.fit(p):
                print person.name

def learn(moves,name):
    """Replace analyze with this to print the moves for defining Recognizers"""
    if len(moves) == len(name)-1:
        print polarize(moves)
