"""Author : Gilbert Kimetto
   Purpose: Example of a stack in python.
   
   """

   

# TODO: create a hash table all at once
items1 = {"key1":1, "keys2":2, "key3":3, "keys4": "four"}
print(items1)
# TODO: Create a hashtable progressively
items2 = {}
items2["key1"] = 1
items2["key2"] = 2
items2["key3"] = 3
print(items2)


# TODO: Try to access a non-existent key

# print(items1["keys6"]) # Error 

# TODO: replace an item
items1["key1"]="one"
print("items1", items1)
# TODO: iterate the keys and values in the dictionary

for key, value in items2.items():
    print("Key :", key, "Value :",value)