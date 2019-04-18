#!/usr/bin/env /usr/bin/python3

def main():
    print("test")
    for i in inclusive_range(1,3,25):
        print(i, end =' ')
    print()

def  inclusive_range(*args):
    num_args = len(args)
    start = 0
    step = 1
    if num_args <1:
        raise TypeError(f'Expected at least 1 argument got {num_args}')
    elif num_args == 1:
        stop = args[0]
    elif num_args ==2:
        start = args[0]
        stop = args[1] 
    elif num_args ==3:
        start = args[0]
        stop = args[2]
        step = args[1]
    else:
        raise TypeError (f'Expected 3 args got {num_args}')

    # generator
    i = start 
    while i <= stop:
        yield i
        i+=step       
if __name__ == "__main__":
    main()