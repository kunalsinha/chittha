'''
class Node:
    def __init__(self, data=None, nextNode=None, prevNode=None):
        self.data = data
        self.next = nextNode
        self.prev = prevNode
'''

class DLList:

    def __init__(self):
        self.head = None

    def add(self, node):
        if not self.head:
            self.head = node
            self.head.next = self.head
            self.head.prev = self.head
        else:
            t = self.head
            while t.next != self.head:
                t = t.next
            t.next = node
            node.next = self.head
            node.prev = t
            self.head.prev = node

    def remove(self, node):
        if self.head:
            # only one element
            if node == self.head and self.head.next == self.head:
                self.head = None
            else:
                t = self.head
                count = 0
                while t != node:
                    if t == self.head:
                        count += 1
                        if count > 1:
                            print('Node not found')
                            break
                    t = t.next
                t.prev.next = t.next
                t.next.prev = t.prev
                if node == self.head:
                    self.head = t.next
        else:
            print('Node not found')

    # generator to return all the nodes in the list
    def all(self):
        if self.head:
            t = self.head
            count = 0 
            while True:
                if t == self.head:
                    count += 1
                    if count > 1:
                        break
                yield t
                t = t.next

    def length(self):
        if self.head:
            t = self.head.next
            length = 1
            while t != self.head:
                length += 1
                t = t.next
            return length
        else:
            return 0

