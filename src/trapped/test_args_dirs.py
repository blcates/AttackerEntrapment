"""
This module tests the defender MDP's planning capabilities.
It instantiates a simple_rl task MDP as an attacker and an MDP defender
agent. ValueIteration planners are created for both agents to plan paths
to their respective goals.

The attacker simply moves toward its goal state. The defender designates
a different coordinate in the environment as a trap from which the attacker
cannot move. The defender's goal is to move the attacker to the trap instead
of the attacker's goal state. This must be done within a certain number of
steps, given as the attacker's budget.

The defender can only move the attacker to adjacent locations, which
are possible for the attacker to move to given current state, chosen
action, and slip probability.
"""

import time

from trapped.defender import Defender
from trapped.defenderpuddle import DefenderPuddle
from trapped.defenderplanner import DefenderPlanner
from trapped.attackerplanner import AttackerPlanner
from trapped.defenderstate import DefenderState
from trapped.rocksampleattacker import RockSampleAttacker
from trapped.PuddleMDPClass import PuddleMDP
from trapped.GridWorldMDPClass import GridWorldMDP1
from trapped.GridWorldMDPClass2 import GridWorldMDP2
from trapped.GridWorldMDPClass3 import GridWorldMDP3
from trapped.GridWorldMDPClass4 import GridWorldMDP4

from simple_rl.tasks.grid_world.GridWorldMDPClass import GridWorldMDP
from simple_rl.tasks.four_room.FourRoomMDPClass import FourRoomMDP
from simple_rl.planning.ValueIterationClass import ValueIteration


def choose_attacker(attacker_name="gridworld", planner="custom", slip_prob=0.0, length=9, breadth=9, delta=0.7):
    """
    Select attacker form simple_rl task MDPs. For planner, choose between standard ValueIteration from
    simple_rl and DefenderPlanner. Defender planner is the same as ValueIteration but with
    altered print statements.

    Note:
        Default args for simple_rl GridWorldMDP:
        width=5, height=3, init_loc=(1, 1), rand_init=False, goal_locs=[()], lava_locs=[()],
        walls=[], is_goal_terminal=True, is_lava_terminal=False, gamma=0.99, slip_prob=0.0,
        step_cost=0.0, lava_cost=1.0, name="gridworld"

        Default args for simple_rl FourRoomMDP:
        width=9, height=9, init_loc=(1,1), goal_locs=[(9,9)], lava_locs=[()],
        gamma=0.99, slip_prob=0.00, name="four_room",
        is_goal_terminal=True, rand_init=False, lava_cost=0.01, step_cost=0.0

        Default args for simple_rl PuddleMDP:
        gamma=0.99, slip_prob=0.00, name="puddle", puddle_rects=[(0.1, 0.8, 0.5, 0.7), (0.4, 0.7, 0.5, 0.4)],
        goal_locs=[[1.0, 1.0]], is_goal_terminal=True, rand_init=False, step_cost=0.0

        Default args for simple_rl RockSampleMDP:
        width=8, height=7, init_loc=(1,1), rocks=None, gamma=0.99, slip_prob=0.00, rock_rewards=[0.1, 1, 20]

    Args:
        attacker_name (str): Name of attacker
        planner(str): Name of planner
        slip_prob (float): Probability of slipping
    Returns:
        Attacker (simple_rl.tasks): Attacker
    """
    if attacker_name == "gridworld":
        attacker = GridWorldMDP1(
            # Default size is 5x3
            name="GridWorldAttacker",
            width=length,
            height=breadth,
            init_loc=(1, 1),
            goal_locs=[(length, breadth)],
            slip_prob=slip_prob)
    elif attacker_name == "gridworld2":
        attacker = GridWorldMDP2(
            # Default size is 5x3
            name="GridWorldAttacker",
            width=length,
            height=breadth,
            init_loc=(1, 1),
            goal_locs=[(length, breadth)],
            slip_prob=slip_prob)
    elif attacker_name == "gridworld3":
        attacker = GridWorldMDP3(
            # Default size is 5x3
            name="GridWorldAttacker",
            width=length,
            height=breadth,
            init_loc=(1, 1),
            goal_locs=[(length, breadth)],
            slip_prob=slip_prob)
    elif attacker_name == "gridworld4":
        attacker = GridWorldMDP4(
            # Default size is 5x3
            name="GridWorldAttacker",
            width=length,
            height=breadth,
            init_loc=(1, 1),
            goal_locs=[(length, breadth)],
            slip_prob=slip_prob)

    elif attacker_name == "fourroom":
        # Default size is 9X9
        attacker = FourRoomMDP(
            name="FourRoomAttacker",
            width=length,
            height=breadth,
            init_loc=(1, 1),
            goal_locs=[(length, breadth)],
            slip_prob=slip_prob)

    elif attacker_name == "puddle":
        # Default size is 1X1
        # Default delta is 0.05
        attacker = PuddleMDP(
            name="PuddleAttacker",
            slip_prob=slip_prob)
        attacker.delta = delta
        print ("Here")

    elif attacker_name == "rocksample":
        '''Default size is 8x7
        Default rocks: rocks = 
        [[1,2,True], [5,4,True], [6,7,True], [1,3,True], 
        [4,5,True], [2,7,False], [2,2,True], [7,4,False]]'''
        attacker = RockSampleAttacker(
            name="RockSampleAttacker",
            width=length,
            height=breadth,
            rocks=[[1, 2, True], [2, 2, False], [3, 4, True]],
            slip_prob=slip_prob)
    else:
        raise ValueError("Invalid attacker name: {}".format(attacker_name))

    if planner == "vi":
        attacker_planner = ValueIteration(attacker)
    else:
        attacker_planner = AttackerPlanner(attacker)

    return attacker, attacker_planner


