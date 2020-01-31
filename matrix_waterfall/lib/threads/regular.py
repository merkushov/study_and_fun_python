import random
import curses
import time
import traceback
import logging
import json

class RegularThread():
    
    head_speed_min   = 0.1
    head_speed_max   = 0.5

    tail_speed_min  = 0.005
    tail_speed_max  = 0.03

    length_min  = 7
    length_max  = 45

    def __init__(self, **kwargs):
        self.color = kwargs['color']

        self.content = []
        self.content.append( { 'char': self.generate_random_sign(), 'color': self.color } );

        self.display_pos = 0

        self.screen_rows = int(kwargs['screen_rows'])
        self.screen_cols = int(kwargs['screen_cols'])

        self.length = random.randrange(
            RegularThread.length_min,
            RegularThread.length_max
        )

        self.tail_speed = random.uniform(
            RegularThread.tail_speed_min,
            RegularThread.tail_speed_max
        )

        # супер скоростной тред
        speed_tail_rundom = random.randrange(100)
        if speed_tail_rundom >= 97:
            self.tail_speed *= 1000
        elif speed_tail_rundom > 94:
            self.tail_speed *= 100
        elif speed_tail_rundom > 90:
            self.tail_speed *= 10

        self.head_speed = random.uniform(
            RegularThread.head_speed_min,
            RegularThread.head_speed_max
        )

        # супер скоростное раскрытие треда
        speed_head_rundom = random.randrange(100)
        if speed_head_rundom >= 97:
            self.tail_speed *= 1000
        elif speed_head_rundom > 94:
            self.tail_speed *= 100
        elif speed_head_rundom > 90:
            self.tail_speed *= 10

        self.timeframe = float(kwargs['timeframe'])
        self.time_of_head_previous_step = float( time.time() )
        self.time_of_tail_previous_step = float( time.time() )


    def generate_random_sign(self):
        return random.choice( list( map( chr, range(97, 123) ) ) )

    def is_complited(self):
        # logging.debug( "display_pos: %s screen_rows %s", self.display_pos, self.screen_rows )
        if self.display_pos > self.screen_rows:
            return True

        return False

    def make_step(self):

        now = float( time.time() )
        # time_diff = now - self.time_of_previous_step
        # logging.debug("diff: {0} tail_speed: {1} timeframe: {2}".format(time_diff, self.tail_speed, self.timeframe) )
        # logging.debug("tail_timeframe: {0}".format( time_diff * self.tail_speed ))

        if (now - self.time_of_head_previous_step) * self.head_speed > self.timeframe:
            self.time_of_head_previous_step = now

            # с ускорением
            if random.randrange(100) > 90:
                self.tail_speed = self.tail_speed * 2

            if len(self.content) < self.length:
                self.content[-1]['color'] = self.color
                self.content.append( { 'char':self.generate_random_sign(), 'color': self.color } )

        elif self.length != len(self.content):
           self.content[-1] = { 'char':self.generate_random_sign(), 'color': self.color | curses.A_BOLD }

        if (now - self.time_of_tail_previous_step) * self.tail_speed > self.timeframe:
            self.time_of_tail_previous_step = now

            self.display_pos = int(self.display_pos) + 1