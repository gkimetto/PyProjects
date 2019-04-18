# Exceptions
"""
Handling Exceptions Household problems. 
"""


class ElectricalError(Exception):
    def __init__(self, device, problem):
        self.device = device
        self.problem = problem
    def __str__(self):
        return "The {} is {}!! Needs your attention!".format(self.device, self.problem)


class PlumbingError(Exception):
    def __init__(self, device, problem):
        self.device = device
        self.problem = problem

    def __str__(self):
        return "The {} is {}!! Needs your attention!".format(self.device, self.problem)

class GenericError(Exception):
    def __init__(self, device, problem):
        self.device = device
        self.problem = problem

    def __str__(self):
        return "The {} is {}!! Needs your attention!".format(self.device, self.problem)

def cause_error(error_type):
    if error_type == 'electrical':
        raise ElectricalError('circuit_breaker', 'overloaded circuit')
    elif error_type == 'plumbing':
        raise PlumbingError('dishwasher', 'spraying water all over')
    else:
        raise GenericError('other_device','Generic error check house')
try:
    cause_error('asdhaksjdhsa')
except ElectricalError as e:
    print (e)
    print ('Fix it myself')
except PlumbingError as e:
    print (e)
    print ('Calling a plumber')
except GenericError as e:
    print (e)
    print ("Call the landlord.")


# try:
#     cause_error('plumbing')
# except ElectricalError as e:
#         print (e)
#         print ('Fix it myself')
# except PlumbingError as e:
#         print (e)
#         print ('Calling a plumber')