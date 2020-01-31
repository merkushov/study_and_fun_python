from .regular import RegularThread

import random
import curses
import time
import traceback
import logging
import json

class BrokenThread(RegularThread):

    # length_min  = 40
    # length_max  = 80

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)

    def is_complited(self):
        if ( self.display_pos + random.randrange( len(self.content) ) ) > self.screen_rows:
            return True

        return False

    def generate_random_sign(self):
        return random.choice( list( map( chr, range(32, 63) ) ) )