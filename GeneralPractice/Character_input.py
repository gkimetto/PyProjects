'''
Exercise 1 (and Solution)
Create a program that asks the user to enter their name and their age. 
Print out a message addressed to them that tells them the year that 
they will turn 100 years old.

Extras:

Add on to the previous program by asking the user for another number and
 printing out that many copies of the previous message. 
 
 (Hint: order of operations exists in Python)
Print out that many copies of the previous message on separate lines. 

(Hint: the string "\n is the same as pressing the ENTER button)
'''


def enter_name():
    user_name = raw_input("Please enter your name: ")

    return user_name


def enter_age():
    user_age = raw_input("Please enter your age: ")

    return user_age


def calculate_100yr_bday(age):
    hundred_bday = ((2018 - age)+ 100)
    hundred_bday = str(hundred_bday)
    print "Your 100 year Birthday will be in the year :" + hundred_bday


def repeat_string(age):
    repeat_count = raw_input("How many times would you like to repeat the last message ? ")
    repeat_count=int(repeat_count)
    for i in range(repeat_count):
        calculate_100yr_bday(age)


def main():
    your_name=enter_name()
    your_age=enter_age()
    print '-'*50
    print "You are : " + your_name
    print "And you are : " + your_age
    your_age= int(your_age)
    calculate_100yr_bday(your_age)
    print '-' * 50

    repeat_string(your_age)
    print '=' * 50
    print "Complete: [PASSED]"
    print '=' * 50

if __name__ == "__main__":
    main()


