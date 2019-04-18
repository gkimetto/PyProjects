"""This is the lotto app main page"""
class Lotto():
    def __init__(self, game= "MassCash"):
        self.game = game
        if (self.game) is "Powerball":
            pb = Lotto("Powerball")
        elif (self.game) is "MegaMillions":
            mg = Lotto("MegaMillions")
        elif(self.game is "MassCash"):
            mc = Lotto("MassCash")
        else:
            raise ("Unknown Game try either Powerball, MegaMillions or MassCash")
    
    def menu():
        while(1):
            print ("-"*50)
            print("\t\tWelcome to the LOTTO App. ")
            print ("-"*50)
            print ("0.) Enter winning LOTTO numbers.")
            print ("1.) Generate lucky numbers.")
            print ("2.) Enter Selected Unlucky numbers.")
            print ("3.) Generate multiple lucky ticket numbers.")
            print ("4.) Check if winner in Multiple numbers.")
            print ("5.) Quit.")
            choice = input("\tMake a Selection 0 - 5. [5 to Quit ] ")
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

# if __name__=="__main__":
#     main()