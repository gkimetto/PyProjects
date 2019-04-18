"""Author : Gilbert Kimetto
   Purpose: Example for a linked list
   Date : Mar 5 2019  """

# the node class

class Node(object):
       
    def __init__(self, val):
        self.val = val
        self.next = None
        
    def get_data(self):
        return self.val
    
    def set_data(self, val):
        self.val = val
    
    def get_next(self):
        return self.next
    
    def set_next(self, next):
        self.next = next

class LinkedList(object):
    def __init__(self, head=None):
        self.head = head
        self.count = 0
        
    def get_count(self):
        return self.count
    def insert(self, data):
        # TODO Insert a new node
        new_node = Node(data)
        # adding new node to head
        new_node.set_next(self.head)
        self.head = new_node
        self.count +=1
        
    def find(self, val):
        #TODO : Find the first item with a given value
        item = self.head
        while (item != None):
            if (item.get_data()) == val:
                return item
            else:
                item = item.get_next()
        return None
    def deleteAt(self, idx):
        # TODO delete an item at given index
        if idx > self.count-1:
            return
        if idx == 0:
            self.head = self.head.get_next()
        else:
            tempIdx = 0
            node = self.head
            while(tempIdx < idx -1):
                node = node.get_next()
                tempIdx +=1
            node.set_next(node.get_next().get_next())
            self.count-=1
            
    def dump_list(self):
        tempnode = self.head
        while (tempnode!= None):
            print("Node: ", tempnode.get_data())
            tempnode = tempnode.get_next()
# Create a linked list and insert some items
itemsList = LinkedList()
itemsList.insert(38)
itemsList.insert(49)
itemsList.insert(13)
itemsList.insert(15)
itemsList.dump_list()

# Exercise the list
print(" Excercise the list :")
print("Item count ", itemsList.get_count())
print("Finding item : ", itemsList.find(13))
print("Finding item: ", itemsList.find(78))


# Delete an item
print("Delete an item : 3")
itemsList.deleteAt(3)
print("Item count : ", itemsList.get_count())
print("Finding item :", itemsList.find(38))
itemsList.dump_list()
