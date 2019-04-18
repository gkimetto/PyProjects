'''

Exercise 2:
Ask the user for a number. Depending on whether the number is even or odd, 
print out an appropriate message to the user. Hint: how does an 
even / odd number react differently when divided by 2?

Extras:

If the number is a multiple of 4, print out a different message.
Ask the user for two numbers: one number to check (call it num) and one 
number to divide by (check). If check divides evenly into num, 
tell that to the user. If not, print a different appropriate message.

'''


def get_number():
     input_number=int(input("Enter a number to check : "))

     return input_number


def check_odd_or_even(int_number):
    str_number=str(int_number)
    if int_number%2==0:
        print "The number {} is an even number ".format(str_number)
    else:
        print "The number {} is an odd number ".format(str_number)


def extra_if_multiple_of_four(int_number):
    int_number =int(int_number)
    if (int_number%4 == 0):
        #int_number=str(int_number)
        print "The number {} is a multiple of 4. ".format(int_number)
    else:
        print "The number {} is NOT a multiple of 4.".format(int_number)


def get_two_numbers():
    num =int(input("Please enter the first number :" ))
    check = int(input("Please enter the second number :"))
    if num%check ==0:
        num= str(num)
        check= str(check)
        print "The number {} is a multiple of {}".format(num, check)
    else:
        num = str(num)
        check = str(check)
        print "The number {} is NOT a multiple of {}".format(num,check)


def main():
    while(1):

        print "Welcome to ODD or EVEN checker: "
        print "-"*50
        print "0.) Enter a number to Test."
        print "1.) Check if number is ODD or EVEN."
        print "2.) Check if it's a multiple of 4. "
        print "3.) Enter 2 numbers."
        print "4.) Quit."
        choice = input("Make a Selection 0 - 4. [4 to Quit ]")
        if choice == 0:
            int_number=get_number()
        elif choice == 1:
            int_number = get_number()
            check_odd_or_even(int_number)
        elif choice ==2:
            int_number = get_number()
            extra_if_multiple_of_four(int_number)
        elif choice ==3:
            get_two_numbers()
        else:
            exit()

if __name__=="__main__":
    main()