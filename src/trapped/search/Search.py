from queue import Queue, PriorityQueue
import copy
import time


def closed_list_key(node):
    #return str(sorted(node[-1]))
    return node.name


def BFSSearch(start_state, goal_test, succ_generator):
    fringe = Queue()
    closed = set()
    fringe.put(start_state)

    while not fringe.empty():

        node = fringe.get()  # [1]

        if node != None and closed_list_key(node) not in closed:
            goal_stat = goal_test(node)
            if goal_stat:
                return node  # .get_plan()
            closed.add(closed_list_key(node))
            successor_list = succ_generator(node)
            while successor_list:
                candidate_node = successor_list.pop()
                fringe.put(candidate_node)
    return None



def AstarSearch(start_state, goal_test, succ_generator, cost=lambda x: len(x[-1]), heuristic=lambda x: 0, start_time = -1, search_limit = 30*60):
    fringe = PriorityQueue()
    closed = set()
    fringe.put((0, start_state))
    node_count = 0
    time_spent_on_goal_test = 0
    #heuristic2=lambda x: 0
    while not fringe.empty():

        node = fringe.get()[1]
        node_count += 1
        curr_time = time.time()
        if start_time != -1 and curr_time - start_time >= search_limit:
            print("Final>> No of nodes expanded", node_count)
            print("Final>> Time spent on goal test", time_spent_on_goal_test)
            return None
        if node_count % 100 == 0:
            print ("No of nodes expanded", node_count)

        #print ("NODE>>>", node)
        if node != None and closed_list_key(node) not in closed:
            goal_test_start = time.time()
            goal_stat = goal_test(node)
            time_spent_on_goal_test += (time.time() - goal_test_start)
            if goal_stat:
                print ("Final>> No of nodes expanded", node_count)
                print ("Final>> Time spent on goal test", time_spent_on_goal_test)
                return node  # .get_plan()
            closed.add(closed_list_key(node))
            successor_list = succ_generator(node)
            while successor_list:
                candidate_node = successor_list.pop()
                fringe.put((cost(candidate_node[-1]) + heuristic(candidate_node), candidate_node))

    return None

