import argparse

from btc.poker import Poker

parser = argparse.ArgumentParser(description='The Psychic Poker Player')
parser.add_argument('--run', type=str, nargs='+',
                    help='Run the poker program for only one line')
parser.add_argument('--file', type=str, default='input.txt',
                    help='Name of the file with the input')

args = parser.parse_args()

if __name__ == '__main__':
    poker = Poker()

    if args.run:
        lines = [args.run]
    else:
        with open(args.file, 'r') as fp:
            lines = fp.readlines()

    for line in lines:
        print(poker.play(line))
