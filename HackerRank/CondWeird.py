
import math
import os
import random
import re
import sys

def check_is_weird(N):
    if (N%2==0):
        if (N>=2 and N<=5):
            print("Not Weird")
        elif (N>=6 and N<=20):
            print("Weird")
        elif (N > 20):
            print("Not Weird")
        elif (N<1 or N>100):
            print()
    else:
        print("Weird")


if __name__ == '__main__':
    N = int(raw_input())
    check_is_weird(N)