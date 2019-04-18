

def foo(bar):
    return bar + 1

print (foo)
print (foo(2))
print (type(foo))

def call_foo_with_arg(foo, arg):
    return foo(arg)

print (call_foo_with_arg(foo, 3))

def parent():
    print ("Printing from the parent() function.")
    def first_child():
        return "Printing from the first child function."
    def second_child():
        return "Printing from the second child function."

    print (first_child())
    print (second_child())
