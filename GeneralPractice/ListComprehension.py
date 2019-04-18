

x = [i for i in range(10)]
print(x)

squares = []

squares = [i**2 for i in range(10)]
print(squares)


inlist = [lambda i:i%3==0 for i in range(5)]
print(inlist)

# a list comprehension
cubes = [i**3 for i in range(5)]

print(cubes)
# A list comprehension can also contain an if statement to enforce 
# a condition on values in the list.
# Example:

evens=[i**2 for i in range(10) if i**2 % 2 == 0]

print(evens)