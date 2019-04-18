

class Monopoly(object):
    def __init__(self):
        self.property_cost = 500

    @property
    def day_rental(self):
        self.property_cost += 50
        return self.property_cost

