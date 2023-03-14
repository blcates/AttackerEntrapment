"""
This module provides the same functionality as simple_rl ValueIteration. It
is only used to modify print statements for more informative output.
"""

from simple_rl.planning.ValueIterationClass import ValueIteration
import queue
import time


class DefenderPlanner(ValueIteration):
    def __init__(self, mdp,  max_iterations=10, sample_rate=3):
        super().__init__(mdp,  max_iterations=max_iterations, sample_rate=sample_rate)
        self.reachable_states = None

    def _compute_matrix_from_trans_func(self):
        #print ("status", self.has_computed_matrix)
        if self.has_computed_matrix:
            self._compute_reachable_state_space()
            # We've already run this, just return.
            return

            # K: state
            # K: a
            # K: s_prime
            # V: prob
        #print ("state size", len(self.get_states()))
        for s in self.get_states():
            for a in self.actions:
                for sample in range(self.sample_rate):
                    s_prime = self.transition_func(s, a)
                    self.trans_dict[s][a][s_prime] += 1.0 / self.sample_rate

        self.has_computed_matrix = True

    def get_gamma(self):
        return self.mdp.get_gamma()

    def get_num_states(self):
        if not self.reachability_done:
            self._compute_reachable_state_space()
        return len(self.states)

    def get_states(self):
        if self.reachability_done:
            return list(self.states)
        else:
            self._compute_reachable_state_space()
            return list(self.states)

    def get_value(self, s):
        '''
        Args:
            s (State)

        Returns:
            (float)
        '''
        return self._compute_max_qval_action_pair(s)[0]

    def get_q_value(self, s, a):
        '''
        Args:
            s (State)
            a (str): action

        Returns:
            (float): The Q estimate given the current value function @self.value_func.
        '''
        # Compute expected value.
        expected_val = 0
        sprime_list = []
        for s_prime in self.trans_dict[s][a].keys():
            '''
            print(s, a, s_prime,
                  self.trans_dict[s][a][s_prime] * self.reward_func(s, a, s_prime) + self.gamma * self.trans_dict[s][a][
                      s_prime] * self.value_func[s_prime])
            '''
            # For debugging
            '''
            trans = self.trans_dict[s][a][s_prime]
            reward = self.reward_func(s, a, s_prime)
            value = self.value_func[s_prime]
            sprime_list.append(s_prime)'''
            expected_val += self.trans_dict[s][a][s_prime] * self.reward_func(s, a, s_prime) + self.gamma * \
                            self.trans_dict[s][a][s_prime] * self.value_func[s_prime]

        # for debugging
        '''if expected_val == 0:
            print("**************GET Q VALUE**************")
            print("s: ", s, "a: ", a, "sprime_list: ", sprime_list)'''

        return expected_val

    def _compute_reachable_state_space(self):
        '''
        Summary:
            Starting with @self.start_state, determines all reachable states
            and stores them in self.states.
        '''

        if self.reachability_done:
            return

        state_queue = queue.Queue()
        state_queue.put(self.init_state)
        self.states.add(self.init_state)

        while not state_queue.empty():
            #print (self.states)
            s = state_queue.get()
            for a in self.actions:
                for samples in range(self.sample_rate):  # Take @sample_rate samples to estimate E[V]
                    next_state = self.transition_func(s, a)

                    if next_state not in self.states:
                        self.states.add(next_state)
                        state_queue.put(next_state)

        self.reachability_done = True

    def run_vi(self):
        '''
        Returns:
            (tuple):
                1. (int): num iterations taken.
                2. (float): value.
        Summary:
            Runs ValueIteration and fills in the self.value_func.
        '''
        # Algorithm bookkeeping params.
        iterations = 0
        max_diff = float("inf")
        print ("Starting compute matrx")
        model_start_time = time.time()
        self._compute_matrix_from_trans_func()
        model_time = time.time() - model_start_time
        print("Finished compute matrx")
        print("Model time: ", model_time)
        state_space = self.get_states()
        self.bellman_backups = 0

        # Main loop.
        planning_start_time = time.time()
        while max_diff > self.delta and iterations < self.max_iterations:
            max_diff = 0
            for s in state_space:
                self.bellman_backups += 1
                if s.is_terminal():
                    continue

                max_q = float("-inf")
                for a in self.actions:
                    q_s_a = self.get_q_value(s, a)
                    max_q = q_s_a if q_s_a > max_q else max_q

                # Check terminating condition.
                max_diff = max(abs(self.value_func[s] - max_q), max_diff)

                # Update value.
                self.value_func[s] = max_q
            iterations += 1

        planning_time = time.time() - planning_start_time
        print("Planning time: ", planning_time)
        value_of_init_state = self._compute_max_qval_action_pair(self.init_state)[0]
        self.has_planned = True

        return iterations, value_of_init_state

    def get_num_backups_in_recent_run(self):
        if self.has_planned:
            return self.bellman_backups
        else:
            print("Warning: asking for num Bellman backups, but VI has not been run.")
            return 0

    def print_value_func(self):
        for key in self.value_func.keys():
            print(key, ":", self.value_func[key])

    def plan(self, state=None, horizon=50):
        '''
        Args:
            state (State)
            horizon (int)

        Returns:
            (list): List of actions
        '''

        state = self.mdp.get_init_state() if state is None else state

        if self.has_planned is False:
            print("Warning: VI has not been run. Plan will be random.")

        action_seq = []
        state_seq = [state]
        steps = 0

        # Only changes made to this function are to allow print statements.
        print("**************PLAN*************************************************************************")
        while (not state.is_terminal()) and steps < horizon:
            print("\nStep", steps, "-------------------\n")
            print("Possible defender actions:")
            next_action = self._get_max_q_action(state)
            action_seq.append(next_action)
            print("\nCurrent state:", state.__str__())
            print("Best action: ", next_action)
            state = self.transition_func(state, next_action)
            '''if state.x == next_action.x and state.y == next_action.y:
                print("Successful defender action")
            else:
                print("Defender action failed, use attacker action")'''
            print("State after action: ", state)
            state_seq.append(state)
            steps += 1

        return action_seq, state_seq

    def _get_max_q_action(self, state):
        '''
        Args:
            state (State)

        Returns:
            (str): The action with the max q value in the given @state.
        '''
        return self._compute_max_qval_action_pair(state)[1]

    def get_max_q_actions(self, state):
        '''
        Args:
            state (State)

        Returns:
            (list): List of actions with the max q value in the given @state.
        '''
        max_q_val = self.get_value(state)
        best_action_list = []

        # Find best action (action w/ current max predicted Q value)
        for action in self.actions:
            q_s_a = self.get_q_value(state, action)
            if q_s_a == max_q_val:
                best_action_list.append(action)

        return best_action_list

    def policy(self, state):
        '''
        Args:
            state (State)

        Returns:
            (str): Action

        Summary:
            For use in a FixedPolicyAgent.
        '''
        return self._get_max_q_action(state)

    def _compute_max_qval_action_pair(self, state):
        '''
        Args:
            state (State)

        Returns:
            (tuple) --> (float, str): where the float is the Qval, str is the action.
        '''
        # Grab random initial action in case all equal
        max_q_val = float("-inf")
        best_action = self.actions[0]

        # Find best action (action w/ current max predicted Q value)
        for action in self.actions:
            q_s_a = self.get_q_value(state, action)

            # Only change made to this function is to allow print statement.
            if q_s_a > -9000:
                print("State: ", state, "Action: ", action, "Qval: ", q_s_a)

            if q_s_a > max_q_val:
                max_q_val = q_s_a
                best_action = action

        print("Defender max q val: ", max_q_val)
        return max_q_val, best_action
