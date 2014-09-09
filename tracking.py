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

# Define to a non-empty string if you want output for creating Recognizers
learning = ''

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
                    if self.current.length() > 100:
                        # only pay attention to real moves, not twitches
                        # print 'moved by:',self.current
                        self.path.append(self.current)
                        if learning:
                            if len(self.path) >= len(learning)-1:
                                #print self.path[-(len(learning)-1):]
                                print polarize(self.path[-(len(learning)-1):])
                        else:
                            analyze(self.path)
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

people = []
"""
people.append(
    Recognizer('Merlin',12.0,
               ([8093.606427298031, 2771.4871459200385, 7608.589948209852, 3496.6878613911194, 9112.136631987034], [0.06259612066161092, -0.3820833812868658, -0.9095979177385292, 0.8472026210790714]))
    )
"""

people.append(
    Recognizer('Houdini',5.0,
               ([6630.671836247063, 4979.341422316811, 4653.158067377467, 5948.995629515961, 7189.5479691007, 8080.3948542134995], [-0.9493428417617078, -0.8602213269097301, -0.9136929390456537, -0.9359798057071793, -0.9998822190220981]))
    )

people.append(
    Recognizer('Midas', 4.0,
               ([3822.2977382720987, 4999.191234589851, 3725.0229529494177, 5331.870403526327], [0.9584049182859741, 0.9807076508765032, -0.9333008921042961]))
    )

people.append(
    Recognizer('Galileo',10.0,
               ([7255.6533820187415, 11233.458950830773, 3318.7780883933774, 3215.880750276664, 7795.025400856626, 4747.526724516672], [-0.9918365796488631, -0.9872788585054973, -0.9999813948537128, -0.9997602854163206, 0.6353019949677967]))
    )

people.append(
    Recognizer('Chanel',10.0,
               ([5290.053402376955, 7738.783496131676, 2557.6053252994293, 5581.160452809075, 7422.016504966828], [-0.9995827172115008, 0.2853657977028101, -0.7546515231404586, 0.7307258820994635]))
    )

people.append(
    Recognizer('Child',3.0,
               ([4883.018738444488, 882.9099614343469, 2758.840517318825, 8449.98769229873], [0.972970842178754, 0.9999816181104513, -0.9875822612813664]))
    )

people.append(
    Recognizer('Mozart',5.0,
               ([8009.136907307803, 12226.723395906198, 12435.491988658912, 3766.108468963686, 2556.6425248751534], [-0.9854573672613719, -0.997492314559631, -0.9998707184892288, 0.9692752551648487]))
    )

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
                print '\nDETECTED: '+person.name.upper(),
    print
