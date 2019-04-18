import math
import os
import random
import re
import sys

def run(n):
    i =0
    while i <10:
        i+=1
        result=(n*i)
        print("%d x %d = %d"%(n,i,result))


if __name__ == '__main__':
    n = int(raw_input())
    run(n)
 