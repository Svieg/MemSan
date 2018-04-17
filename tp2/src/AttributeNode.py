#!/usr/bin/python3


class AttributeNode(object):
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.isPublic = False
    def __str__(self):
        symbol = "-"
        if self.isPublic:
            symbol = "+"
        return "{} {} : {}\\l".format(symbol, self.name, self.type)
