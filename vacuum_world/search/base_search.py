"""
Abstract base class for all search algorithms.
"""
from abc import ABC, abstractmethod
from typing import List
from .search_node import SearchNode
from .problem import SearchProblem


class BaseSearch(ABC):
    """
    Abstract base class for all search algorithms.
    
    This class defines the common interface that all search algorithms should implement.
    By using the methods and class attributes provided, you ensure that the visualization will properly display the relevant data structures.

    Note that some methods have to be adapted to fit the data structures required in input and ouput.s
    """
    
    def __init__(self, max_depth: int = 1000000):
        """
        Initialize the search algorithm.
        
        Args:
            max_depth: Maximum search depth or steps
        """
        self.max_depth = max_depth
        self.path: List[SearchNode] = []

        # Tailor the following data structures to the needs of the search algorithm
        self.frontier = []
        self.explored = []
    
    @abstractmethod
    def search(self, problem: SearchProblem) -> List[SearchNode]:
        """
        Perform search to find path from initial state to goal.
        
        Args:
            problem: The search problem to solve
            
        Returns:
            List of SearchNode objects representing path to goal,
            empty list if no path exists
        """
        pass
    
    def get_path(self) -> List[SearchNode]:
        """
        Get the path found by the search.
        
        Returns:
            List of SearchNode objects representing the path to goal
        """
        return self.path
    
    @abstractmethod
    def get_frontier_nodes(self) -> List[SearchNode]:
        """
        Get all nodes currently in the frontier.
        
        Returns:
            List of SearchNode objects in the frontier
        """
        pass
    
    @abstractmethod
    def get_explored_nodes(self) -> List[SearchNode]:
        """
        Get all nodes that have been explored.
        
        Returns:
            List of SearchNode objects that have been explored
        """
        pass
    
    def get_all_expanded_nodes(self) -> List[SearchNode]:
        """
        Get all nodes that have been expanded (frontier + explored).
        
        Default implementation combines frontier and explored nodes.
        Subclasses can override if they need different behavior.
        
        Returns:
            List of all SearchNode objects that have been expanded
        """
        all_nodes = self.get_explored_nodes()
        all_nodes.extend(self.get_frontier_nodes())
        return all_nodes