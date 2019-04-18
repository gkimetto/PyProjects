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


