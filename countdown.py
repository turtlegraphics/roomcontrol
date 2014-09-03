#
# countdown.py
#
#   Handle display of the countdown timer
#
import pygame
import pygame.font
import pygame.color
class CountdownTimer:
    """Create a countdown timer on screen"""
    def __init__(self):
        pygame.font.init()
        self.font = pygame.font.Font(None, 64)  # 64 point

        self.timeleft = 1000
        self.render()

    def render(self):
        """Build the text image of the current time"""
        self.image = self.font.render(str(self.timeleft),True,pygame.Color('white'))

    def tick(self,timepassed):
        """Decrease current time by timepassed (ms) and rebuild image"""
        self.timeleft -= float(timepassed)/1000.0
        self.render()

    def draw(self,surf):
        surf.blit(self.image,(0,0))
