#!/bin/python

import math
import os
import random
import re
import sys

# Complete the miniMaxSum function below.
def miniMaxSum(arr):
    minArr=sorted(arr)
    minArr.pop()
    
    maxArr= sorted(arr)
    maxArr.reverse()
    maxArr.pop()
    print(sum(minArr), sum(maxArr))

if __name__ == '__main__':
    arr = map(int, raw_input().rstrip().split())

    miniMaxSum(arr)