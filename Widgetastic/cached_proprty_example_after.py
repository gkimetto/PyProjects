# Add cached_property
# Also look at threaded_cached_property

from cached_property import cached_property

class Monopoly(object):
    def __init__(self):
        self.property_cost = 500

    @cached_property
    def day_rental(self):
        self.property_cost += 50
        return self.property_cost

