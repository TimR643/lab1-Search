"""
Depth First Search implementation.
Keeps expanding a successor of the last expanded state until none is left
(or the goal is reached), and backtracks when needed.
"""
from typing import List, Set
from vacuum_world.search.search_node import SearchNode
from vacuum_world.search.problem import SearchProblem
from vacuum_world.world.grid_pos import GridPos
from .base_search import BaseSearch


class DepthFirstSearch(BaseSearch):

    def __init__(self):
        super().__init__()
        # LIFO stack of SearchNode: the deepest node is always expanded first
        self.frontier: List[SearchNode] = []
        # SearchNode objects already expanded, in expansion order
        self.explored: List[SearchNode] = []
        # GridPos of the expanded nodes, for O(1) lookups
        self.explored_states: Set[GridPos] = set()
    
    def search(self, problem: SearchProblem) -> List[SearchNode]:
        """
        Perform a depth first search to find a path to goal.

        The path returned is the first one found, which is generally not the
        shortest one.
        """
        self.path = []
        self.frontier = []
        self.explored = []
        self.explored_states = set()
        
        initial_state = problem.get_initial_state()
        self.frontier.append(SearchNode(initial_state, None, None, 0.0))
        
        while self.frontier:
            # Expand the newest node of the stack, i.e. the deepest one
            current_node = self.frontier.pop()
            current_state = current_node.get_state()
            
            # The same state can be pushed several times, only expand it once
            if current_state in self.explored_states:
                continue
            
            self.explored.append(current_node)
            self.explored_states.add(current_state)
            
            # Goal test at expansion time, since the depth of the goal is unknown
            if problem.is_goal_state(current_state):
                self.path = current_node.get_path_from_root()
                return self.path
            
            if current_node.get_cost() >= self.max_depth:
                continue
            
            for successor in problem.get_successors(current_state):
                if successor in self.explored_states:
                    continue
                
                self.frontier.append(SearchNode(successor, current_node, None, current_node.get_cost() + 1))
        
        # The frontier is empty: the goal is unreachable
        return []
    
    
    def get_frontier_nodes(self) -> List[SearchNode]:
        return list(self.frontier)
    
    def get_explored_nodes(self) -> List[SearchNode]:
        return list(self.explored)
