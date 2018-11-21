## @file health.py
#  Source file for health object
#
#  Project: Galaga Clone
#  Author: Py Five
#  Created: 10/24/18

from .. import setup, constants, actor
from .player import Player


## @class Health
#  @brief Implements Actor base class as Health object
class Health(actor.Actor):

    ## Constructor
    #  @param image, surface object with Health image
    #  @param player, Player object that will be linked with health
    def __init__(self, player):
        actor.Actor.__init__(self, setup.IMAGES['hearts_3'])
        self.player = player
        self.rect.left = constants.SCREENRECT.left
        self.rect.bottom = constants.SCREENRECT.bottom

    def increase(self):
        if self.player.health < 3:
            self.player.health += 1

    def decrease(self):
        if self.player.health > 0:
            self.player.health -= 1

    def update(self):
        if self.player.health <= 0:
            self.image = setup.IMAGES['hearts_0']
        elif self.player.health == 1:
            self.image = setup.IMAGES['hearts_1']
        elif self.player.health == 2:
            self.image = setup.IMAGES['hearts_2']
        elif self.player.health >= 3:
            self.image = setup.IMAGES['hearts_3']
