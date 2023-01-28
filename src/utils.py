class ListNode:
    class HEAD:
        def __str__(self):
            return "<Doubly LinkedList HEAD>"

    prev: 'ListNode'
    next: 'ListNode'

    def __init__(self, data=None):
        self.data = data
        self.prev = self
        self.next = self

    def print(self):
        print(self.data)
        if not isinstance(self.next.data, self.HEAD):
            self.next.print()


class DLinkedList:
    '''
    A Doubly Linked List
    | -------------------------------------|
    + HEAD <=> data <=> data <= ...=> data +

    In this list, index 0 always is HEAD.

    '''

    head: 'ListNode' = ListNode(ListNode.HEAD())
    len: int = 0

    def __getitem__(self, index):
        r = self.head
        for _ in range(index):
            if isinstance(r.next.data, ListNode.HEAD) is True:
                raise IndexError
            r = r.next
        return r.data

    def __len__(self):
        return self.len

    @property
    def is_empty(self):
        return self.len == 0

    def insert(self, data, index: int = len):
        '''
        Insert data before index.
        (Put data at index)

                           data
        data (index-1)                 data (index)
                           
        data (index-1)  data (index)   data (index+1)


        '''
        if index > self.len+1 or -1*index > self.len+1:
            raise IndexError(f"Index{index} out of range{self.len}")

        if index < 0:
            index += self.len

        newNode = ListNode(data)
        if self.is_empty:
            newNode.next = self.head
            newNode.prev = self.head
            self.head.next = newNode
            self.head.prev = newNode

        else:
            target = self.head
            if index != 0:
                for _ in range(index):
                    target = target.next

            newNode.prev = target.prev

            target.prev = newNode
            newNode.next = target

            newNode.prev.next = newNode

        self.len += 1

    def append(self, data):
        '''
        Insert data **BEFORE** HEAD.
        Equals insert(data,0)
        '''
        self.insert(data, 0)

    def delete(self, index: int):
        if index > self.len or -1*index > self.len:
            raise IndexError(f"Index({index}) out of range({self.len})")

        if index < 0:
            index += self.len

        target = self.head.next
        for _ in range(index-1):
            target = target.next

        target.prev.next = target.next
        target.next.prev = target.prev
        self.len -= 1

    def print(self):
        if self.is_empty:
            return None
        else:
            self.head.print()


def test_DLinkedList():
    ll = DLinkedList()
    ll.append('a')
    ll.append('b')
    ll.append('c')
    ll.append('d')
    ll.append('e')
    ll.insert('b or 2? SB', 2)

    for i in ll:
        print(i)

    print(ll[7])


test_DLinkedList()
