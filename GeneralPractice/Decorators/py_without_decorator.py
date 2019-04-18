'''
Created on Aug 1, 2018
/home/gkimetto/gk-sandbox/PYTHON/src/py_decorator.py

@author: gkimetto
'''


def decor(func):
    def wrap():
        print ("#"*40)
        func()
        print ("#"*40)
    return wrap

def print_text():
    print("This sentence needs to be decorated !!")

decorated = decor(print_text)
decorated()