'''
Created on Aug 1, 2018
/home/gkimetto/gk-sandbox/PYTHON/src/hello.py

@author: gkimetto
'''



from datetime import datetime, timedelta
import time

class cached_property(object):
    """ A property that is only computed once per instance and then replaces
        itself with an ordinary attribute. Deleting the attribute resets the
        property.

        Source: https://github.com/bottlepy/bottle/commit/fa7733e075da0d790d809aa3d2f53071897e6f76
        """

    def __init__(self, func):
        print ("hello")
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
        """Represents a performance heavy property."""
        time.sleep(1)  # Wait a WHOLE second!
        return "I am slooooow"

def test_slow_class1():
    # Instantiate the slow class
    slow_class = SlowClass1()

    # Start the clock!
    start = datetime.now()

    # Call the property. This time it's really slow...
    assert slow_class.very_slow == "I am slooooow"

    # Check that it took at least a second to run
    assert timedelta(milliseconds=1000) >= start - datetime.now()

    # Call the property a second time. This time it runs fast.
    assert slow_class.very_slow == "I am slooooow"

    # Second time running, should take a TINY amount of time.
    # Should take just a microsecond, but we'll play a test for and test
    #   for a maximim of at least 100 milliseconds.
    assert timedelta(milliseconds=1100) > start - datetime.now()