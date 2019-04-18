#!/bin/python

import math
import os
import random
import re
import sys

# Complete the solve function below.
def solve(meal_cost, tip_percent, tax_percent):
    tip=float(float(meal_cost)*float(tip_percent)/100)
    print(tip)
    tax=float(float(meal_cost)*float(tax_percent)/100)
    print(tax)
    print(meal_cost)
    total_cost=round(meal_cost+tip+tax)
    print(total_cost)

def main():
    meal_cost = float(raw_input())
    tip_percent = int(raw_input())
    tax_percent = int(raw_input())
    solve(meal_cost, tip_percent, tax_percent)


if __name__ == '__main__':
    main()