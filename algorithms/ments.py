import numpy as np
from .base import TreeSearchAlgorithm
from components.node import Node

# Incomplete, was following:
# https://arxiv.org/html/2404.07732v1

class MENTS(TreeSearchAlgorithm):
    def __init__(self, env, tree, tau=1.0, epsilon=1.0):
        super().__init__(env, tree)
        self.tau = tau
        self.epsilon = epsilon
        self.alpha = tau 
        self.Q_soft = {}
        self.V_soft = {}

    def softmax(self, x):
        x = np.clip(x, -500, 500) 
        e_x = np.exp((x - np.max(x)) / self.tau)
        return e_x / e_x.sum()

    def soft_policy(self, state, action):
        q_value = self.Q_soft.get((state, action), 0)
        v_value = self.V_soft.get(state, 0)
        return np.exp((q_value - v_value) / self.alpha)

    def compute_value(self, parent, child):
        if child.num_visits == 0:
            return -np.inf

        exploitation_term = child.total_simulation_reward / child.num_visits
        children = self.tree.children(parent)
        children_values = [c.total_simulation_reward / c.num_visits for c in children if c.num_visits > 0]

        if not children_values:
            return exploitation_term

        softmax_value = self.softmax(children_values)
        child_index = children.index(child)
        exploration_term = softmax_value[child_index] + np.random.normal(0, 0.01)
        return exploitation_term + exploration_term

    def best_child(self, node, exploration_constant=None):
        children = self.tree.children(node)
        if not children:
            # print(f"No children for node {node.state}")
            return None

        best_child = None
        best_value = -np.inf
        for child in children:
            value = self.compute_value(node, child)
            # print(f"Node {child.state} value: {value}")
            if value > best_value:
                best_child = child
                best_value = value
        # print(f"Best child for node {node.state} is {best_child.state if best_child else 'None'} with value {best_value}")
        return best_child

    def update_soft_values(self, state, action, reward, next_state):
        N_sa = self.tree.get_visit_count(state, action)
        N_s = self.tree.get_visit_count(state)
        future_value = sum(self.tree.get_visit_count(next_state, a) * self.V_soft.get(next_state, 0) for a in self.env.action_space)
        self.Q_soft[(state, action)] = reward + (future_value / N_sa if N_sa > 0 else 0)
        
        q_values = [self.Q_soft.get((state, a), 0) for a in self.env.action_space]
        self.V_soft[state] = self.alpha * np.log(sum(np.exp(q / self.alpha) for q in q_values))

    def tree_policy(self):
        node = self.tree.root
        while not node.terminal:
            if self.tree.is_expandable(node):
                return self.expand(node)
            else:
                node = self.best_child(node)
        return node

    def run(self, iterations):
        for i in range(iterations):
            self.env.reset()
            node = self.tree_policy()
            reward = self.default_policy(node)
            self.backup(node, reward)
            # if i % 100 == 0:
            #     # print(f"Iteration {i}/{iterations}")
