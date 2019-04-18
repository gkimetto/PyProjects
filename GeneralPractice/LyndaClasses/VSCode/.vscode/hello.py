# Say hello
from datetime import date, time, datetime
class myClass():
    def methos1(self):
        print "My class method 1"

    def method2(self):
        print "My class method 2"
#print ("Hello world")

def main():
    c = myClass()
    c.method2()
    c.methos1()

    today = date.today()
    print "Todays date is ", today
    # Print date compoinents
    print ("Date components ", today.day , today.month, today.year)
    #Print weekday number
    wkday = today.weekday()
    print "Print weekday number is ", today.wkday()

if __name__== "__main__":
    main()