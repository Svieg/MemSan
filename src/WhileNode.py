#!/usr/bin/python3


class WhileNode(object):
    def __init__(self, name):
        self.name = "while{}".format(name)
        self.children = []
        self.type = "whileBegin"

    def __str__(self):
        return "".format()