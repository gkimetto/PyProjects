"""This project will generate a lucky set of numbers. 
    [(x,y,z) for x in range(1,30) for y in range(x,30) for z in range(y,30) if x**2 + y**2 == z**2]

"""

import random


class TicGenerator():
    def __init__(self):
        self.num1 = 0
        self.num2 = 0
        
    def pick_six_random(self):
        
        [(ball1,ball2,ball3,ball4,ball5,mgc_ball) for ball1 in range(1,60) for ball2 in range(1,60) \
         for ball3 in range(1,60) for ball4 in range(1,60) for ball5 in range(1,60)  \
          for mgc_ball in range(1,60)if x**2 + y**2 == z**2]
    