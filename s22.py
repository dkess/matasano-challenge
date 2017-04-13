from itertools import cycle, islice
import random
from sys import argv
import time

import util

WAIT_MIN = 40
WAIT_MAX = 1000

def roundrobin(*iterables):
    "roundrobin('ABC', 'D', 'EF') --> A D E B F C"
    # Recipe credited to George Sakkis
    pending = len(iterables)
    nexts = cycle(iter(it).__next__ for it in iterables)
    while pending:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            pending -= 1
            nexts = cycle(islice(nexts, pending))

if len(argv) > 1:
    fastmode = argv[1] == '--fast'
else:
    fastmode = False

current_time = int(time.time())
wait_time = random.randint(WAIT_MIN, WAIT_MAX)
if fastmode:
    current_time += wait_time
else:
    time.sleep(wait_time)
    current_time = int(time.time())

seed = current_time
gen = util.MT19937(seed)

wait_time = random.randint(WAIT_MIN, WAIT_MAX)
if fastmode:
    current_time += wait_time
else:
    time.sleep(wait_time)
    current_time = int(time.time())

output = gen.extract_number()

for guess in roundrobin(range(WAIT_MAX + WAIT_MIN, 2 * WAIT_MAX - 1),
                        range(WAIT_MAX + WAIT_MIN - 1, 2 * WAIT_MIN - 1, -1)):
    seedguess = current_time - guess
    genguess = util.MT19937(seedguess)
    if genguess.extract_number() == output:
        print('Guess seed is {}'.format(seedguess))
        if seedguess == seed:
            print('Guessed correctly')
        else:
            print('Guessed wrong :(')
        break
print('Actual seed was {}'.format(seed))
