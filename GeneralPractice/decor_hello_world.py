
def decor(func):
    def wrap():
        print "="*30
        func()
        print "="*30
    return wrap

#def print_text():
#    print "Wrapper with Wild Decorator"


# def main():

#print_text = decor(print_text)
#print_text()

# if __name__=="__main__":
#     main()

@decor
def print_text_with_decor():
    print "Hello World with Decorators"
    numbers = list(range(10))
    print(numbers)
print_text_with_decor()
