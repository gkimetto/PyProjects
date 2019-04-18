"""
    Take a list, say for example this one:
    
    a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    and write a program that prints out all the elements of the list that are less than 5.
    
    Extras:
    
    Instead of printing the elements one by one, make a new list that has all the elements 
    less than 5 from this list in it and print out this new list.
    Write this in one line of Python.
    Ask the user for a number and return a list that contains only elements from the original
    list a that are smaller than that number given by the user.
"""
class ListAllLessThanTen():
    def __init__(self):
        self.array = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    def get_user_input(self):
        inpt_num = input("Enter the number to check in the array : ")
        print(f"You have entered {inpt_num}. Checking for elements less than this...")
        return inpt_num
        
    # Get the number from the user to check for in the list say x
    def get_elements_less_than_x(self):
        x = int(self.get_user_input())
        # Make a new list of all the elements that are less than x
        smaller_lst = []
        for i in self.array:
            if i < x:
                smaller_lst.append(i)
        # Print all the elements of the list that are less than x 
        print(f"The following items are smaller than {x} : ")
        print(smaller_lst)
    # Extra do this in one line? List comprehension?
    def single_line_lc_elmnts_lt_x(self):
        samp = int(self.get_user_input())
        smallr_lst = [x for x in self.array if x < samp]
        print(smallr_lst)