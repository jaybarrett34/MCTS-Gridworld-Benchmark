from math import sqrt, log
from .base import TreeSearchAlgorithm

class UCT(TreeSearchAlgorithm):
    def tree_policy(self):
        node = self.tree.root
        while not node.terminal:
            if self.tree.is_expandable(node):
                return self.expand(node)
            else:
                node = self.best_child(node, exploration_constant=1.0/sqrt(2.0))
                result = self.env.step(node.action)
                if len(result) == 4:
                    state, reward, done, info = result
                else:
                    state, reward, done, truncated, info = result
                assert node.state == state
        return node
