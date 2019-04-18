# -*- coding: utf-8 -*-
"""
Exercise 6 (and Solution)
Ask the user for a string and print out whether this string is a palindrome or 
not. (A palindrome is a string that reads the same forwards and backwards.)

Discussion
Concepts for this week:

List indexing
Strings are lists
List indexing
In Python (and most programming in general), you start counting lists from the 
number 0. The first element in a list is “number 0”, the second is 
“number 1”, etc.

As a result, when you want to get single elements out of a list, you can ask 
a list for that number element:

  >>> a = [5, 10, 15, 20, 25]
  >>> a[3]
  20
  >>> a[0]
  5
There is also a convenient way to get sublists between two indices:

  >>> a = [5, 10, 15, 20, 25, 30, 35, 40]
  >>> a[1:4]
  [10, 15, 20]
  >>> a[6:]
  [35, 40]
  >>> a[:-1]
  [5, 10, 15, 20, 25, 30, 35]
The first number is the “start index” and the last number is the “end index.”

You can also include a third number in the indexing, to count how often you 
should read from the list:

  >>> a = [5, 10, 15, 20, 25, 30, 35, 40]
  >>> a[1:5:2]
  [10, 20]
  >>> a[3:0:-1]
  [15, 10, 5]
To read the whole list, just use the variable name (in the above examples, a), 
or you can also use [:] at the end of the variable name (in the above 
examples, a[:]).

"""

