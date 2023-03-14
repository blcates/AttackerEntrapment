from simple_rl.tasks.puddle.PuddleMDPClass import PuddleMDP
from simple_rl.tasks.grid_world.GridWorldMDPClass import GridWorldMDP


class PuddleAttacker(PuddleMDP):
    ''' Class for a Puddle MDP '''

    def __init__(self, gamma=0.99, slip_prob=0.00, name="puddle", puddle_rects=[(0.1, 0.8, 0.5, 0.7), (0.4, 0.7, 0.5, 0.4)], goal_locs=[[1.0, 1.0]], is_goal_terminal=True, rand_init=False, step_cost=0.0):
        '''
        Args:
            gamma (float)
            slip_prob (float)
            name (str)
            puddle_rects (list): [(top_left_x, top_left_y), (bot_right_x, bot_right_y)]
            is_goal_terminal (bool)
            rand_init (bool)
            step_cost (float)
        '''
        self.delta = 0.05
        self.puddle_rects = puddle_rects
        GridWorldMDP.__init__(self, width=1.0, height=1.0, init_loc=[0.25, 0.6], goal_locs=goal_locs, gamma=gamma, name=name, is_goal_terminal=is_goal_terminal, rand_init=rand_init, step_cost=step_cost)
