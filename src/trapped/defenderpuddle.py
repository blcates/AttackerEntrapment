"""
The Defender class is a simple_rl MDP which is used to thwart simple_rl
task MDPs, here referred to as attackers.

The attacker simply moves toward its goal state. The defender designates
a different coordinate in the environment as a trap from which the attacker
cannot move. The defender's goal is to move the attacker to the trap instead
of the attacker's goal state. This must be done within a certain number of
steps, given as the attacker's budget.

The defender can only move the attacker to adjacent locations, which
are possible for the attacker to move to given current state, chosen
action, and slip probability.
"""

import copy
import random
import math
import numpy as np

from simple_rl.mdp import MDP
from simple_rl.tasks.grid_world.GridWorldStateClass import GridWorldState
from trapped.defenderstate import DefenderState
from trapped.search.Search import BFSSearch
from trapped.node import Node


class DefenderPuddle(MDP):
    """
    Default MDP arg values: gamma=0.99, step_cost=0
    """
    def __init__(self, attacker, attacker_planner, k=10, step_cost=0, delta=0.5):
        self.delta = delta
        self.name = "Defender"
        self.budget = k
        self.step_cost = step_cost
        self.attacker = copy.deepcopy(attacker)
        self.width = self.attacker.width
        self.height = self.attacker.height
        self.attacker_planner = attacker_planner
        self.actions = copy.deepcopy(self.attacker_planner.get_states())
        self.actions.append('NOOP')
        self.attacker_trans_dict = copy.deepcopy(self.attacker_planner.trans_dict)

        self.transition_func = self._transition_func
        self.reward_func = self._reward_func
        self.init_state = DefenderState(
            self.attacker.init_loc[0],
            self.attacker.init_loc[1],
            self.attacker.plan_actions[0],
            self.budget)

        MDP.__init__(
            self,
            self.actions,
            self.transition_func,
            self.reward_func,
            self.init_state)

        if hasattr(attacker, 'walls'):
            self.walls = attacker.walls
        else:
            self.walls = []
        if hasattr(attacker, 'lava_locs'):
            self.lava_locs = attacker.lava_locs
        else:
            self.lava_locs = []
        self.trap_locs = self.set_trap()
        self.goal_locs = self.trap_locs

    def __str__(self):
        return self.name

    def get_trap_locs(self):
        return self.trap_locs

    def get_transition_func(self):
        return self.transition_func

    def set_trap(self, numtraps=1):
        """
        Randomly select given number of trap locations.
        Args:
            numtraps (int)
        Returns:
            trap_locs (list)
        """
        trap_locs = []
        i = 0
        while i < numtraps:
            x = random.random() #random.randint(1, self.width)
            y = random.random() #random.randint(1, self.height)
            if (x, y) not in self.walls and self.width > 1:
                trap_locs.append((x, y))
                i += 1
            elif self.width <= 1:
                trap_locs.append((random.random(), random.random()))
                i += 1

        return trap_locs

    def _reward_func(self, state, action, next_state):
        """
        Get attacker state, action, and next state from defender state, action, and next state.
        Call attacker reward function with these values. Defender reward is negative of attacker reward.
        Args:
            state (DefenderState)
            action (x,y)
            next_state (DefenderState)

        Returns:
            defender_reward (float)
        """

        attacker_state = GridWorldState(state.x, state.y)
        attacker_action = state.attacker_action
        attacker_next_state = GridWorldState(next_state.x, next_state.y)
        attacker_reward = self.attacker.reward_func(attacker_state, attacker_action, attacker_next_state)
        attacker_q_value = self.attacker_planner.get_q_value(attacker_state, attacker_action)

        if action == 'NOOP':
           if next_state.budget == 0:
               defender_reward = -attacker_q_value
               return defender_reward
           return 0



        valid_move = self.check_valid_move(state, action)
        valid_move2 = self.check_valid_move(state, next_state)

        step_cost = 0

        if valid_move and valid_move2 and self.check_if_in_trap_state(next_state.x, next_state.y):
            defender_reward = 0
        elif valid_move and valid_move2 and next_state.budget == 0:
            defender_reward = -attacker_q_value
        elif valid_move and valid_move2:
            defender_reward = -attacker_reward + step_cost
        else:
            defender_reward = -attacker_reward + step_cost + -1000000

        return defender_reward

    def check_valid_move(self, state, next_state):
        """
        Check if defender action is valid. Defender action is valid if it is not a wall
        and id directly up, down, left, or right from current state.
        Args:
            state (GridWorldState)
            next_state (GridWorldState)

        Returns:
            valid_move (bool)
        """
        if next_state[0] == state[0] and abs(next_state[1] - state[1]) == 1:
            valid_move = True
        elif next_state[1] == state[1] and abs(next_state[0] - state[0]) == 1:
            valid_move = True
        elif next_state in self.walls:
            valid_move = False
        else:
            valid_move = False
        return valid_move

    def check_if_in_trap_state(self, state_x, state_y):
        if _euclidean_distance(state_x, state_y, self.goal_locs[0][0], self.goal_locs[0][1]) <= self.delta * 2:
                return True
        return False



    def _transition_func(self, defender_state, defender_action):
        """
        Check if defender action exists in attacker trans_dict. If not, return defender state
        resulting from allowing attacker action to be executed. If defender action is valid,
        return defender state resulting from defender action being executed.
        Args:
            defender_state (DefenderState)
                (x, y, attacker_action)
            defender_action (x,y)

        Returns
            next_state (DefenderState)
        """
        terminal = defender_state.is_terminal()
        if terminal:
            return defender_state


        attacker_state = GridWorldState(defender_state.x, defender_state.y)
        attacker_action = defender_state.attacker_action
        #print ("trans dict", self.attacker_planner.trans_dict[attacker_state]['up'].keys())
        try:

            trans_prob = \
                self.attacker_trans_dict[attacker_state][attacker_action][defender_action]
        except KeyError:
            trans_prob = 0
        #print ("trans dict post", self.attacker_planner.trans_dict[attacker_state]['up'].keys())

        if trans_prob == 0 or defender_state.budget == 0:
            new_attacker_state = self.attacker._transition_func(attacker_state, attacker_action)
            #print("Use attacker action... ")  # for debugging
        else:
            new_attacker_state = GridWorldState(defender_action.x, defender_action.y)
            #print("Use defender action... ",defender_action)  # for debugging

        #print ("trans dict after", self.attacker_planner.trans_dict[attacker_state]['up'].keys(), new_attacker_state, self.attacker_planner.get_states())
        next_attacker_action = self.select_next_attacker_action(new_attacker_state)
        defender_next_state = DefenderState(
            new_attacker_state[0],
            new_attacker_state[1],
            next_attacker_action,
            defender_state.budget - 1)

        if (defender_next_state.x, defender_next_state.y) in self.goal_locs or defender_next_state.budget == 0 or  self.check_if_in_trap_state(defender_next_state.x, defender_next_state.y):
            defender_next_state.set_terminal(True)

        return defender_next_state

    def select_next_attacker_action(self, attacker_state):
        """
        Select next attacker action based on attacker's value function.
        Args:
            attacker_state (GridWorldState)

        Returns:
            next_attacker_action (str)
        """
        action_probs_dict = {}
        cumsum = 0
        for action in self.attacker.actions:
            #print ("attacker state", attacker_state, action, self.attacker_planner.get_states(), self.attacker_planner.trans_dict[attacker_state]["up"].keys())
            action_prob = math.exp(self.attacker_planner.get_q_value(attacker_state, action))
            cumsum += action_prob
            action_probs_dict[action] = cumsum
        action_probs_dict = {k: v / cumsum for k, v in action_probs_dict.items()}
        rand = random.random()
        next_attacker_action = next(k for k, v in action_probs_dict.items() if v >= rand)
        return next_attacker_action

    def calculate_budget(self, max_budget):
        """
        Calculate budget for defender based. Budget is the number of steps required to reach
        the trap state without violating attacker's model of the environment.
        Returns:
            budget (int)
        """
        budget = max_budget
        start_node_name = "Location: " + str(self.init_state.x) + "," + str(self.init_state.y)
        for action in self.attacker.actions:
            start_node = Node(
                name=start_node_name + " Action: " + action,
                x=self.init_state.x,
                y=self.init_state.y,
                attacker_action=self.init_state.attacker_action)
            goal_node = BFSSearch(start_node, self.goal_test, self.succ_generator)
            if goal_node and goal_node.depth < budget:
                budget = goal_node.depth
        return budget

    def goal_test(self, node):
        """
        Calculate likelihood of step as prob in transition matrix X step number.
        For null model, prob is 1/num states
        Args:
            node (Node)
        Returns:
            goal_state (bool)
        """
        goal_state = False
        path_len_valid = False
        path_prob_valid = False
        goal_path_found = False

        step_prob_null = 1 / len(self.attacker_planner.get_states())

        prob_model_path = node.path_prob
        prob_null_path = step_prob_null ** node.depth

        if (node.x, node.y) in self.goal_locs:
            goal_state = True
        if node.depth <= self.budget:
            path_len_valid = True
        if prob_model_path >= prob_null_path:
            path_prob_valid = True
        if goal_state and path_len_valid and path_prob_valid:
            goal_path_found = True
        return goal_path_found

    def succ_generator(self, node):
        """
        Generate list of successor nodes for node. Because nodes are possible defender states,
        successor node lis includes possible positions resulting from defender action being executed,
        along with all possible attacker actions from the new position.
        Args: node (Node)
        Returns: successors (list of Nodes)
        """
        attacker_state = GridWorldState(node.x, node.y)
        attacker_action = node.attacker_action
        successors = []
        next_attacker_state = self.attacker._transition_func(attacker_state, attacker_action)
        for next_attacker_action in self.attacker.actions:
            trans_dict_prob = self.attacker_planner.trans_dict[attacker_state][attacker_action][next_attacker_state]
            node_prob = trans_dict_prob*(node.depth+1)
            if node_prob > 0:
                next_node = Node(
                    name=str(next_attacker_state) + " " + str(next_attacker_action),
                    x=next_attacker_state[0],
                    y=next_attacker_state[1],
                    attacker_action=next_attacker_action,
                    path_prob=node.path_prob * node_prob,
                    parent=node)
                successors.append(next_node)

        return successors

def _euclidean_distance(ax, ay, bx, by):
    '''
    Args:
        ax (float)
        ay (float)
        bx (float)
        by (float)

    Returns:
        (float)
    '''
    return np.linalg.norm(np.array([ax, ay]) - np.array([bx, by]))
