# -*- coding: utf-8 -*-
# *args is used to send a non-keyworded variable length argument list to the function.
# Here’s an example to help you get a clear idea:
# 
# def test_var_args(f_arg, *argv):
#     print "first normal arg:", f_arg
#     for arg in argv:
#         print "another arg through *argv :", arg
# 
# test_var_args('yasoob','python','eggs','test')


def print_args(first_arg, *args):
        print("The first mandatory arg is :%s",first_arg)
        for my_arg in args:
            print ("This is additional argument %s", my_arg)
            
def main():
    print_args("hello", "hello2", "hello3", "hello4")
    print_kwargs(firstname="Foo",lastname="Bar" )

def print_kwargs(first_kwarg= "Name: ", **kwargs):
    
    print("*~*"*50)
    print ("\t\t\t KWARGS EXAMPLE: %s", first_kwarg)
    print("*~*"*50)
    for key, value  in kwargs.iteritems():
        print(key, value)

if __name__=="__main__":
    main()