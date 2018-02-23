#!/usr/bin/python3


class BaseNode(object):
    def __init__(self, name, type):
        self.name = "{}{}".format(type, name)
        self.children = []
        self.type = type