import queue


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 0


class AVLTree:
    def __init__(self):
        self.root = None

    # BFS
    def find(self, value):
        q = queue.Queue()
        q.put(self.root)
        while q.qsize() > 0:
            node = q.get()
            if node.value == value:
                return node
            for child in [node.left, node.right]:
                if child:
                    q.put(child)
        raise ValueError(f"There is no node with value={value}.")

    def insert(self, value):
        if not self.root:
            self.root = Node(value)
            return

        self.root = self._add_leaf(self.root, value)

    def delete(self, value):
        deleted_node, self.root = self._find_and_delete_node(self.root, value)
        return deleted_node

    def _add_leaf(self, node, value):
        if value < node.value:
            if node.left:
                node.left = self._add_leaf(node.left, value)
            else:
                node.left = Node(value)
        elif value > node.value:
            if node.right:
                node.right = self._add_leaf(node.right, value)
            else:
                node.right = Node(value)
        elif value == node.value:
            raise ValueError(f"Node with value={value} already exists.")
        node.height = self._get_node_height(node)
        return self._balance_tree(node)

    def _find_and_delete_node(self, node, value):
        found_node = None
        if value < node.value and node.left:
            if node.left.value == value:
                found_node = node.left
                node.left = self._get_new_subtree(node.left)
                if node.left:
                    node.left.height = self._get_node_height(node.left)
            else:
                found_node, node.left = self._find_and_delete_node(node.left, value)
        elif value > node.value and node.right:
            if node.right.value == value:
                found_node = node.right
                node.right = self._get_new_subtree(node.right)
                if node.right:
                    node.right.height = self._get_node_height(node.right)
            else:
                found_node, node.right = self._find_and_delete_node(node.right, value)
        elif value == node.value:
            found_node = node
            node = self._get_new_subtree(node)
        else:
            return None, node
        node.height = self._get_node_height(node)
        return found_node, self._balance_tree(node)

    def _get_new_subtree(self, node):
        if node.right:
            new_subtree_root = self._find_min_subtree_node(node.right)
            if node.right != new_subtree_root:
                new_subtree_root.right = node.right
        elif node.left:
            new_subtree_root = self._find_min_subtree_node(node.left)
        else:
            return None
        if node.left != new_subtree_root:
            new_subtree_root.left = node.left
        return new_subtree_root

    def _find_min_subtree_node(self, subtree):
        min_subtree_node = subtree
        if subtree.left:
            if subtree.left.left or subtree.left.right:
                return self._find_min_subtree_node(subtree.left)
            min_subtree_node = subtree.left
            subtree.left = None
        elif subtree.right:
            if subtree.right.left or subtree.right.right:
                return self._find_min_subtree_node(subtree.right)
            min_subtree_node = subtree.right
            subtree.right = None
        return min_subtree_node

    def _balance_tree(self, node):
        balance_factor = self._get_balance_factor(node)
        if balance_factor == 2 or balance_factor == -2:
            return self._balance_subtree(node)
        return node

    def _balance_subtree(self, subtree):
        subtree_to_balance = subtree
        if not subtree_to_balance.left:
            right_subtree = subtree_to_balance.right
            if right_subtree.left:
                if not right_subtree.right or right_subtree.right.height < right_subtree.left.height:
                    subtree_to_balance.right = self._balance_right_left_shape(right_subtree)
            return self._balance_right_right_shape(subtree_to_balance)

        if not subtree_to_balance.right:
            left_subtree = subtree_to_balance.left
            if left_subtree.right:
                if not left_subtree.left or left_subtree.left.height < left_subtree.right.height:
                    subtree_to_balance.left = self._balance_left_right_shape(left_subtree)
            return self._balance_left_left_shape(subtree_to_balance)

        if subtree_to_balance.left.height > subtree_to_balance.right.height:
            left_subtree = subtree_to_balance.left
            if left_subtree.right:
                if not left_subtree.left or left_subtree.left.height < left_subtree.right.height:
                    subtree_to_balance.left = self._balance_left_right_shape(left_subtree)
            return self._balance_left_left_shape(subtree_to_balance)
        else:
            right_subtree = subtree_to_balance.right
            if right_subtree.left:
                if not right_subtree.right or right_subtree.right.height < right_subtree.left.height:
                    subtree_to_balance.right = self._balance_right_left_shape(right_subtree)
            return self._balance_right_right_shape(subtree_to_balance)

    def _balance_left_right_shape(self, node):
        new_subtree_root = node.right
        node.right = node.right.left
        new_subtree_root.left = node
        new_subtree_root.left.height = self._get_node_height(new_subtree_root.left)
        new_subtree_root.height = self._get_node_height(new_subtree_root)
        return new_subtree_root

    def _balance_left_left_shape(self, node):
        new_subtree_root = node.left
        node.left = node.left.right
        new_subtree_root.right = node
        new_subtree_root.right.height = self._get_node_height(new_subtree_root.right)
        new_subtree_root.height = self._get_node_height(new_subtree_root)
        return new_subtree_root

    def _balance_right_left_shape(self, node):
        new_subtree_root = node.left
        node.left = node.left.right
        new_subtree_root.right = node
        new_subtree_root.right.height = self._get_node_height(new_subtree_root.right)
        new_subtree_root.height = self._get_node_height(new_subtree_root)
        return new_subtree_root

    def _balance_right_right_shape(self, node):
        new_subtree_root = node.right
        node.right = node.right.left
        new_subtree_root.left = node
        new_subtree_root.left.height = self._get_node_height(new_subtree_root.left)
        new_subtree_root.height = self._get_node_height(new_subtree_root)
        return new_subtree_root

    @staticmethod
    def _get_balance_factor(node):
        if node.left and node.right:
            return node.left.height - node.right.height
        elif node.left:
            return abs(node.left.height) + 1
        elif node.right:
            return -abs(node.right.height) - 1

    @staticmethod
    def _get_node_height(node):
        if node.left and node.right:
            if node.left.height > node.right.height:
                return node.left.height + 1
            else:
                return node.right.height + 1
        elif node.left:
            return node.left.height + 1
        elif node.right:
            return node.right.height + 1
        else:
            return 0


