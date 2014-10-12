import pygame
import sound
from tracking import Recognizer

people = []
"""people.append(
    Recognizer('Houdini',5.0,
               ([6630.671836247063, 4979.341422316811, 4653.158067377467, 5948.995629515961, 7189.5479691007, 8080.3948542134995], [-0.9493428417617078, -0.8602213269097301, -0.9136929390456537, -0.9359798057071793, -0.9998822190220981]))
    )
"""
people.append(
    Recognizer('Midas', 6.0,
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

class Game:
    def __init__(self):
        self.played = []
        self.got5 = False
        self.playedHoudini = False

    def detected(self,who):
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
            pygame.time.set_timer(pygame.USEREVENT,90000)

    def winEvent(self):
        if not self.playedHoudini:
            self.playedHoudini = True
            sound.player.play('Houdini.ogg')
            
