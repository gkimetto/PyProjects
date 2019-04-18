from datetime import datetime, timedelta
import time

class cached_property(object):
    """A property that is only computed once per instance and then replaces 
       itself with an ordinary attribute. Deleting the attribute resets the 
       property."""
    def __init__(self, func):
        self.__doc__ = getattr(func, '__doc__')
        self.func = func
    
    def __get__(self, obj, cls):
        if obj is None:
            return self 
        value = obj.__dict__[self.func.__name__] = self.func(obj)
        return value
    
class SlowClass1(object):
    @cached_property
    def very_slow(self):
        """You can delay this function"""
        time.sleep(5)
        print ("IN Main Now")
        return "I am very slooooow"

def main():
    #Instantiate a slow_class
    slow_class = SlowClass1()
    # Start the clock
    start = datetime.now()
    time.sleep(5)
    #Call the property should be slow 40 secs plus
    assert slow_class.very_slow() == "I am very slooooow"
    
    # Calculate the time taken
    print ("Calculating the time taken : ")
    print (start - datetime.now())
    
    
    
    # Call the property again and this time the cached proprty is called
    # Its much faster
    assert slow_class.very_slow() == "I am very slooooow"
    
     # Calculate the time taken
    print ("Calculating the time taken :")
    print (start - datetime.now())
    
#     
# def main():
#     print ("IN Main Now")
#     test_slow_class1()
#     
    
if '__name__' == '__main__':
    main()
        
    
    