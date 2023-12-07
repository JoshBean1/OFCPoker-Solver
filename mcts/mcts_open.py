from collections import defaultdict
import math


class MCTS:
    def __init__(self, node):
        self.Q = defaultdict(int)  # total reward of each node's random playout
        self.N = defaultdict(int)  # total visit count for each node
        self.children = defaultdict(list)
        self.node = node

    def rollout(self, sims=10, score_method='royalties'):
        #  select_child
        search_node = self.select(self.node)
        # no expansion step in this version of MCTS

        #  simulate x sims
        for sim in range(sims):
            playout = search_node.random_playout(score_method=score_method)
            #  update node reward values
            self.N[search_node] += 1
            self.Q[search_node] += playout
            self.N[self.node] += 1

    def select(self, node):
        if node not in self.children:
            self.children[node] = node.get_children()

        return self.UCB(node)

    def UCB(self, node):  # upper confidence bound
        #  UCB = x + c*sqrt(log(N)/n)
        #  x = average ev of node (exploitation)
        #  c = 'exploration' weight
        #  N = parent node visits
        #  n = node visits
        children = self.children[node]
        parent_visits = self.N[node]
        if parent_visits == 0:
            log_N_parent = 0
        else:
            log_N_parent = math.log(parent_visits)

        def uct(n):
            child_visits = self.N[n]
            if child_visits == 0:
                return float('inf')
            return (self.Q[n] / self.N[n]) + (2 * math.sqrt(log_N_parent / child_visits))

        return max(children, key=uct)

    def choose(self):
        choices = self.children[self.node]

        def best_choice(n):
            visits = self.N[n]
            if visits == 0:
                return 0
            return self.Q[n] / self.N[n]

        return max(choices, key=best_choice)
