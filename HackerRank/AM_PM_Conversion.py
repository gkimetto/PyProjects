
from __future__ import print_function

import os
import sys

#
# Complete the timeConversion function below.
#
def timeConversion(s):
    #
    # Write your code here.
    # Get AM or PM string
    am_pm_str=s[-1:-2]
    am_pm_str=list(am_pm_str)
    am_pm_str.reverse()
    am_pm_str.strip()
    if "AM" in am_pm_str.upper():
        s_mil_time=s[:-3]
        print(s_mil_time)
    elif "PM" in am_pm_str.upper():
        s_mil_time=s[:-3]
        # Convert hour
        hour_to_mil=int(s[0:3])
        suff=s[3:]
        hour_to_mil+=12
        result=str("%s%s"%(hour_to_mil,suff))
        print(result)




if __name__ == '__main__':
#     f = open(os.environ['OUTPUT_PATH'], 'w')

    s = raw_input()

    result = timeConversion(s)

#     f.write(result + '\n')
# 
#     f.close()

