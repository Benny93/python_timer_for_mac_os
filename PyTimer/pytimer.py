import sys
import os
import time
import select
import signal
import constants


OKBLUE = '\033[36m'
GREEN = '\033[32m'
ENDC = '\033[0m'

def signal_handler(signal, frame):
    print('\nYou pressed Ctrl+C!\nExiting ...')
    sys.exit(0)


def getBlockStringListFromChar(c):
    return {
        ':': constants.LETTER_BLOCK_DOTS,
        '0': constants.LETTER_BLOCK_ZERO,
        '1': constants.LETTER_BLOCK_ONE,
        '2': constants.LETTER_BLOCK_TWO,
        '3': constants.LETTER_BLOCK_THREE,
        '4': constants.LETTER_BLOCK_FOUR,
        '5': constants.LETTER_BLOCK_FIVE,
        '6': constants.LETTER_BLOCK_SIX,
        '7': constants.LETTER_BLOCK_SEVEN,
        '8': constants.LETTER_BLOCK_EIGHT,
        '9': constants.LETTER_BLOCK_NINE,
    }[c]


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def printTimeAsLetterBlock(time):
    clear_terminal()
    #print '\n'*5
    print 'Time Remaining:\n\n'
    print GREEN +'/' * 80 + ENDC
    print '\n'
    result = ["" for x in range(constants.ROWS)]
    for c in time:
        result = [a + b for a, b in zip(result, getBlockStringListFromChar(c))]
    print OKBLUE + '\n'.join(result) + ENDC
    print '\n'
    print GREEN +'/' * 80 + ENDC


def start_timer(input_time):
    minutes_and_seconds = str(input_time).split(':')
    # TODO: catch errors
    seconds = int(minutes_and_seconds[1])
    seconds += int(minutes_and_seconds[0]) * 60
    for sec in range(seconds, 0, -1):
        sys.stdout.flush()
        minutes_remain = int(sec / 60)
        seconds_remain = int(sec - minutes_remain * 60)
        minutes_remain_str = '0{0}'.format(str(minutes_remain)) if minutes_remain < 10 else str(minutes_remain)
        seconds_remain_str = '0{0}'.format(str(seconds_remain)) if seconds_remain < 10 else str(seconds_remain)
        printTimeAsLetterBlock(minutes_remain_str + ":" + seconds_remain_str)
        time.sleep(1)
    printTimeAsLetterBlock('00:00')
    print "Timer done \n Press ENTER to exit."
    while True:
        os.system('afplay /System/Library/Sounds/Ping.aiff')
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            line = raw_input()
            break
        time.sleep(0.1)


def main(argv):
    if len(argv) != 2:
        print 'Invalid number of argments'
        sys.exit(1)
    input_time = argv[1]
    start_timer(input_time)


signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    main(sys.argv)
