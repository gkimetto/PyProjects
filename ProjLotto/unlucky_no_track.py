"""This project will generate a lucky set of numbers. 
    [(x,y,z) for x in range(1,30) for y in range(x,30) for z in range(y,30) if x**2 + y**2 == z**2]

"""

import random


class UnluckyNoTracker():
    def __init__(self):
        self.num1 = 0
        self.num2 = 0
        
    def pick_six_random(self):
        
        [(a,b,c,d,e,f,g) for a in range(1,60) for y in range(1,60) for z in range(1,60) if x**2 + y**2 == z**2]
    