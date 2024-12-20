from lista_enlazada import LinkedList

class BTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = LinkedList()
        self.child = LinkedList()

class BTree:
    def __init__(self, t):
        self.root = BTreeNode(True)
        self.t = t

    def insert(self, k):
        root = self.root
        if self.root.keys.size() == (2 * self.t) - 1:
            temp = BTreeNode(False)  # New root is not a leaf
            self.root = temp
            temp.child.add(root)
            self.split_child(temp, 0)
            self.insert_non_full(temp, k)
        else:
            self.insert_non_full(root, k)

    def insert_non_full(self, x, k):
        i = x.keys.size() - 1
        
        if x.leaf:
            # Insert key in sorted order
            while i >= 0 and k[0] < x.keys.get(i)[0]:
                i -= 1
            x.keys.add(k)
            self._sort_keys(x.keys)
        else:
            # Find appropriate child
            while i >= 0 and k[0] < x.keys.get(i)[0]:
                i -= 1
            i += 1
            
            # Split child if full
            if x.child.get(i).keys.size() == (2 * self.t) - 1:
                self.split_child(x, i)
                if k[0] > x.keys.get(i)[0]:
                    i += 1
            self.insert_non_full(x.child.get(i), k)

    def _sort_keys(self, keys):
        # Bubble sort implementation for LinkedList
        n = keys.size()
        for i in range(n):
            for j in range(0, n-i-1):
                if keys.get(j)[0] > keys.get(j+1)[0]:
                    temp = keys.get(j)
                    keys.remove(j)
                    keys.add(temp)

    def split_child(self, x, i):
        t = self.t
        y = x.child.get(i)
        z = BTreeNode(y.leaf)
        
        # Move median key to parent
        median = y.keys.get(t-1)
        x.keys.add(median)
        self._sort_keys(x.keys)
        
        # Copy keys to z (right half)
        for j in range(t, (2*t)-1):
            z.keys.add(y.keys.get(j))
        
        # Remove keys from y (left half keeps t-1 keys)
        for j in range((2*t)-2, t-2, -1):
            y.keys.remove(j)
        
        if not y.leaf:
            # Move children if not a leaf
            for j in range(t, 2*t):
                z.child.add(y.child.get(j))
            for j in range(2*t-1, t-1, -1):
                y.child.remove(j)
        
        # Insert z as child of x
        x.child.add(z)
        self._sort_children(x, x.keys.size())

    def _sort_children(self, x, n):
        # Bubble sort for children based on their first key
        for i in range(n):
            for j in range(0, n-i-1):
                if x.child.get(j).keys.get(0)[0] > x.child.get(j+1).keys.get(0)[0]:
                    temp = x.child.get(j)
                    x.child.remove(j)
                    x.child.add(temp)

    def print_tree(self, x, l=0):
        print(f"Level {l}, Keys: ", end="")
        for i in range(x.keys.size()):
            key = x.keys.get(i)
            print(f"({key[0]}, {key[1]})", end=" ")
        print()
        
        if not x.leaf:
            for i in range(x.child.size()):
                self.print_tree(x.child.get(i), l + 1)

def main():
    B = BTree(3)
    values = [
        (1, "uno"),
        (3, "tres"),
        (7, "siete"),
        (10, "diez"),
        (11, "once"),
        (13, "trece"),
        (14, "catorce"),
        (15, "quince"),
        (4, "cuatro"),
        (5, "cinco")
    ]

    for value in values:
        print(f"\nInsertando: {value}")
        B.insert(value)
        print("\nÁrbol actual:")
        B.print_tree(B.root)
        print("-" * 50)

if __name__ == "__main__":
    main()