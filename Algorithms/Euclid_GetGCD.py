"""
   Author: Gilbert Kimetto
   Purpose: Algorithm to calculate the Greatest Common Deominator of 2 numbers
   
"""
def get_user_input():
    num1 = input("Please enter the first number : ")
    num2 = input("Please enter the second number : ")
    return (num1, num2)

def calculate_GCD(num1, num2):
    """Using Euclid's Algorithm"""
    
    while(num2 != 0):
        temp= num2
        rem_num = num1%num2
        num1=num2
        num2=rem_num
    return temp
        
def main():
    # Get user input - get two numbers  
    
    input1, input2 = get_user_input()
    gcd_num= calculate_GCD(input1, input2)
    print("The greatest common divider for",input1, " and ",input2, " is ",gcd_num,"!") 
    print("TEST:: Calculate_GCD(60,96)",calculate_GCD(60,96))
    print("TEST:: Calculate_GCD(20, 8)",calculate_GCD(20, 8))
if __name__=="__main__":
    main()