class Vehicle:
    def __init__(self, color, manuf):
        self.color = color
        self.manuf = manuf
        self.gas = 4 # Atank full of gas

    def drive(self):
        if self.gas > 0:
            self.gas -= 1
            print ('The {} {} goes VROOM!!'.format(self.color, self.manuf))
        else:
            print ('The {} {} sputters out of cags'.format(self.color, self.manuf))


class Car(Vehicle):
    def radio(self):
        print "Blues Clues !! Jamma Jams"

    def window(self):
        print "Letting the cool air in"import Vehicle

class Motorcycle(Vehicle):
    # Put on helmet
    def helmet(self):
        print ("Helmet on ...Nice and Safe")

    def remove_helmet(self):
        print ("Helmet off ...Watch Out!!")
