# import matrix.matrix
from lib.matrix import Matrix

import traceback
import logging

if __name__ == "__main__":

    # logging.basicConfig(filename='log.txt',level=logging.DEBUG)
    logging.basicConfig(filename='matrix_waterfall.log',level=logging.INFO)

    matrix = Matrix()

    try:
        matrix.run()
    except Exception as e:
        matrix.finish()
        traceback.print_exc()
    except KeyboardInterrupt:
        matrix.finish()

    # with Matrix() as matrix:
    #     matrix.run()