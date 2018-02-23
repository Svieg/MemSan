#!/usr/bin/python3


class ContinueNode(object):
    def __init__(self, name):
        self.name = "continue{}".format(name)
        self.children = []
        self.type = "continue"

    def visit(self):
        pass

    def __str__(self):
        return "".format()