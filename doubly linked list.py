class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None 
        self.tail = None
        self.size = 0

    def append(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

        self.size += 1

    def prepend(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

        self.size += 1

    def insert_at(self, index, data):
        if index < 0 or index > self.size:
            raise IndexError("Индекс вне диапазона")

        if index == 0:
            self.prepend(data)
            return
        if index == self.size:
            self.append(data)
            return
        if index <= self.size // 2:
            current = self.head
            for _ in range(index):
                current = current.next
        else:
            current = self.tail
            for _ in range(self.size - index - 1):
                current = current.prev

        new_node = Node(data)
        new_node.prev = current.prev
        new_node.next = current
        current.prev.next = new_node
        current.prev = new_node
        self.size += 1

        def remove_first(self):
            if self.head is None:
                return None

            removed_data = self.head.data

            if self.head == self.tail:

                self.head = None
                self.tail = None
            else:
                self.head = self.head.next
                self.head.prev = None

            self.size -= 1
            return removed_data

        def remove_last(self):
            if self.tail is None:
                return None

            removed_data = self.tail.data

            if self.head == self.tail:
                self.head = None
                self.tail = None
            else:
                self.tail = self.tail.prev
                self.tail.next = None

            self.size -= 1
            return removed_data

        def remove_by_value(self, value):
            current = self.head

            while current:
                if current.data == value:


                    if current.prev:

                        current.prev.next = current.next
                    else:
                        self.head = current.next

                    if current.next:

                        current.next.prev = current.prev
                    else:

                        self.tail = current.prev

                    self.size -= 1
                    return True

                current = current.next

            return False

        def remove_at(self, index):
            if index < 0 or index >= self.size:
                raise IndexError("Индекс вне диапазона")

            if index <= self.size // 2:
                current = self.head
                for _ in range(index):
                    current = current.next
            else:
                current = self.tail
                for _ in range(self.size - index - 1):
                    current = current.prev

            if current.prev:
                current.prev.next = current.next
            else:
                self.head = current.next

            if current.next:
                current.next.prev = current.prev
            else:
                self.tail = current.prev

            self.size -= 1
            return current.data
    def print_list(self):
        current = self.head
        while current.next:
            print(current.data,end=", ")
            current = current.next
        print(current.data,end="\n")
dl = DoublyLinkedList()
dl.append(1)
dl.append(2)
dl.append(3)
dl.prepend(4)
dl.insert_at(2, 15)
dl.print_list()

