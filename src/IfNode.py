#!/usr/bin/python3


class IfNode(object):
    def __init__(self, name):
        self.name = "if{}".format(name)
        self.children = []
        self.type = "ifBegin"