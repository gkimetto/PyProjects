"""
   Author : Gilbert Kimetto
   Date: Mar 1 2019
   Purpose: Python Practice
   Create a program that asks the user for a number and then prints out a list of all 
   the divisors of that number. (If you don’t know what a divisor is, it is a number 
   that divides evenly into another number. For example, 13 is a divisor of 26 
   because 26 / 13 has no remainder.)

"""

class DivisorsCl():
    # Constructor to initialise class variables
    def __init__(self):
        self.input_num = 26
    # Get user input for number to get calculate divisors
    def get_user_input(self):
        self.input_num = int(input("Please enter a number to find Divisors : "))
        return self.input_num
    
    # Using number given calculate the divisor(s) save in a list
    def get_divisors_from_num(self):
        # Create a list to hold list of divisors
        divisors = []
        num = self.get_user_input()
        for i in range(1,num+1):
            if num%i == 0:
                divisors.append(i)
                
        print(f" The divisors for {num} are : \n {divisors}")        
        
