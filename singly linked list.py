print("Hello World")

class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next

class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0
    def append(self, data:Node):
        if self.head is None:
            self.head = Node(data)

        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = Node(data)
        self.size+=1
    def getSize(self):
        return self.size
    def printList(self):
        current = self.head
        while current.next is not None:
            print(current.data,end=", ")
            current = current.next
        print(current.data,end="\n")
    def getOnIndex(self, index:int):

        current = self.head
        if index < 0 or index >= self.size:
            print("Index out of range")
            return None
        else:
            for i in range(index):
                current = current.next
            return current.data
    def inputOnIndex(self,data:Node, index:int):
        new_node = Node(data)
        current = self.head
        if index < 0 or index >= self.size:
            print("Index out of range")
            return None
        else:
            for i in range(index-1):
                current = current.next
            new_node.next = current.next
            current.next = new_node
            self.size += 1
    def deleteNode(self, index:int):
        current = self.head
        if index < 0 or index >= self.size:
            print("Index out of range")
            return None
        else:
            for i in range(index-1):
                current = current.next
            print(current.data)
            current.next = current.next.next
            self.size -= 1
    def appendToEnd(self,data):
        current = self.head
        while current.next is not None:
            current = current.next
        current.next = Node(data,None)
        



        
l=LinkedList()
l.append(1)
l.append(2)
l.appendToEnd(3)
l.append(4)
l.inputOnIndex(7, 2)
l.deleteNode(2)
# print(l.getSize())
l.printList()
# print(l.getOnIndex(6))

