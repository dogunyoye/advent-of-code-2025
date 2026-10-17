class UnionFind:
    """Disjoint-set forest with path compression and union by rank.

    Elements are any hashable values. They are added to the structure lazily
    the first time they are seen by :meth:`add`, :meth:`find` or :meth:`union`.
    """

    def __init__(self):
        self._parent = {}
        self._rank = {}
        self.n_comps = 0

    def add(self, x) -> None:
        if x not in self._parent:
            self._parent[x] = x
            self._rank[x] = 0
            self.n_comps += 1

    def find(self, x):
        self.add(x)

        root = x
        while self._parent[root] != root:
            root = self._parent[root]

        # Path compression.
        while self._parent[x] != root:
            self._parent[x], x = root, self._parent[x]

        return root

    def union(self, x, y) -> bool:
        """Merge the sets containing ``x`` and ``y``.

        Returns ``True`` if the two elements were in different sets.
        """
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False

        if self._rank[root_x] < self._rank[root_y]:
            root_x, root_y = root_y, root_x

        self._parent[root_y] = root_x
        if self._rank[root_x] == self._rank[root_y]:
            self._rank[root_x] += 1

        self.n_comps -= 1
        return True

    def connected(self, x, y) -> bool:
        return self.find(x) == self.find(y)

    def components(self) -> list:
        """Return the disjoint sets as a list of lists of elements."""
        groups = {}
        for x in self._parent:
            groups.setdefault(self.find(x), []).append(x)
        return list(groups.values())
