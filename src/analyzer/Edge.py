#!/usr/bin/python3


class Edge(object):
    def __init__(self, parent, child):
        self.parent = parent
        self.child = child

    def __eq__(self, other):
        if self.parent == other.parent and self.child == other.child:
            return True
        return False

    def __ne__(self, other):
        if self.parent == other.parent and self.child == other.child:
            return False
        return True

    def __str__(self):
        return "{} -> {}".format(self.parent, self.child)