binary_tree = AVLTree()
binary_tree.insert(10)
binary_tree.insert(25)
binary_tree.insert(50)
binary_tree.insert(100)
binary_tree.insert(40)
binary_tree.insert(5)
binary_tree.insert(15)
binary_tree.insert(1)
binary_tree.insert(30)
binary_tree.insert(45)
binary_tree.insert(60)
binary_tree.insert(120)

deleted_node = binary_tree.delete(25)
print(f"Node with value={deleted_node.value} has been deleted.")

found_node = binary_tree.find(60)
print(f"Node with value={found_node.value} has been found.")

# binary_tree.insert(10)
# binary_tree.insert(25)
# binary_tree.insert(50)
# binary_tree.insert(100)
# binary_tree.insert(150)
# binary_tree.insert(175)
# binary_tree.insert(190)

# binary_tree.insert(-2)
# binary_tree.insert(-7)
# binary_tree.insert(5)
# binary_tree.insert(-14)
# binary_tree.insert(-8)
# binary_tree.insert(-1)
# binary_tree.insert(10)

# binary_tree.insert(7)
# binary_tree.insert(3)
# binary_tree.insert(11)
# binary_tree.insert(9)
# binary_tree.insert(10)
# binary_tree.insert(8)

# binary_tree.insert(5)
# binary_tree.insert(2)
# binary_tree.insert(8)
# binary_tree.insert(3)
# binary_tree.insert(1)
# binary_tree.insert(9)

# binary_tree.insert(2)
# binary_tree.insert(1)
# binary_tree.insert(3)
# binary_tree.insert(0)
# binary_tree.insert(4)
# binary_tree.insert(5)

# binary_tree.insert(0)
# binary_tree.insert(1)
# binary_tree.insert(2)
# binary_tree.insert(3)
# binary_tree.insert(4)
# binary_tree.insert(5)
