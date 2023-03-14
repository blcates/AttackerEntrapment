from simple_rl.tasks import GridWorldMDP


class GridWorldAttacker(GridWorldMDP):
    """
    Default values for GridWorldMDP:
    width=5, height=3, init_loc=(1, 1), rand_init=False, goal_locs=[()], lava_locs=[()],
    walls=[], is_goal_terminal=True, is_lava_terminal=False, gamma=0.99, slip_prob=0.0,
    step_cost=0.0, lava_cost=1.0, name="gridworld"):
    """
    def __init__(self, slip_prob=0.0):
        super().__init__(
            name="Attacker",
            width=5,
            height=5,
            init_loc=(1, 1),
            goal_locs=[(5, 5)],
            slip_prob=slip_prob)

    def __str__(self):
        return self.name