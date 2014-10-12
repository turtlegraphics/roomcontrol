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

# Used for color terminal output
class bcolors:
    BLACK = '\033[90m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    ENDC = '\033[0m'

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

class MouseTrack:
    """Process mouse motion into discrete vectors separated by pauses.
    people is a list of Recognizers.  If learning is a string, print
    mouse track data when that many letters have appeared."""
    def __init__(self,people,learning = None):
        self.still = True
        self.stilltime = 0
        self.movetime = 0
        self.path = []
        self.people = people
        self.learning = learning

    def analyze(self):
        """Check current path for match against defined people."""
        detected = None
        for person in self.people:
            if len(self.path) >= len(person):
                p = polarize(self.path[-len(person):])
                if person.fit(p):
                    detected = person
        print
        if detected:
            print '\nDETECTED: ' + detected.name.upper()
            self.path = []
        return detected

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
                    if self.current.length() > 100:
                        # only pay attention to real moves, not twitches
                        # print 'moved by:',self.current
                        self.path.append(self.current)
                        if self.learning:
                            if len(self.path) >= len(self.learning)-1:
                                print polarize(self.path[-(len(self.learning)-1):])
                            return None
                        else:
                            return self.analyze()
            else:
                # moved more
                self.stilltime = 0
                self.current += rel

class Recognizer:
    def __init__(self,name,threshold,target):
        self.dists,self.angles = target
        self.name = name
        self.threshold = threshold
        assert(len(self.name) == len(self.dists)+1)

        print self.name,' created with ', len(self.dists), 'dists and', len(self.angles), 'angles.'

    def displayfit(self,fit):
        colorvalues = [bcolors.GREEN, bcolors.BLUE, bcolors.RED, bcolors.BLACK]
        debugstr = '%8s %2.1f' % (self.name,fit)
        print colorvalues[max(0,min(len(colorvalues)-1,int(fit/5)))] + debugstr + bcolors.ENDC,

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
        self.displayfit(fit)
        return fit < self.threshold

    def __len__(self):
        """Return the number of moves (before polarization) needed to
        match this target, which is one less than the number of letters
        in the word."""
        return len(self.dists)

