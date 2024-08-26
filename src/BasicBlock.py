class BasicBlock():
    def __init__(self, name="bb_unk", entry_node=False):
        self.name = name
        self.entry_node = entry_node
        self.edges = []
        self.predecessors = []
        self.successors = []
        self.parents = []
        self.children = []
        self.dominators = []
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
        return self.name