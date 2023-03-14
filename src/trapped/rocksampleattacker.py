"""
Copy of simple_rl.tasks.dev_rock_sample.RockSampleMDPClass.
Modified reward_function to work with ValueIteration. Original
function took two args (state, action). ValueIteration passes
three args (state, action, next_state) to reward_function.
"""
from simple_rl.tasks.dev_rock_sample.RockSampleMDPClass import RockSampleMDP


class RockSampleAttacker(RockSampleMDP):
    def __init__(self,
                 width=8,
                 height=7,
                 init_loc=(1, 1),
                 rocks=None,
                 gamma=0.99,
                 slip_prob=0.00,
                 rock_rewards=[0.1, 1, 20],
                 name="rocksample"):
        super().__init__(width=width,
                         height=height,
                         init_loc=init_loc,
                         rocks=rocks,
                         gamma=gamma,
                         slip_prob=slip_prob,
                         rock_rewards=rock_rewards,
                         name=name)
        self.goal_locs = rocks  # Should goal_locs be rocks or exit area?

    def _reward_func(self, state, action, next_state):
        if state[0] == self.width-1 and action == "right":
            # Moved into exit area, receive 10 reward.
            return 10.0
        elif action == "sample":
            rock_index = self._get_rock_at_agent_loc(state)
            if rock_index != None:
                if state.data[rock_index + 2]:
                    # Sampled good rock.
                    return self.rock_rewards[rock_index % 3]
                else:
                    # Sampled bad rock.
                    return -self.rock_rewards[rock_index % 3]

        return 0
