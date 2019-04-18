from datetime import date
from datetime import time
from datetime import datetime

def main():
    tozday = date.today()
    today = datetime.now()
    print ("Todays date is : ", tozday)
    print ("Date components: ", tozday.day, tozday.month, tozday.year)
    print ("SYstem date", today)
if __name__ == "__main__":
    main()