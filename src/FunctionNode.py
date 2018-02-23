#!/usr/bin/python3


class FunctionNode(object):
    def __init__(self, name):
        self.name = name
        self.children = []
        self.type = "\"Entry\\n{}\"".format(name)

    def __str__(self):
        return "".format()
