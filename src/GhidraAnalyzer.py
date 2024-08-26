from Edge import Edge
from BasicBlock import BasicBlock
import re

class GhidraAnalyzer():
    def __init__(self):
        self.name = "GhidraAnalyzer"
        self.filename = "cfg/entry.dot"
        self.basic_blocks = {}
        self.edges = []

    def load_cfg(self):
        # read .dot file
        with open(self.filename, "rb") as dot_file:
            dot = dot_file.read()
        # load basic blocks
        regex = re.compile(b"(bb_.*) \[shape=")
        matches = regex.findall(dot)

        for match in matches:
            self.basic_blocks[match] = BasicBlock(match)

        print(self.basic_blocks)
        # load edges
        # matches (bb_4ac) -> (bb_4b1)
        regex = re.compile(b"(bb_.*) -> (bb_.*) \[")
        matches = regex.findall(dot)

        print(matches)
        for match in matches:
            self.edges.append(Edge(match[0], match[1]))
            self.basic_blocks[match[0]].children.append(match[1])
            self.basic_blocks[match[0]].successors.append(match[1])
            self.basic_blocks[match[1]].parents.append(match[0])
            self.basic_blocks[match[1]].predecessors.append(match[0])

    def build_dom_tree(self):
        changed = False
        for basic_block_name in self.basic_blocks:
            new_doms = []
            predecessors = self.basic_blocks[basic_block_name].predecessors
            for predecessor in predecessors:
                for second_order_predecessor in predecessors.predecessors:
                    
            


        

if __name__ == "__main__":
    ghidra_analyzer = GhidraAnalyzer()
    ghidra_analyzer.load_cfg()
    ghidra_analyzer.build_dom_tree()
    #ghidra_analyzer.build_pdom_tree()
    #ghidra_analyzer.build_cd # WTF is CD?