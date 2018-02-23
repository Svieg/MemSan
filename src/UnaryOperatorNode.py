#!/usr/bin/python3


class UnaryOperatorNode(object):
    def __init__(self, name):
        self.name = "unaryOperator{}".format(name)
        self.children = []
        self.type = "unaryOperator"

    def __str__(self):
        # TODO: new dot node
        # TODO: links for children
        return "".format()