def choose_defender_planner(defender, planner_name, max_iterations=10, sample_rate=3):
    """
    Select defender planner. Choose between standard ValueIteration from simple_rl
    and DefenderPlanner. Defender planner is the same as ValueIteration but with
    altered print statements.
    Args:
        planner_name (str): Name of planner
        defender (simple_rl.tasks): Defender
    Returns:
        defender_planner: simple_rl.planning
    """
    if planner_name == "vi":
        defender_planner = ValueIteration(
            defender,
            max_iterations=max_iterations,
            sample_rate=sample_rate)
    else:
        defender_planner = DefenderPlanner(
            defender,
            max_iterations=max_iterations,
            sample_rate=sample_rate)

    return defender_planner


if __name__ == "__main__":
    import sys
    domain_name = sys.argv[1]
    length = int(sys.argv[2])
    breadth = int(sys.argv[3])
    delta = float(sys.argv[4])
    print("\n********** ATTACKER PLANNING ***************************************************")
    attacker, attacker_planner = choose_attacker(domain_name, "custom", slip_prob=0.5, length=length, breadth=breadth, delta=delta)
    #attacker, attacker_planner = choose_attacker("gridworld", "custom", slip_prob=0.5)
    #attacker, attacker_planner = choose_attacker("fourroom", "custom", slip_prob=0.5)
    #attacker, attacker_planner = choose_attacker("puddle", "custom", slip_prob=0.5)
    #attacker, attacker_planner = choose_attacker("rocksample", "custom", slip_prob=0.5)
    print('\nRunning Value Iteration...')
    attacker_vi_start = time.time()
    attacker_planner.run_vi()
    attacker_vi_time = time.time() - attacker_vi_start
    print("\n--- %s seconds for attacker vi ---\n" % attacker_vi_time)
    attacker.plan_actions, attacker.plan_states = attacker_planner.plan()
    attacker_first_step_val = attacker_planner.get_value(attacker.init_state)

    print("\n********** DEFENDER PLANNING ****************************************************")
    if domain_name != "puddle": 
       defender = Defender(attacker, attacker_planner)
    else:
       defender = DefenderPuddle(attacker, attacker_planner, delta=delta)
    budget_start = time.time()
    budget = defender.calculate_budget(max_budget=15)
    #budget = 2  # Uncomment to directly set budget for testing
    defender.budget = budget
    budget_time = time.time() - budget_start
    defender.init_state = DefenderState(
        defender.attacker.init_loc[0],
        defender.attacker.init_loc[1],
        defender.attacker.plan_actions[0],
        defender.budget)
    defender_planner = choose_defender_planner(
        defender, "custom", max_iterations=1000, sample_rate=3)
    print('\nDefender budget: ' + str(budget))
    print('\nRunning Value Iteration...')
    vi_start = time.time()
    print('\nRunning Value Iteration Starting New...')
    defender_planner.run_vi()
    vi_time = time.time() - vi_start
    print('\nValue Iteration complete. Planning...')
    planning_start = time.time()
    defender.plan_actions, defender.plan_states = defender_planner.plan()
    planning_time = time.time() - planning_start
    defender_first_step_val = defender_planner.get_value(defender.init_state)

    print("\n*********** SUMMARY *************************************************************")
    print('________________________________')
    print('Starting state: ' + str(attacker.init_loc))
    print('Attacker goal: ' + str(attacker.goal_locs))
    print('Traps: ' + str(defender.get_trap_locs()))
    print('Defender budget: ' + str(budget))
    if hasattr(attacker, 'delta'):
        print('Attacker delta: ' + str(attacker.delta))
    print('Attacker Plan Actions: ' + str(attacker.plan_actions))
    print('Attacker Plan States: ' + str(attacker.plan_states))
    print('Defender Plan Actions: ' + str(defender.plan_actions))
    print('Defender Plan States: ' + str(defender.plan_states))
    print('Attacker value at first step: ' + str(attacker_first_step_val))
    print('Defender value at first step: ' + str(defender_first_step_val))
    print("--- %s seconds to calculate budget ---" % budget_time)
    print("--- %s seconds for value iteration ---" % vi_time)
    print("--- %s seconds to plan ---" % planning_time)

    if domain_name != "puddle":
        if (defender.plan_states[-1].x, defender.plan_states[-1].y) in defender.goal_locs:
           print('Defender succeeded! Attacker is at trap.')
        elif (defender.plan_states[-1].x, defender.plan_states[-1].y) in attacker.goal_locs:
           print('Defender failed. Attacker reached their goal.')
        else:
           print('Attacker is not at trap or goal.')
    else:
       if defender.check_if_in_trap_state(defender.plan_states[-1].x, defender.plan_states[-1].y):
           print('Defender succeeded! Attacker is at trap.')
       elif (defender.plan_states[-1].x, defender.plan_states[-1].y) in attacker.goal_locs:
           print('Defender failed. Attacker reached their goal.')
       else:
           print('Attacker is not at trap or goal.')
    print('________________________________')
    #attacker.visualize_interaction()  # Can be used to view grid and fourroom environment.
