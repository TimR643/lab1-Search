"""
Random Search implementation.
A simple search method that randomly explores the maze until it finds the target.
"""
import random
from typing import List
from .search_node import SearchNode
from .problem import SearchProblem
from .base_search import BaseSearch


class RandomSearch(BaseSearch):
    """
    Random Search implementation.
    """
    
    def __init__(self):
        """Initialize Random Search.
        
        Args:
            max_depth: Maximum number of random steps before giving up
        """
        super().__init__()
    
    def search(self, problem: SearchProblem) -> List[SearchNode]:
        """
        Perform a random search to find a path to goal.
        """
        self.path = []
        
        initial_state = problem.get_initial_state()
        current_node = SearchNode(initial_state, None, None, 0.0)
        path_nodes = [current_node]
        
        steps = 0
        
        while steps < self.max_depth:
            current_state = current_node.get_state()
            
            # Check if we've reached the goal
            if problem.is_goal_state(current_state):
                self.path = path_nodes
                return self.path
            
            # Get all possible successors
            successors = problem.get_successors(current_state)
            
            if not successors:
                break
            
            # Choose randomly from all available successors
            next_state = random.choice(successors)
            
            # Create next node and add to path
            next_node = SearchNode(next_state, current_node, None, current_node.get_cost() + 1)
            path_nodes.append(next_node)
            current_node = next_node
            
            steps += 1
        
        return []
    
    
    def get_frontier_nodes(self) -> List[SearchNode]:
        return []
    
    def get_explored_nodes(self) -> List[SearchNode]:
        return []
    
    def get_all_expanded_nodes(self) -> List[SearchNode]:
        return []