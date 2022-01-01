import os, sys
import time
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from squishy import *

if __name__ == '__main__':
    start = time.time()
    squishy = Squishy()
    squishy.compress('octopus.png')
    print('-' * 40)
    squishy.decompress('octopus.bin', 'octopus_new.png')
    stop = time.time()
    times = (stop - start) * 1000
    print('-' * 40)
    print('Run time takes %d miliseconds' % times)
    print('Images equal = %s' % images_equal('octopus.png', 'octopus_new.png'))