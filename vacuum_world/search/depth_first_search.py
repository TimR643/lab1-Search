from typing import List
from vacuum_world.search.search_node import SearchNode
from vacuum_world.search.problem import SearchProblem
from .base_search import BaseSearch


class DepthFirstSearch(BaseSearch):

    def __init__(self):
        super().__init__()

#the goal is to implement a depth-first algorithm, which always expands the deepest node first  
    def search(self, problem: SearchProblem) -> List[SearchNode]:
        self.path = [] #reset the path to empty list 
        self.frontier = [SearchNode(problem.get_initial_state())]  #finding initial state and creating the trees root
        self.explored = [] #empty the explored list
        frontier_states = {problem.get_initial_state()} #finding the intial state
        explored_states = set()

        while self.frontier: #do while there are still nodes in the frontier
            node = self.frontier.pop() # pop the last node from the frontier -> LIFO
            frontier_states.remove(node.get_state()) #remove the state of this taken node

            if problem.is_goal_state(node.get_state()): #check for goal state
                self.path = node.get_path_from_root() #path = path from root to this node
                return self.path

            self.explored.append(node) #append new node
            explored_states.add(node.get_state())

            if node.get_cost() >= self.max_depth:
                continue

            # Reverse insertion preserves the maze's documented N/S/E/W order
            # when items are removed from the LIFO stack.
            for state in reversed(problem.get_successors(node.get_state())):
                if state in explored_states or state in frontier_states:
                    continue
                child = SearchNode(state, node, cost=node.get_cost() + 1)
                self.frontier.append(child)
                frontier_states.add(state)

            return []
    
    
    def get_frontier_nodes(self) -> List[SearchNode]:
        return list(self.frontier)
    
    def get_explored_nodes(self) -> List[SearchNode]:
        return list(self.explored)