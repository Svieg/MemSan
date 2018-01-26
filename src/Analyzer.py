#!/usr/bin/python3

import xml.etree.ElementTree as ET
from ClassNode import ClassNode


class ASTAnalyzer(object):
    """
    Takes the AST dumped and calculates metrics from it.
    """
    def __init__(self, filename="../MemSan.dump", output_filename="output.txt"):
        self.filename = filename
        self.output_filename = output_filename
        self.AST = None
        self.root = None
        self.currentID = 0

    def load_AST(self):
        self.AST = ET.parse(self.filename)

    def get_root_node(self):
        self.root = self.AST.getroot()

    def append_to_output(self, str_to_append):
        with open(self.output_filename, "a") as f:
            f.write(str_to_append)

    def parse_class(self):
        for child in self.root:
            if classChild.tag == "filename":
                filename = classChild.text
            elif child.tag == "class":
                for classChild in child:
                    if classChild.tag == "className":
                        classname = classChild.text
                    elif classChild.tag == "method":
                        nb_ifs = 0
                        nb_while = 0
                        nb_break = 0
                        nb_local_vars = 0
                        for methodChild in classChild:
                            if methodChild.tag == "methodName":
                                methodName = methodChild.text
                            elif methodChild.tag == "if":
                                nb_ifs += 1
                            elif methodChild.tag == "while":
                                nb_while += 1
                            elif methodChild.tag == "break":
                                nb_break += 1
                            elif methodChild.tag == "var":
                                nb_local_vars += 1
                        output_line = "{},{},{},{},{},{},{},{}".format(
                            self.currentID,
                            filename,
                            classname,
                            methodName,
                            nb_ifs,
                            nb_while,
                            nb_break,
                            nb_local_vars
                        )
                        self.currentID += 1
                        self.append_to_output(output_line)


    def getFilename(self):
        raise


if __name__ == "__main__":
    analyzer = ASTAnalyzer()
    analyzer.load_AST()
    analyzer.get_root_node()
    analyzer.parse_class()
