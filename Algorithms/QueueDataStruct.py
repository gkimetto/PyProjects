"""Author : Gilbert Kimetto
   Purpose: Example of a stack in python.
   
   """
from collections import deque
   
# Try out stack functions
# TODO: create a new empty queue
queue = deque()

# TODO: add items on the queue
queue.append(1)
queue.append(2)
queue.append(3)
queue.append(4)

# TODO: print out the queue contents
print(queue)
# TODO pop an item off front of the queue
x=queue.popleft()
print (x)
print(queue)