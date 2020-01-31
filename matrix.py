import random
import curses
import time
import traceback
import logging
import json

class MatrixThread():
    
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
            MatrixThread.length_min,
            MatrixThread.length_max
        )

        self.tail_speed = random.uniform(
            MatrixThread.tail_speed_min,
            MatrixThread.tail_speed_max
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
            MatrixThread.head_speed_min,
            MatrixThread.head_speed_max
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
                logging.debug( "random: {0}".format(num) )
                if num > 80:
                    logging.debug( " === append" )
                    column.append(
                        MatrixThread(
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

if __name__ == "__main__":

    # logging.basicConfig(filename='log.txt',level=logging.DEBUG)
    logging.basicConfig(filename='log.txt',level=logging.INFO)
    # signal.signal(signal.SIGINT, interrupt_handler)

    # m = MatrixThread();
    # m.make_step()
    # m.make_step()
    # print( m.display_pos )

    matrix = Matrix()

    try:
        matrix.run()
    except Exception as e:
        matrix.finish()
        # print( "Exception: ", e )
        traceback.print_exc()
    except KeyboardInterrupt:
        matrix.finish()
        logging.info(" === KeyboardInterrupt")

    # with Matrix() as matrix:
    #     matrix.run()