class BasicBlock():
    def __init__(self, name="bb_unk", entry_node=False):
        self.name = name
        self.entry_node = entry_node
        self.edges = []
        self.predecessors = set()
        self.successors = []
        self.parents = []
        self.children = []
        self.dominators = set()
        self.postdominators = []

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return self.name != other.name

    def __and__(self, other):
        if self == other:
            return self
        return None

    def __str__(self):
        return self.name.decode()
    
    def __hash__(self) -> int:
        return int(self.name[3:], 16)