#!/usr/bin/python3


class MethodNode(object):
    def __init__(self, name, return_type):
        self.name = name
        self.return_type = return_type
        self.isPublic = False

    def __str__(self):
        symbol = "-"
        if self.isPublic:
            symbol = "+"
        return "{} {}() : {}\\l".format(symbol, self.name, self.return_type)
