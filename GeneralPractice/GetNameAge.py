"""Create a program that asks the user to enter their name and their age. 
Print out a message addressed to them that tells them the year that 
they will turn 100 years old.

Extras:

Add on to the previous program by asking the user for another number 
and printing out that many copies of the previous message. 
(Hint: order of operations exists in Python)

Print out that many copies of the previous message on separate lines. 
(Hint: the string "\n is the same as pressing the ENTER button)
"""
from datetime import datetime

class GetNameAge():
    def __init__(self):
        self.name = input("Please enter your name :")
        self.age = int(input("Please enter your age : "))
    
    def calc_100yrs(self):
        curr_year = int(datetime.now().strftime('%Y'))
        birth_year = curr_year - self.age
        print(f"You were born in {birth_year}")
        age100 = birth_year + 100
        print(f"{self.name}, you will turn 100 in the year {age100}")
        
        
     