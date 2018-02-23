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
        self.counter = {
            "functions" : 0,
            "if" : 0,
            "while" : 0,
            "return" : 0,
            "unaryOperator" : 0,
            "continue" : 0,
            "condition": 0,
            "break": 0,
            "whileEnd": 0,
            "ifEnd": 0
        }

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
            line += self.recursiveDump(function)
        print(line)

        with open("cfg.dot", "w") as f:
            f.write(self.file.dump(line))

    def recursiveDump(self, node):
        line = ""
        if node.name != "end":
            line += node.name + " [label={}]\n".format(node.type)
        for child in node.children:
            line += "{} -> {}\n".format(node.name, child.name)
        for child in node.children:
            line += self.recursiveDump(child)
        return line

    def parseWhile(self, parent, whileXMLNode, previousNode):
        self.counter["while"] += 1
        new_while = WhileNode(self.counter["while"])
        parent.children.append(new_while)
        if previousNode is not None:
            previousNode.children.append(new_while)
        self.counter["condition"] += 1
        condition = BaseNode(self.counter["condition"], "Condition")
        new_while.children.append(condition)
        whileEnd = BaseNode(self.counter["while"], "whileEnd")
        condition.children.append(whileEnd)
        self.parseNode(condition, whileXMLNode)
        return whileEnd

    def parseIf(self, parent, ifXMLNode, previousNode):
        self.counter["if"] += 1
        new_if = IfNode(self.counter["if"])
        parent.children.append(new_if)
        if previousNode is not None:
            previousNode.children.append(new_if)
        condition = BaseNode("", "Condition")
        new_if.children.append(condition)
        self.parseNode(condition, ifXMLNode)
        ifEnd = BaseNode(self.counter["if"], "ifEnd")
        condition.children.append(ifEnd)
        return ifEnd

    def parseReturn(self, parent, returnXMLNode, previousNode):
        self.counter["return"] += 1
        new_return = ReturnNode(self.counter["return"])
        if previousNode is not None:
            previousNode.children.append(new_return)
        parent.children.append(new_return)
        new_return.children.append(self.endNode)
        self.parseNode(new_return, returnXMLNode)
        return None

    def parseBreak(self, parent, returnXMLNode, previousNode):
        self.counter["break"] += 1
        new_break = BaseNode(self.counter["break"], "break")
        if previousNode is not None:
            previousNode.children.append(new_break)
        parent.children.append(new_break)
        self.parseNode(new_break, returnXMLNode)
        return None

    def parseContinue(self, parent, returnXMLNode, previousNode):
        self.counter["continue"] += 1
        new_cont = BaseNode(self.counter["continue"], "continue")
        if previousNode is not None:
            previousNode.children.append(new_cont)
        parent.children.append(new_cont)
        self.parseNode(new_cont, returnXMLNode)
        return None

    def parseFor(self, parent, XMLNode, previousNode):
        self.counter["for"] += 1
        new_for = BaseNode(self.counter["for"], "for")
        parent.children.append(new_for)
        if previousNode is not None:
            previousNode.children.append(new_for)
        self.counter["condition"] += 1
        condition = BaseNode(self.counter["condition"], "Condition")
        new_for.children.append(condition)
        forEnd = BaseNode("", "forEnd")
        condition.children.append(forEnd)
        self.parseNode(condition, XMLNode)
        return forEnd

    def parseUnaryOperator(self, parent, unaryOperatorXMLNode, previousNode):
        self.counter["unaryOperator"] += 1
        new_op = UnaryOperatorNode(self.counter["unaryOperator"])
        parent.children.append(new_op)
        if previousNode is not None:
            previousNode.children.append(new_op)
        self.parseNode(new_op, unaryOperatorXMLNode)
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