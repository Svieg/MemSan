#!/usr/bin/python3

import xml.etree.ElementTree as ET
from FileNode import FileNode
from WhileNode import WhileNode
from FunctionNode import FunctionNode
from IfNode import IfNode
from ReturnNode import ReturnNode
from UnaryOperatorNode import UnaryOperatorNode
from ClassNode import ClassNode
from MethodNode import MethodNode
from AttributeNode import AttributeNode
from BaseNode import BaseNode


class ASTAnalyzer(object):
    """
    Takes the AST dumped and calculates metrics from it.
    """
    def __init__(self, filename="../MemSan.dump", output_filename="test.dot"):
        self.filename = filename
        self.output_filename = output_filename
        self.AST = None
        self.root = None
        self.currentID = 0
        self.file = FileNode()
        self.endNode = BaseNode("end", "")
        self.counter = 0
        self.edges = []
        self.nodes = []

    def load_AST(self):
        self.AST = ET.parse(self.filename)

    def get_root_node(self):
        self.root = self.AST.getroot()

    def append_to_output(self, str_to_append):
        with open(self.output_filename, "a") as f:
            f.write(str_to_append)

    def parse_class(self):
        for child in self.root:
            if child.tag == "filename":
                self.file.name = child.text
            elif child.tag == "class":
                for classChild in child:
                    if classChild.tag == "className":
                        class_name = classChild.text
                        new_class = ClassNode(class_name)
                    elif classChild.tag == "parentClass":
                        parent_class = classChild.text
                        if parent_class.find("class ") != -1:
                            parent_class = parent_class[len("class ") - 1:]
                        new_class.parent_class = parent_class
                    elif classChild.tag == "method":
                        for methodChild in classChild:
                            if methodChild.tag == "methodName":
                                method_name = methodChild.text
                            elif methodChild.tag == "methodReturnType":
                                method_return_type = methodChild.text
                        new_method = MethodNode(method_name, method_return_type)
                        new_class.methods[method_name] = new_method
                    elif classChild.tag == "attribute":
                        for attributeChild in classChild:
                            if attributeChild.tag == "attributeName":
                                attribute_name = attributeChild.text
                            elif attributeChild.tag == "attributeType":
                                attribute_type = attributeChild.text
                                if attribute_type.find("class ") != -1:
                                    attribute_type = attribute_type[len("class ") - 1:]
                                    new_class.classes_used.append(attribute_type)
                        new_attribute = AttributeNode(attribute_name, attribute_type)
                        new_class.attributes[attribute_name] = new_attribute
                self.file.classes[class_name] = new_class
        with open(self.output_filename, "w") as f:
            f.write(str(self.file))

    def getFilename(self):
        raise

    def buildCFG(self):
        for child in self.root:
            if child.tag == "function":
                self.parseFunction(child)
        line = "{} [label=\"{}\"]\n".format(self.endNode.name, self.endNode.type)
        for function in self.file.children:
            tmp_line = self.recursiveDump(function)
            line += tmp_line
        print(line)

        with open("cfg.dot", "w") as f:
            f.write(self.file.dump(line))

    def new_node(self, label, parent):
        self.counter += 1
        node = BaseNode(self.counter, label)
        parent.children.append(node)
        node.parent = parent
        return node

    def recursiveDump(self, node):
        line = ""
        if node.name != "end":
            line += node.name + " [label={}]\n".format(node.type)
        for child in node.children:
            new_edge = [node.name, child.name]
            if new_edge not in self.edges:
                self.edges.append(new_edge)
                line += "{} -> {}\n".format(node.name, child.name)

        for child in node.children:
            line += self.recursiveDump(child)
        return line

    def parseWhile(self, parent, whileXMLNode, previousNode):
        new_while = self.new_node("WhileBegin", parent)

        if previousNode is not None:
            previousNode.children.append(new_while)

        condition = self.new_node("Condition", new_while)

        whileEnd = self.new_node("WhileEnd", condition)

        #foundWhileBegin = False
        #while not foundWhileBegin:

        self.parseNode(condition, whileXMLNode)
        return whileEnd

    def parseIf(self, parent, ifXMLNode, previousNode):

        new_if = self.new_node("ifBegin", parent)

        if previousNode is not None:
            previousNode.children.append(new_if)

        # condition
        condition = self.new_node("Condition", new_if)

        ifEnd = self.new_node("ifEnd", condition)

        self.parseNode(condition, ifXMLNode)

        return ifEnd

    def parseReturn(self, parent, returnXMLNode, previousNode):

        new_return = self.new_node("return", parent)

        if previousNode is not None:
            previousNode.children.append(new_return)

        new_return.children.append(self.endNode)
        self.parseNode(new_return, returnXMLNode)
        #TODO: check why returns None
        return None

    def parseBreak(self, parent, returnXMLNode, previousNode):

        new_break = self.new_node("break", parent)

        if previousNode is not None:
            previousNode.children.append(new_break)

        self.parseNode(new_break, returnXMLNode)

        return None

    def parseContinue(self, parent, returnXMLNode, previousNode):

        new_continue = self.new_node("continue", parent)

        if previousNode is not None:
            previousNode.children.append(new_continue)

        self.parseNode(new_continue, returnXMLNode)
        return None

    def parseFor(self, parent, XMLNode, previousNode):

        new_for = self.new_node("for", parent)

        if previousNode is not None:
            previousNode.children.append(new_for)

        condition = self.new_node("Condition", new_for)

        forEnd = self.new_node("forEnd", condition)

        self.parseNode(condition, XMLNode)

        return forEnd

    def parseUnaryOperator(self, parent, unaryOperatorXMLNode, previousNode):

        new_unary_op = self.new_node("UnaryOperator", parent)

        if previousNode is not None:
            previousNode.children.append(new_unary_op)
        self.parseNode(new_unary_op, unaryOperatorXMLNode)
        return None

    def parseFunction(self, functionXMLNode):
        for functionChild in functionXMLNode:
            if functionChild.tag == "functionName":
                functionName = functionChild.text.strip()
                new_function = FunctionNode(functionName)
        self.file.children.append(new_function)
        self.endNode.type = "Exit\\n{}".format(functionName)
        self.parseNode(new_function, functionXMLNode)
        return None

    def parseNode(self, parent, XMLNode):
        node = None
        for child in XMLNode:
            if child.tag == "while":
                node = self.parseWhile(parent, child, node)
            if child.tag == "if":
                node = self.parseIf(parent, child, node)
            if child.tag == "return":
                node = self.parseReturn(parent, child, node)
            if child.tag == "unaryOperator":
                node = self.parseUnaryOperator(parent, child, node)
            if child.tag == "break":
                node = self.parseBreak(parent, child, node)
            if child.tag == "continue":
                node = self.parseContinue(parent, child, node)
            if child.tag == "for":
                node = self.parseFor(parent, child, node)


if __name__ == "__main__":
    analyzer = ASTAnalyzer()
    analyzer.load_AST()
    analyzer.get_root_node()
    analyzer.buildCFG()