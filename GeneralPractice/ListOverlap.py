# -*- coding: utf-8 -*-
"""
Take two lists, say for example these two:

  a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
  b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
and write a program that returns a list that contains only the elements 
that are common between the lists (without duplicates). Make sure your 
program works on two lists of different sizes.

Extras:

Randomly generate two lists to test this
Write this in one line of Python (don’t worry if you can’t figure this 
out at this point we’ll get to it soon)
"""


def get_lists():
    a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    get_common_elements(a, b)


def get_common_elements(a,b):

    print "-"*50
    print "List A :: {} ".format(a)
    print "-"*50
    print "List B :: {} ".format(b)
    print "-" * 50

    print "\nGetting the common elements in the two lists :"
    len_a = len(a)

    c = []
    len_b = len(b)
    for i in len_a:
        for j in len_b:
            if a[i] == b[j]:
                c.append(a[i])


def main():
    get_lists()


if __name__ == "__main__":
    main()