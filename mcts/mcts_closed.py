#  https://gist.github.com/qpwo/c538c6f73727e254fdc7fab81024f6e1
from collections import defaultdict
import math
import random
from mcts.node import Node, ChanceNode


class MCTS:
    def __init__(self, node):
        self.Q = defaultdict(int)  # total reward of each node's random playout
        self.N = defaultdict(int)  # total visit count for each node
        self.children = defaultdict(list)
        self.root = node
        self.children[self.root] = node.get_children()

    def rollout(self, sims=1):
        #  select_child
        path = self.select(self.root)
        leaf = path[-1]
        self.expand(leaf)
        reward = 0

        for sim in range(sims):
            reward += leaf.random_playout(score_method='traditional')

        self.backup(path, reward)

    def select(self, root):
        node = root
        path = []
        while True:
            path.append(node)
            if type(node) == Node:
                if node not in self.children or not self.children[node]:
                    return path
                else:
                    node = self.UCB(choices=self.children[node], parent=node)  # only returns non-chanceNode on first iteration

            elif type(node) == ChanceNode:
                # Chance node draws card and returns possible moves with given card
                if node not in self.children or not self.children[node]:
                    self.children[node] = node.draw_child_list()
                choices = random.choice(self.children[node])
                # select moves based on UCB value
                node = self.UCB(choices=choices, parent=node)

    def expand(self, node):
        if node in self.children or node.is_terminal():  # is node already expanded or terminal?
            return
        self.children[node].append(ChanceNode(node))

    def UCB(self, choices, parent, exploration_weight=10):  # upper confidence bound
        #  UCB = x + c*sqrt(log(N)/n)
        #  x = average ev of node (exploitation)
        #  c = 'exploration' weight
        #  N = parent node visits
        #  n = node visits
        if len(choices) == 1:
            return choices[0]
        parent_visits = self.N[parent]
        if parent_visits == 0:
            log_N_parent = 0
        else:
            log_N_parent = math.log(parent_visits)

        def uct(n):
            child_visits = self.N[n]
            if child_visits == 0:  # unexplored node, gets priority
                return float('inf')
            return (self.Q[n] / self.N[n]) + (exploration_weight * math.sqrt(log_N_parent / child_visits))

        return max(choices, key=uct)

    def backup(self, path, reward):
        player = path[-1].p1
        for node in reversed(path):
            if node.p1 == player:
                self.Q[node] += reward
            else:
                self.Q[node] -= reward
            self.N[node] += 1

    def choose(self):
        choices = self.children[self.root]

        def best_choice(n):
            visits = self.N[n]
            if visits == 0:
                return 0
            return self.Q[n] / self.N[n]

        return max(choices, key=best_choice)

