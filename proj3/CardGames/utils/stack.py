import random

#This is the abstraction for a stack that will be used to define properties of a deck and a pile
class Stack():

    #initializes the stack
    def __init__(self):
        self.stack = []

    #places an element on the stack
    def push(self, item):
        self.stack.append(item)

    def size(self):
        return len(self.stack)

    #removes an element from the stack
    def pop(self):
        return self.stack.pop()

    #returns the first element on the stack
    def peekFirst(self):
        if self.size() >= 1:
            return self.stack[-1]

    #returns the second element on the stack
    def peekSecond(self):
        if self.size() >= 2:
            return self.stack[-2]

    #returns the third element on the stack
    def peekThird(self):
        if self.size() >= 3:
            return self.stack[-3]

    #shuffles the stack
    def shuffle(self):
        random.shuffle(self.stack)
