## @file health.py
#  Source file for health object
#
#  Project: Gallaga Clone
#  Author: Py Five
#  Created: 10/24/19

from actor import Actor
import constants as const

## @class Health
#  @brief Implements Actor base class as Health object
class Health(Actor):

    ## Constructor
    #  @param image, surface object with Health image
    #  @param player, Player object that will be linked with health
    def __init__(self, image, player):
        Actor.__init__(self, image)
        self.rect.left = const.SCREENRECT.left
        self.rect.bottom = const.SCREENRECT.bottom
