#!/bin/python

from __future__ import print_function

import os
import sys

#
# Complete the timeConversion function below.
#
def timeConversion(s):
    #
    # Write your code here.
    #
    print(type(s))
if __name__ == '__main__':
    f = open(os.environ['OUTPUT_PATH'], 'w')

    s = raw_input()

    result = timeConversion(s)

    f.write(result + '\n')

    f.close()