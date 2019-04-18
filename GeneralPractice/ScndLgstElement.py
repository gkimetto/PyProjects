# -*- coding: utf-8 -*-
"""
    Given an array A of size N, print second largest element from an array.
     
    Input:
    The first line of input contains an integer T denoting the number of test cases. T testcases follow.
     Each testcase contains two lines of input. The first line contains an integer N
      denoting the size of the array. The second line contains the N space seperated intgers 
      of the array
     
    Output:
    For each testcase, in a new line, print the second largest element.
     
    Constraints:
    1 ≤ T ≤ 50
    1 ≤ N ≤ 500
    1 ≤ Ai ≤ 1200
     
    Example:
    Input
    2
    5
    89 24 75 11 23
    6
    56 42 21 23 65 20
    Output
    75
    56
     
    ** For More Input/Output Examples Use 'Expected Output' option **
"""
import sys
#Verify that the array input is greater than 1
def check_array_sz_gt_1(in_array):
    arr_len = len(in_array)
    if(arr_len == 1):
        sys.exit()
    elif (arr_len > 1):
        return True
    else: 
        return False    
#Get the user input of an array
def get_user_input():
    in_array = []
    in_array = raw_input()
    in_array = list(map(int, in_array.split()))
    return in_array

def find_scnd_largest_element(tst_lst):
    srt_lst = sorted(tst_lst)
    sec_large = srt_lst[-2]
       
        
    return sec_large        
    
def get_second_largest_element():
    tst_array = []
    tst_array = get_user_input()
    if check_array_sz_gt_1(tst_array) is True:
        sec_lgst_elem = find_scnd_largest_element(tst_array)
        print(sec_lgst_elem)
    else:
        print(tst_array[0])
        
if __name__ == "__main__":
    get_second_largest_element()
