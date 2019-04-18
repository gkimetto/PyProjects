"""" Author : Gilbert Kimetto
     Purpose: Recursion a program that calls itself 
     
     - Make sure the recursive functions have a breaking condition
       A break would prevents inifinite loops and crashes
     - Each time the function is called old arguments are saved.
     - This is called a stack
     """
     
def countdown(x):
    if x ==0:
        print("Done!!")
        return
    else:
        print("x = ", x)
        countdown(x-1)
        print("foo", x)
countdown(4)