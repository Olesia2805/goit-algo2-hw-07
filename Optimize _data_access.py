import random
from timeit import timeit


class Node:
    def __init__(self, key, value):
        self.data = (key, value)
        self.next = None
        self.prev = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def push(self, key, value):
        new_node = Node(key, value)
        new_node.next = self.head
        if self.head:
            self.head.prev = new_node
        else:
            self.tail = new_node
        self.head = new_node
        return new_node

    def remove(self, node):
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        node.prev = None
        node.next = None

    def move_to_front(self, node):
        if node != self.head:
            self.remove(node)
            node.next = self.head
            self.head.prev = node
            self.head = node

    def remove_last(self):
        if self.tail:
            last = self.tail
            self.remove(last)
            return last
        return None


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.list = DoublyLinkedList()

    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self.list.move_to_front(node)
            return node.data[1]
        return -1

    def put(self, key, value):
        if key in self.cache:
            node = self.cache[key]
            node.data = (key, value)
            self.list.move_to_front(node)
        else:
            if len(self.cache) >= self.capacity:
                last = self.list.remove_last()
                if last:
                    del self.cache[last.data[0]]
            new_node = self.list.push(key, value)
            self.cache[key] = new_node

    def clear(self):
        self.cache.clear()


cache = LRUCache(1000)


def range_sum_no_cache(array, L, R):
    sum = 0
    for i in range(L, R + 1):
        sum += array[i]
    return sum


def update_no_cache(array, index, value):
    array[index] = value


def range_sum_with_cache(array, L, R):
    pass


def update_with_cache(array, index, value):
    array[index] = value
    range_sum_with_cache.cache_clear()


if __name__ == "__main__":

    array = [random.randint(1, 100) for _ in range(100000)]
    time_no_cache = round(
        timeit(lambda: range_sum_no_cache(array, 0, 99999), number=1000), 10
    )
    time_with_cache = round(
        timeit(lambda: range_sum_with_cache(array, 0, 99999), number=1000), 10
    )

    print(f"Time without cache: {time_no_cache:.2f} sec")
    print(f"Time with cache: {time_with_cache:.2f} sec")
