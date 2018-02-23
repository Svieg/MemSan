#!/usr/bin/python3


class ReturnNode(object):
    def __init__(self, name):
        self.name = "return{}".format(name)
        self.children = []
        self.type = "return"

    def __str__(self):
        return "".format()