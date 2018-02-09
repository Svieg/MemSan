#!/usr/bin/python3


class ClassNode(object):
    def __init__(self, name):
        self.name = name
        self.attributes = {}
        self.methods = {}
        self.classes_used = []
        self.parent_class = None

    def __str__(self):
        line = "{} [\n\t\tlabel = \"".format(self.name)
        line += "{ "
        line += "{}".format(self.name)
        if self.parent_class:
            line += "::{}".format(self.parent_class)
        line += "|"
        for attribute_name in self.attributes.keys():
            line += str(self.attributes[attribute_name])
        line += "|"
        for method_name in self.methods.keys():
            line += str(self.methods[method_name])
        line += "}\"\n\t]\n"
        for class_used in self.classes_used:
            line += "\n{} -> {}\n".format(self.name, class_used)
        if self.parent_class is not None:
            line += "{} -> {} [arrowhead = \"empty\"]\n".format(self.name, self.parent_class)
        return line