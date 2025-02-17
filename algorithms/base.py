import random
from components.node import Node
from math import sqrt, log

class TreeSearchAlgorithm:
    def __init__(self, env, tree):
        self.env = env
        self.tree = tree
        self.action_space = self.env.action_space.n
        self.path = []
        self.steps = []
        state = self.env.reset()
        self.tree.add_node(Node(state=state, action=None, action_space=self.action_space, reward=0, terminal=False))

    def expand(self, node):
        action = node.untried_action()
        result = self.env.step(action)
        if len(result) == 4:
            state, reward, done, info = result
        else:
            state, reward, done, truncated, info = result
        new_node = Node(state=state, action=action, action_space=self.action_space, reward=reward, terminal=done)
        self.tree.add_node(new_node, node)
        return new_node

    def default_policy(self, node):
        if node.terminal:
            return node.reward

        while True:
            action = random.randint(0, self.action_space - 1)
            result = self.env.step(action)
            if len(result) == 4:
                state, reward, done, info = result
            else:
                state, reward, done, truncated, info = result
            if done:
                return reward

    def compute_value(self, parent, child, exploration_constant):
        exploitation_term = child.total_simulation_reward / child.num_visits
        exploration_term = exploration_constant * sqrt(2 * log(parent.num_visits) / child.num_visits)
        return exploitation_term + exploration_term

    def best_child(self, node, exploration_constant):
        best_child = self.tree.children(node)[0]
        best_value = self.compute_value(node, best_child, exploration_constant)
        iter_children = iter(self.tree.children(node))
        next(iter_children)
        for child in iter_children:
            value = self.compute_value(node, child, exploration_constant)
            if value > best_value:
                best_child = child
                best_value = value
        return best_child

    def tree_policy(self):
        raise NotImplementedError

    def backup(self, node, reward):
        while node:
            node.num_visits += 1
            node.total_simulation_reward += reward
            node.performance = node.total_simulation_reward / node.num_visits
            node = self.tree.parent(node)

    def forward(self):
        self._forward(self.tree.root)

    def _forward(self, node):
        best_child = self.best_child(node, exploration_constant=0)
        print("****** {} ******".format(best_child.state))
        for child in self.tree.children(best_child):
            print("{}: {:0.4f}".format(child.state, child.performance))
        if len(self.tree.children(best_child)) > 0:
            self._forward(best_child)

    def run(self, iterations):
        for _ in range(iterations):
            self.env.reset()
            node = self.tree_policy()
            reward = self.default_policy(node)
            self.backup(node, reward)

    def get_path(self, node):
        path = []
        while node:
            path.append(node.state)
            node = self.tree.parent(node)
        return path[::-1]

    def print_best_path(self):
        best_node = self.tree.root
        while not best_node.terminal:
            best_node = self.best_child(best_node, exploration_constant=0)
        best_path = self.get_path(best_node)
        print("Best path found:")
        for state in best_path:
            print(state, end=" -> ")
        print("Goal")

    def get_steps(self):
        return self.steps
