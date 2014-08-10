class OneZero:

    def __init__(self):
        self.one = None
        self.zero = None

    def __getitem__(self, key):
        assert key == "1" or key == "0"
        if key == "1":
            return self.one
        elif key == "0":
            return self.zero

    def __setitem__(self, key, value):
        assert key == "1" or key == "0"
        if key == "1":
            self.one = value
        elif key == "0":
            self.zero = value

    def empty(self):
        return self.zero is None and self.one is None

    def __repr__(self):
        return "<%s, %s>" % (self.zero, self.one)


class BitTree:

    def __init__(self):
        self._branch = OneZero()
        self._leaf = OneZero()

    def add(self, binary, value):
        branch = binary[0]
        binary = binary[1:]
        assert branch == "1" or branch == "0"
        if not binary:
            self._add_leaf(branch, value)
        else:
            self._add_branch(branch, binary, value)

    def _add_leaf(self, branch, value):
        if self._leaf[branch] is None:
            self._leaf[branch] = []
        self._leaf[branch].append(value)

    def _add_branch(self, branch, binary, value):
        if self._branch[branch] is None:
            self._branch[branch] = BitTree()
        self._branch[branch].add(binary, value)

    def lookup(self, binary):
        branch = binary[0]
        binary = binary[1:]
        result = self._lookup_leaf(branch)
        if not binary:
            return result + self._children(branch)
        # Continue recursive lookup
        return result + self._lookup_branch(branch, binary)

    def _lookup_leaf(self, branch):
        result = self._leaf[branch]
        if result is None:
            return []
        return result

    def _children(self, branch):
        if self._branch[branch] is not None:
            return self._branch[branch]._all_children()
        return []

    def _all_children(self):
        result = []
        if self._leaf.zero is not None:
            result.extend(self._leaf.zero)
        if self._leaf.one is not None:
            result.extend(self._leaf.one)
        if self._branch.zero is not None:
            result.extend(self._branch.zero._all_children())
        if self._branch.one is not None:
            result.extend(self._branch.one._all_children())
        return result

    def _lookup_branch(self, branch, binary):
        if self._branch[branch] is None:
            return []
        return self._branch[branch].lookup(binary)

    def delete(self, binary, value):
        branch = binary[0]
        binary = binary[1:]
        assert branch == "1" or branch == "0"
        if not binary:
            self._delete_leaf(branch, value)
        else:
            self._delete_branch(branch, binary, value)
        return self._empty()

    def _delete_leaf(self, branch, value):
        if self._leaf[branch] is None:
            return
        self._leaf[branch].remove(value)
        if not self._leaf[branch]:
            self._leaf[branch] = None

    def _delete_branch(self, branch, binary, value):
        is_empty = self._branch[branch].delete(binary, value)
        if is_empty:
            self._branch[branch] = None

    def _empty(self):
        return self._branch.empty() and self._leaf.empty()

    def __repr__(self):
        return "<BitTree branch: %s leaves: %s>" % (self._branch, self._leaf)

if __name__ == "__main__":
    tree = BitTree()
    tree.add("010101", 666)
    tree.add("010101", 888)
    tree.add("101", 110)
    print tree
    tree.add("10111", 116)
    print tree.lookup("101")
    print tree.lookup("10111")
    print tree.lookup("010")
    print tree.lookup("010101")
    print tree
    tree.delete("10111", 116)
    print tree
    print tree.lookup("101")
    print tree.lookup("0")
    print tree.lookup("1")
    print "------------"
    tree = BitTree()
    tree.add("10", 777)
    tree.add("101", 333)
    tree.add("1011", 222)
    tree.add("00", 666)
    print tree.lookup("1011")
