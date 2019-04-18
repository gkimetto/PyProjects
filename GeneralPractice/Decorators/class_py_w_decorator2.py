'''
Created on Aug 1, 2018
/home/gkimetto/gk-sandbox/PYTHON/src/py_w_decorator.py

@author: gkimetto
'''


    
class DecorMe():
    def __init__(self):
        self.test2 =" GOOOD MORNING!! "
    def decor(self, funct):

        def wrap(self, *args, **kwargs):
    
            print ("#"*40)
            print("")
            print(test)
            print(test2)
            print("-"*len(test))
            return_val=funct(self, *args, **kwargs)
            print(__name__)
            print ("#"*40)
        return return_val
    
    def print_test(self):
        self.test="MYYYYYYYYYY"
        __name__= "hello world"
        print(__name__)
        print ("I have been decorated!!!!")

dm =DecorMe()
decorated=dm.decor(dm.print_test)
decorated()
