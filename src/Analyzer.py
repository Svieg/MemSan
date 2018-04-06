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
from Edge import Edge

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

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
        self.reversed_edges = []
        self.tree_nodes = []
        self.dump_cfg = False

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

        # edge case function node
        for child in self.root:
            if child.tag == "function":
                self.parseFunction(child)

        # Adding node to .dot format
        line = "{} [label=\"{}\"]\n".format(self.endNode.name, self.endNode.name)

        # DFS for children
        for function in self.file.children:
            tmp_line = self.recursiveDump(function)
            line += tmp_line

        #self.reverse_edges()

        for node in self.nodes:
            if node.same_level_node is not None:
                for same_child in node.same_level_node.children:
                    self.add_edge(node, same_child)
        if self.dump_cfg:
            for node in self.nodes:
                for child in node.children:
                    line += "{} -> {}\n".format(node.name, child.name)

        for node in self.nodes:
            if len(node.children) == 0:
                self.add_edge(node, self.endNode)

        print(line)

        with open("cfg.dot", "w") as f:
            f.write(self.file.dump(line))

    def new_node(self, label, parent):
        self.counter += 1
        node = BaseNode(self.counter, label)
        if parent is None:
            return node

        #if parent.type == "return":
        #    parent, node = node, parent

        self.nodes.append(node)

        self.add_edge(parent, node)

        self.tree_nodes.append(node)

        node.dom_tree_parent = parent

        return node

    def add_edge(self, parent, child):
        if parent.name == "end":
            return
        if parent.type == "return" and child.name != "end":
            return

        if child not in parent.children:
            parent.children.append(child)

        if parent not in child.parents:
            child.parents.append(parent)

        new_edge = Edge(parent, child)
        if new_edge not in self.edges:
            self.edges.append(new_edge)

    def recursiveDump(self, node):

        if node.visited == True:
            return ""

        node.visited = True

        line = ""
        if node.name != "end":
            line += node.name + " [label={}]\n".format(node.name)

       # previous_child = None
       # for child in node.children:
       #     if previous_child is not None:
       #         self.add_edge(previous_child, child)
       #     previous_child = child

        for child in node.children:
            line += self.recursiveDump(child)
        return line

    def parseWhile(self, parent, XMLNode, previousNode):

        new_while = self.new_node("WhileBegin", parent)

        condition = self.new_node("Condition", new_while)

        whileEnd = self.new_node("WhileEnd", condition)


        #foundWhileBegin = False
        #while not foundWhileBegin:

        node_to_return = whileEnd
        new_parent = condition
        for child in XMLNode:
            node_to_return = self.parseNode(new_parent, child, new_while)
            new_parent = node_to_return

        #leafs = condition.getLeafs()
        #for child in leafs:
        #    self.add_edge(child, new_while)

        return whileEnd

    def parseIf(self, parent, XMLNode, previousNode):

        new_if = self.new_node("ifBegin", parent)

        # condition
        condition = self.new_node("Condition", new_if)

        ifEnd = self.new_node("ifEnd", condition)

        if previousNode is not None:
            ifEnd.children.append(previousNode)

        node_to_return = ifEnd
        new_parent = condition
        for child in XMLNode:
            node_to_return = self.parseNode(new_parent, child, previousNode)
            new_parent = node_to_return

        self.add_edge(ifEnd, node_to_return)
        #ifEnd.same_level_node = node_to_return

        return node_to_return

    def parseReturn(self, parent, XMLNode, previousNode):

        new_return = self.new_node("return", parent)

        self.add_edge(new_return, self.endNode)

        #node_to_return = new_return
        #for child in XMLNode:
        #    node_to_return = self.parseNode(node_to_return, child)

        return new_return

    def parseBreak(self, parent, XMLNode, previousNode):

        new_break = self.new_node("break", parent)

        node_to_return = new_break
        for child in XMLNode:
            node_to_return = self.parseNode(node_to_return, child, previousNode)

        return node_to_return

    def parseContinue(self, parent, XMLNode, previousNode):

        new_continue = self.new_node("continue", parent)

        node_to_return = new_continue
        for child in XMLNode:
            node_to_return = self.parseNode(node_to_return, child, previousNode)
        return node_to_return

    def parseFor(self, parent, XMLNode, previousNode):

        new_for = self.new_node("for", parent)

        condition = self.new_node("Condition", new_for)

        forEnd = self.new_node("forEnd", condition)

        node_to_return = forEnd
        new_parent = condition
        for child in XMLNode:
            node_to_return = self.parseNode(new_parent, child, previousNode)
            new_parent = node_to_return

        return node_to_return

    def parseUnaryOperator(self, parent, unaryOperatorXMLNode, previousNode):

        new_unary_op = self.new_node("UnaryOperator", parent)

        node_to_return = new_unary_op
        for child in unaryOperatorXMLNode:
            node_to_return = self.parseNode(node_to_return, child, previousNode)
        return node_to_return

    def parseBinaryOperator(self, parent, binaryOperatorXMLNode, previousNode):

        new_binary_op = self.new_node("BinaryOperator", parent)

        node_to_return = new_binary_op
        for child in binaryOperatorXMLNode:
            node_to_return = self.parseNode(node_to_return, child, previousNode)
        return node_to_return

    def parseCall(self, parent, callXMLNode, previousNode):

        call = self.new_node("callExpr", parent)

        node_to_return = call
        for child in callXMLNode:
            node_to_return = self.parseNode(node_to_return, child, previousNode)
        return node_to_return

    def parseFunction(self, XMLNode):

        parent = None
        for functionChild in XMLNode:
            if functionChild.tag == "functionName":
                functionName = functionChild.text.strip()
                new_function = self.new_node(functionName, None)
                parent = new_function
            else:
                parent = self.parseNode(parent, functionChild, None)

        self.file.children.append(new_function)
        self.endNode.type = "Exit\\n{}".format(functionName)

        return new_function

    def parseNode(self, parent, XMLNode, node):
        node = parent
        if XMLNode.tag == "while":
            node = self.parseWhile(parent, XMLNode, node)
        if XMLNode.tag == "if":
            node = self.parseIf(parent, XMLNode, node)
        if XMLNode.tag == "callExpr":
            node = self.parseCall(parent, XMLNode, node)
        if XMLNode.tag == "return":
            node = self.parseReturn(parent, XMLNode, node)
        if XMLNode.tag == "unaryOperator":
            node = self.parseUnaryOperator(parent, XMLNode, node)
        if XMLNode.tag == "binaryOperator":
            node = self.parseBinaryOperator(parent, XMLNode, node)
        if XMLNode.tag == "break":
            node = self.parseBreak(parent, XMLNode, node)
        if XMLNode.tag == "continue":
            node = self.parseContinue(parent, XMLNode, node)
        if XMLNode.tag == "for":
            node = self.parseFor(parent, XMLNode, node)
        return node

    def reverse_edges(self):
        for edge in self.edges:
            self.reversed_edges.append(Edge(edge.child, edge.parent))

    def reverse_cfg(self):
        for node in self.nodes:
            tmp_parents = node.parents
            node.parents = node.children
            node.children = tmp_parents

    def nca(self, n1, n2):
        path = []
        c = n1
        i = 0
        while c is not None:
            path.append(c)
            c = c.dom_tree_parent
            if i == 100:
                break
            i += 1
        c = n2
        i = 0
        while c is not None and c not in path:
            c = c.dom_tree_parent
            if i == 100:
                break
            i += 1

        return c

    def make_dom_tree(self):
        changed = True
        while changed:
            changed = False
            for node in self.nodes:
                if len(node.parents) == 0:
                    continue
                parent = node.parents[0]
                for p in node.parents[1:]:
                    if p not in self.tree_nodes:
                        continue
                    parent = self.nca(parent, p)
                if node.dom_tree_parent != parent:
                    node.dom_tree_parent = parent
                    changed = True

    # Algo inspire du cours
    # Je ne sais pas comment ressortir le graph apres cependant
    def algo_dom_tree(self):
        changed = True

        entry = self.file.children[0]

        entry.dom = entry

        for node in self.nodes:
            if node == entry:
                continue
            node.dom.append(node)

        while changed:
            changed = False
            for node in self.nodes:
                if len(node.parents) == 0:
                    continue
                if len(node.parents) == 1:
                    only_parent = node.parents[0]
                    if only_parent not in node.dom:
                        node.dom.append(node.parents[0])
                        changed = True
                else:
                    before = node.dom
                    itDom = node.parents[0].dom
                    for i in range(1, len(node.parents)):
                        parent = node.parents[i]
                        itDom = intersection(itDom, parent.dom)
                    node.dom = itDom
                    if len(node.dom) != len(before):
                        changed = True
                    for dom in node.dom:
                        if dom not in before: # same size but diff nodes
                            changed = True
        return

    def make_pdom_tree(self):
        changed = True

        end = self.endNode

        end.pdom = end

        for node in self.nodes:
            if node == end:
                continue
            node.pdom.append(node)

        while changed:
            changed = False
            for node in self.nodes:
                if len(node.children) == 0:
                    continue
                if len(node.children) == 1:
                    only_parent = node.children[0]
                    if only_parent not in node.pdom:
                        node.pdom.append(node.children[0])
                        changed = True
                else:
                    before = node.pdom
                    itDom = node.children[0].pdom
                    for i in range(1, len(node.children)):
                        parent = node.children[i]
                        itDom = intersection(itDom, parent.pdom)
                    node.pdom = itDom
                    if len(node.pdom) != len(before):
                        changed = True
                    for dom in node.pdom:
                        if dom not in before:  # same size but diff nodes
                            changed = True
        return

    def dump_dom_tree(self):
        line = ""
        for node in self.nodes:
            line += node.name + " [label={}]\n".format(node.name)
            for dom in node.dom:
                if dom != node:
                    line += "{} -> {}\n".format(node.name, dom.name)
        dump_dot("dom.dot", line)

    def dump_pdom_tree(self):
        line = ""
        for node in self.nodes:
            line += node.name + " [label={}]\n".format(node.name)
            for pdom in node.pdom:
                if pdom != node:
                    line += "{} -> {}\n".format(node.name, pdom.name)
        dump_dot("pdom.dot", line)

    def build_cd(self):
        cd = self.nodes


def dump_dot(filename, content):
    with open(filename, "w") as f:
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
        line += content
        line += "\n}"
        print(line)
        f.write(line)



if __name__ == "__main__":
    analyzer = ASTAnalyzer()
    analyzer.load_AST()
    analyzer.get_root_node()
    analyzer.buildCFG()
    analyzer.algo_dom_tree()
    #analyzer.make_dom_tree()
    analyzer.dump_dom_tree()
    analyzer.dump_pdom_tree()