class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None
        self.prev = None
        
        
class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0
    
    def add(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1
    
    def get(self, index):
        if index >= self._size:
            return None
        current = self.head
        for _ in range(index):
            current = current.next
        return current.data
    
    def remove(self, index):
        if index >= self._size:
            return
        current = self.head
        for _ in range(index):
            current = current.next
        
        if current.prev:
            current.prev.next = current.next
        else:
            self.head = current.next
            
        if current.next:
            current.next.prev = current.prev
        else:
            self.tail = current.prev
            
        self._size -= 1
    
    def size(self):
        return self._size