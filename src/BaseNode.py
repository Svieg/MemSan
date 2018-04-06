#!/usr/bin/python3


class BaseNode(object):
    def __init__(self, name, type):
        self.name = "{}{}".format(type, name)
        self.children = []
        self.parents = []
        self.type = type
        self.visited = False
        self.dom_tree_parent = None
        self.same_level_node = None
        self.dom = []
        self.pdom = []

    def visit(self):
        pass

    def getLeafs(self):
        if len(self.children) == 0:
            return [self]
        leafs = []
        for child in self.children:
            leafs += child.getLeafs()
        return leafs


    def __eq__(self, other):
        if not isinstance(other, BaseNode):
            return False
        if self.name == other.name:
            return True
        return False

    def __ne__(self, other):

        if other is None:
            return

        if self.name == other.name:
            return False
        return True

    def __str__(self):
        return self.name
