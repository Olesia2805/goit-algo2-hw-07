from functools import lru_cache
from timeit import timeit
import matplotlib


class Node:
    def __init__(self, data, parent=None):
        self.data = data
        self.parent = parent
        self.left_node = None
        self.right_node = None


class SplayTree:
    def __init__(self):
        self.root = None

    def insert(self, data):
        """Inssert the new element into the tree."""

        if self.find(data) is not None:
            return

        if self.root is None:
            self.root = Node(data)
        else:
            self._insert_node(data, self.root)

    def _insert_node(self, data, current_node):
        """Recursive insertion of an element into the tree."""
        if data < current_node.data:
            if current_node.left_node:
                self._insert_node(data, current_node.left_node)
            else:
                current_node.left_node = Node(data, current_node)
        else:
            if current_node.right_node:
                self._insert_node(data, current_node.right_node)
            else:
                current_node.right_node = Node(data, current_node)

    def find(self, data):
        """Search for an element in the tree using splay."""
        node = self.root
        while node is not None:
            if data < node.data:
                node = node.left_node
            elif data > node.data:
                node = node.right_node
            else:
                self._splay(node)
                return node.data
        return None  # If the element is not found

    def _splay(self, node):
        """Realizations of splaying to move the node to the root."""
        while node.parent is not None:
            if node.parent.parent is None:  # Zig-case
                if node == node.parent.left_node:
                    self._rotate_right(node.parent)
                else:
                    self._rotate_left(node.parent)
            elif (
                node == node.parent.left_node
                and node.parent == node.parent.parent.left_node
            ):  # Zig-Zig
                self._rotate_right(node.parent.parent)
                self._rotate_right(node.parent)
            elif (
                node == node.parent.right_node
                and node.parent == node.parent.parent.right_node
            ):  # Zig-Zig
                self._rotate_left(node.parent.parent)
                self._rotate_left(node.parent)
            else:  # Zig-Zag
                if node == node.parent.left_node:
                    self._rotate_right(node.parent)
                    self._rotate_left(node.parent)
                else:
                    self._rotate_left(node.parent)
                    self._rotate_right(node.parent)

    def _rotate_right(self, node):
        """Right rotation of the node."""
        left_child = node.left_node
        if left_child is None:
            return

        node.left_node = left_child.right_node
        if left_child.right_node:
            left_child.right_node.parent = node

        left_child.parent = node.parent
        if node.parent is None:
            self.root = left_child
        elif node == node.parent.left_node:
            node.parent.left_node = left_child
        else:
            node.parent.right_node = left_child

        left_child.right_node = node
        node.parent = left_child

    def _rotate_left(self, node):
        """Left rotation of the node."""
        right_child = node.right_node
        if right_child is None:
            return

        node.right_node = right_child.left_node
        if right_child.left_node:
            right_child.left_node.parent = node

        right_child.parent = node.parent
        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left_node:
            node.parent.left_node = right_child
        else:
            node.parent.right_node = right_child

        right_child.left_node = node
        node.parent = right_child


def fibonacci_splay(n, tree):
    if n < 2:
        return n
    if tree.find(n) is not None:
        return tree.find(n)
    else:
        result = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
        tree.insert(n)
        return result


@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)


if __name__ == "__main__":
    tree = SplayTree()

    print(f"|{'n':^15}|" f"{'LRU Cache Time (s)':^30}|{'Splay Tree Time (s)':^30}|")
    print("-" * 80)
    for times in range(0, 950 + 1, 50):
        lru_time = round(timeit(lambda: fibonacci_lru(times)), 10)
        splay_time = round(timeit(lambda: fibonacci_splay(times, tree)), 10)
        print(f"|{times:^15}|{lru_time:^30}|{splay_time:^30}|")
