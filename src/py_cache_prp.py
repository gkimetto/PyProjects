'''
Created on Aug 1, 2018
/home/gkimetto/gk-sandbox/PYTHON/src/py_cache_prp.py

@author: gkimetto
'''
from datetime import datetime, timedelta
import time

from cached_property import cached_property

class SlowClass2(object):
    @cached_property
    def very_slow(self):
        """Simulate a very slow property"""
        time.sleep(20)
        return "I am slooow 2"
    
def test_slow_class2():
    slow_class2 = SlowClass2
    
    start_time = datetime.now()
    
    assert slow_class2.very_slow() == "I am slooow 2"
    assert timedelta(milliseconds=1000) >= start_time - datetime.now()
    
    
    
    assert slow_class2.very_slow() == "I am slooow 2"
    assert timedelta(milliseconds=1100) >= start_time - datetime.now()