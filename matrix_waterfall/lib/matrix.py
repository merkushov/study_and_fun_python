from .threads.regular import RegularThread
from .threads.broken import BrokenThread

import random
import curses
import time
import traceback
import logging
import json

class Matrix():

    steps_per_second = 24
    column_num = 3

    """The main class responsible for calculating and displaying the matrix"""

    def __init__(self):

        random.seed()
        
        self.curses_stdscr = curses.initscr()
        self.curses_stdscr.keypad(1)

        curses.start_color()
        curses.cbreak()
        curses.noecho()
        curses.curs_set(0)

        """Initialize default color-pairs."""
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(8, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(9, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(10, curses.COLOR_GREEN, curses.COLOR_BLACK)


    def run(self):

        screen_rows, screen_cols = self.curses_stdscr.getmaxyx()
        logging.info("screen_rows: {0} screen_cols: {1}".format(screen_rows, screen_cols))

        # columns = []
        columns = [ [] for i in range(screen_cols) ]

        while True:
            
            logging.debug("===================== calculate ========================")
            self.calculate(
                columns,
                # columns_num = Matrix.column_num
                screen_rows = screen_rows,
                screen_cols = screen_cols
            )

            logging.debug("===================== visualize ========================")
            self.visualize(
                columns,
                # columns_num = Matrix.column_num,
                screen_rows = screen_rows,
                screen_cols = screen_cols
            )

            # time.sleep( 1 / Matrix.steps_per_second )

            # assert False, "My error!!!"

    def calculate(self, columns, **kwargs):

        counter = 0
        for column in columns:

            if 'columns_num' in kwargs and kwargs['columns_num'] and counter > kwargs['columns_num'] - 1:
                break

            counter += 1

            # добавить новую нить в столбец
            if len(column) == 0:
                num = int( random.randrange(100) )
                if num > 98:
                    column.append(
                        BrokenThread(
                            timeframe = 1 / Matrix.steps_per_second,
                            screen_rows = kwargs['screen_rows'],
                            screen_cols = kwargs['screen_cols'],
                            # color = curses.color_pair( random.choice([2,6,8,9,10]) ),
                            color = curses.color_pair( 9 ),
                        )
                    )
                elif num > 80:
                    column.append(
                        RegularThread(
                            timeframe = 1 / Matrix.steps_per_second,
                            screen_rows = kwargs['screen_rows'],
                            screen_cols = kwargs['screen_cols'],
                            # color = curses.color_pair( random.choice([2,6,8,9,10]) ),
                            color = curses.color_pair( 10 ),
                        )
                    )
            else:

                # цикл по всем тредам
                for i in range(0,len(column)):
                    thread = column[i]
                    if thread.is_complited() is True:
                        # logging.debug(" == del {0} display_pos: {1} vs {2}".format(i, thread.display_pos, thread.screen_rows))
                        del column[i]
                    else:
                        thread.make_step()
                        # logging.debug(" == make_step pos: {0}\n".format(thread.display_pos))

        return True

    def visualize(self, columns, **kwargs):

        color = curses.COLOR_RED | curses.A_BOLD

        self.curses_stdscr.erase()

        for x in range(0,len(columns)):

            if 'columns_num' in kwargs and kwargs['columns_num'] and x > kwargs['columns_num'] - 1:
                break

            logging.debug( "i: {0} threads: {1}".format(x, len(columns[x])) )

            for thread in columns[x]:
                logging.debug( json.dumps(thread.__dict__) )
                for y in range(0,len(thread.content)):
                # for y in range(0,thread.display_pos):
                    if x < kwargs['screen_cols'] - 1 and y + thread.display_pos < kwargs['screen_rows']:
                        # logging.debug("draw x:{0} y:{1} sign:{2}".format(x, y + thread.display_pos, thread.content[y]['char']) )
                        try:
                            self.curses_stdscr.addstr(
                                y + thread.display_pos,
                                x,
                                thread.content[y]['char'],
                                thread.content[y]['color'],
                            )
                        except Exception as e:
                            logging.error( "Exception x: {0} y: {1} sign: {2}".format(x, y + thread.display_pos, thread.content[y]['char']))
                            logging.error( json.dumps( thread.__dict__ ) )
                            logging.error( traceback.format_exc() )

                            screen_rows, screen_cols = self.curses_stdscr.getmaxyx()
                            logging.error("screen_rows: {0} screen_cols: {1}".format(screen_rows, screen_cols))
                    

        self.curses_stdscr.refresh()

    def finish(self):

        """Safely finish app."""
        """End curses mode."""
        if self.curses_stdscr:
            self.curses_stdscr.clear()
            self.curses_stdscr.refresh()
            curses.curs_set(1)
            curses.endwin()
            self.curses_stdscr = None

        return True

    # def __enter__ (self):
    #     return self

    # def __exit__(self, exc_type, exc_val, exc_tb):
    #     self.finish()
    #     # pprint.pprint(exc_type.__name__)

    #     if exc_type is None:
    #         return True
    #     elif exc_type.__name__ is 'KeyboardInterrupt':
    #         print("++++++")
    #         return True

    #     print("===no====")

    #     return False

    # def __del__(self):
    #     self.finish()