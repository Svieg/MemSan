#!/usr/bin/python3


class FileNode(object):
    def __init__(self):
        self.name = None
        self.classes = {}
        self.children = []

    def dump(self, cfg):
        line = """
digraph G {
        fontname = "Bitstream Vera Sans"
        fontsize = 8

        node [
                fontname = "Bitstream Vera Sans"
                fontsize = 8
                shape = "record"
        ]

        edge [
                fontname = "Bitstream Vera Sans"
                fontsize = 8
        ] \n
        
"""
        for class_name in self.classes.keys():
            line += str(self.classes[class_name])
        line += cfg
        line += "\n}"
        return line
