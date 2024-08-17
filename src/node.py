import random

class Node:

    def __init__(self, value=None, weight=0, prob=0):
        self.value = value
        self.weight = weight
        self.prob = prob
        self.children = []
    
    """
    Adds a child node to the current node and recalculates the probabilities of its children.

    Parameters:
    child_node (Node): The node to be added as a child. This node must be an instance of the Node class.

    Returns:
    None
    """
    def add_child(self, child_node):
        self.children.append(child_node)
        self.calc_prob()
    

    def add_children(self, *nodes):
        for node in nodes:
            self.add_child(node)
    
    """
    Calculates and updates the probability of each child node based on their weights.

    This method iterates over all child nodes, calculates the total weight of all children,
    and then updates each child's probability by dividing its weight by the total weight.
    The probabilities are then multiplied by 100 to express them as percentages.

    Parameters:
    None

    Returns:
    None
    """
    def calc_prob(self):
        weights = 0
        for child in self.children:
            weights += child.weight
        
        for child in self.children:
            child.prob = (child.weight / weights) * 100

    def get_child(self, idx):
        return self.children[idx]
    
    """
    Chooses a child node based on their weights.

    If the 'weighted' parameter is set to False, the function returns the first child node.
    If 'weighted' is True, the function uses a weighted random selection to choose a child node,
    based on their probabilities calculated in the 'calc_prob' method.

    Parameters:
    weighted (bool): A flag indicating whether to use weighted random selection. Default is True.

    Returns:
    Node: The chosen child node. If 'weighted' is False, returns the first child node.
    """
    def choose_child(self, weighted=True):
        if not weighted: return self.children[0]
        
        ran = random.randint(1, 100)

        c = 0
        for child in self.children:
            if ran <= child.prob + c:
                return child.value
        
            c += child.prob