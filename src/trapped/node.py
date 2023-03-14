class Node:
    def __init__(self, name, x, y, attacker_action, path_prob=1, parent=None):
        self.name = name
        self.x = x
        self.y = y
        self.attacker_action = attacker_action
        self.path_prob = path_prob
        self.parent = parent
        self.path = parent.path + [self] if parent else [self]
        self.depth = len(self.path) - 1

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    '''def __eq__(self, other):
        return self.name == other.name'''

    def __hash__(self):
        return hash