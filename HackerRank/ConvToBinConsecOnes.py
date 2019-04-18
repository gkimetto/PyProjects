
import math
import os
import random
import re
import sys


def convert_to_bin(n):
    bin_num=[]
    while n >0:
        remainder=n%2
        num=n//2
        bin_num.append(remainder)
        n=num
    return bin_num
    
def count_coseq_ones(lst_bins):
    print(lst_bins)
    count=0
    max_count=0
    prev_num=0
    for num in lst_bins:
        if num==1 and prev_num==0:
            prev_num=num
            count+=1
        elif num==1 and prev_num==1:
            prev_num=num
            count+=1
        elif num==0:
            if count > max_count:
                max_count=count
                prev_num=num
                count=0
            else:
                prev_num=num
                count=0
    if count > max_count:
        return count
    else:
        return max_count
    
if __name__ == '__main__':
    n = int(raw_input())
    lst_bins=convert_to_bin(n)
    count=count_coseq_ones(lst_bins)
    print(count)