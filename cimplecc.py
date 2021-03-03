#!/usr/bin/env python3
import sys
import os


def main(filename):
    print(filename[:-2])


if __name__ == '__main__':

    # # No arguments passed
    # if len(sys.argv) == 1:
    #     sys.exit(1)
    #
    # # File does not exist
    # if not os.path.exists(sys.argv[1]):
    #
    #     sys.exit(1)

    # Call main function
    main(sys.argv[1])
