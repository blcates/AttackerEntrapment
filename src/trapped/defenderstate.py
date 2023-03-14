"""
This class is a modification of simple_rl's GridWorldState class. It
represents the state of the defender as an x,y coordinate, the action
the attacker is taking, and the defender's budget.
"""

from simple_rl.tasks.grid_world.GridWorldStateClass import GridWorldState


class DefenderState(GridWorldState):
    def __init__(self, x, y, attacker_action, budget=10):
        super().__init__(x, y)
        self.data = [x, y, attacker_action, budget]
        self.attacker_action = attacker_action
        self.budget = budget

    def __str__(self):
        return "s: (" + str(self.x) + "," + str(self.y) + "," + str(self.attacker_action) + "," + str(
            self.budget) + ")"
