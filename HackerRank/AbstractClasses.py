from abc import ABCMeta, abstractmethod
class Book:
    __metaclass__ = ABCMeta
    def __init__(self,title,author):
        self.title=title
        self.author=author   
    @abstractmethod
    def display(): pass

#Write MyBook class
class MyBook(Book):
    def __init__(self, title, author, price):
        self.title = title
        self.author = author
        self.price = price
    # Implements the Book class' abstract display() method so it prints these  lines:
    # Title a space, and then the current instance's .
    # Author a space, and then the current instance's .
    # Price a space, and then the current instance's .
    
    def display(self):
        print('Title: ',self.title)
        print('Author: ', self.author) 
        print('Price: ', self.price)     
title=raw_input()
author=raw_input()
price=int(raw_input())
new_novel=MyBook(title,author,price)
new_novel.display()