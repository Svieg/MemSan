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

        #print(f"Basic blocks: {self.basic_blocks}")
        # load edges
        # matches (bb_4ac) -> (bb_4b1)
        regex = re.compile(b"(bb_.*) -> (bb_.*) \[")
        matches = regex.findall(dot)

        for match in matches:
            #print(f"Edge: {match}")
            self.edges.append(Edge(match[0], match[1]))
            self.basic_blocks[match[0]].children.append(match[1])
            self.basic_blocks[match[0]].successors.append(match[1])
            self.basic_blocks[match[1]].parents.append(match[0])
            self.basic_blocks[match[1]].predecessors.add(self.basic_blocks[match[0]])

    def build_dom_tree(self):
        changed = True
        # Initialize every basic block with all the nodes as dominators, except the entry node
        for basic_block_name in self.basic_blocks:
            basic_block = self.basic_blocks[basic_block_name]
            if len(basic_block.predecessors) == 0:
                #print(f"Entry node: {str(basic_block)}")
                basic_block.dominators.add(basic_block)
            else:
                basic_block.dominators = set(self.basic_blocks.values())
        
        # Iterate through all basic blocks and intersect with its predecessors' dominators
        while changed:
            changed = False
            for basic_block_name in self.basic_blocks:
                #print(f"Basic Block: {basic_block}")
                temp_dominators = set()
                basic_block = self.basic_blocks[basic_block_name]
                temp_dominators.add(basic_block)
                predecessors = basic_block.predecessors
                #print(f"Predecessors: {predecessors}")
                for predecessor in predecessors:
                    #print(predecessor)
                    temp_dominators = basic_block.dominators & predecessor.dominators
                    temp_dominators.add(basic_block)
                if temp_dominators != basic_block.dominators:
                    basic_block.dominators = temp_dominators
                    changed = True
                #print(f"New doms = {temp_dominators}")

        for basic_block in self.basic_blocks.values():
            print(basic_block)
            print(basic_block.dominators)

if __name__ == "__main__":
    ghidra_analyzer = GhidraAnalyzer()
    ghidra_analyzer.load_cfg()
    ghidra_analyzer.build_dom_tree()
    #ghidra_analyzer.build_pdom_tree()
    #ghidra_analyzer.build_cd # Code Dependence Graph