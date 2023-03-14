from simple_rl.tasks.four_room.FourRoomMDPClass import FourRoomMDP


class FourRoomAttacker(FourRoomMDP):
    """
    Default values for FourRoomMDP:
    width=9, height=9, init_loc=(1,1), goal_locs=[(9,9)], lava_locs=[()],
    gamma=0.99, slip_prob=0.00, name="four_room",
    is_goal_terminal=True, rand_init=False, lava_cost=0.01, step_cost=0.0):
    """
    def __init__(self, slip_prob=0.0):
        super().__init__(lava_cost=0.0, slip_prob=slip_prob)
        self.name = "Attacker"

    def __str__(self):
        return self.name
