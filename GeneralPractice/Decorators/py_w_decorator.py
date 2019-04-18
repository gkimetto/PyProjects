'''
Created on Aug 1, 2018
/home/gkimetto/gk-sandbox/PYTHON/src/py_w_decorator.py

@author: gkimetto
'''
test =" GOOOD MORNING!! "

def decor(funct):

    def wrap():

        print ("#"*40)
        print("")
        print(test)
        print("-"*len(test))
        funct()
        print(__name__)
        print ("#"*40)
    return wrap


@decor
def print_test():
    __name__= "hello world"
    print(__name__)
    print ("I have been decorated!!!!")

print_test()
