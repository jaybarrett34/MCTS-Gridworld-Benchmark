import numpy as np
from .base import TreeSearchAlgorithm
from components.node import Node

class BTS(TreeSearchAlgorithm):
    def __init__(self, env, tree, tau=1.0, epsilon=1.0):
        super().__init__(env, tree)
        self.tau = tau
        self.epsilon = epsilon
        self.Q_values = {}
        self.V_values = {}

    def softmax(self, x):
        x = np.clip(x, -500, 500)
        e_x = np.exp((x - np.max(x)) / self.tau)
        return e_x / e_x.sum()

    def boltzmann_policy(self, state):
        q_values = [self.Q_values.get((state, a), 0) for a in range(self.env.action_space.n)]
        softmax_values = self.softmax(q_values)
        return np.random.choice(range(self.env.action_space.n), p=softmax_values)

    def compute_value(self, parent, child):
        if child.num_visits == 0:
            return -np.inf
        exploitation_term = child.total_simulation_reward / child.num_visits
        exploration_term = np.random.normal(0, self.epsilon)
        return exploitation_term + exploration_term

    def best_child(self, node, exploration_constant=None):
        children = self.tree.children(node)
        if not children:
            return None

        best_child = None
        best_value = -np.inf
        for child in children:
            value = self.compute_value(node, child)
            if value > best_value:
                best_child = child
                best_value = value
        return best_child

    def update_bellman_values(self, state, action, reward, next_state):
        state = (state,) if isinstance(state, int) else tuple(state)
        next_state = (next_state,) if isinstance(next_state, int) else tuple(next_state)
        N_sa = self.tree.get_visit_count(state, action)
        future_value = sum(self.tree.get_visit_count(next_state, a) * self.V_values.get(next_state, 0) for a in range(self.env.action_space.n))
        self.Q_values[(state, action)] = reward + (future_value / N_sa if N_sa > 0 else 0)
        q_values = [self.Q_values.get((state, a), 0) for a in range(self.env.action_space.n)]
        self.V_values[state] = max(q_values)

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

    def backup(self, node, reward):
        while node:
            state = node.state
            action = node.action
            parent_node = self.tree.parent(node)
            next_state = parent_node.state if parent_node else None
            if next_state is not None:
                self.update_bellman_values(state, action, reward, next_state)
            node.num_visits += 1
            node.total_simulation_reward += reward
            node.performance = node.total_simulation_reward / node.num_visits
            node = parent_node
