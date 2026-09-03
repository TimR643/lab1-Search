"""
Representation of a search problem, which contains the world, the initial state, and the goal.
"""
from typing import List
from ..world.grid_pos import GridPos
from ..world.world import World


class SearchProblem:
    """Search problem for navigating in the grid world."""
    
    def __init__(self, world: World, initial_state: GridPos, goal_state: GridPos):
        """Initialize the grid search problem.
        
        Args:
            world: The world instance
            initial_state: The starting position
            goal_state: The target position
        """
        self.world = world
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.num_expanded_nodes = 0  # A counter that is automatically managed
    
    def get_initial_state(self) -> GridPos:
        """Get the initial state.
        
        Returns:
            The initial GridPos
        """
        return self.initial_state
    
    def is_goal_state(self, state: GridPos) -> bool:
        """Check if a state is a goal state.
        
        Args:
            state: The state to check
            
        Returns:
            True if it's the goal state, False otherwise
        """
        return state == self.goal_state
    
    def get_successors(self, state: GridPos) -> List[GridPos]:
        """Get all reachable states from the given state.
        
        Args:
            state: The current state
            
        Returns:
            List of reachable GridPos objects
        """
        successors = self.world.maze.get_reachable_positions(state)
        self.num_expanded_nodes += len(successors)
        return successors
    
    def reset_expanded_count(self):
        self.num_expanded_nodes = 0
    
    def get_num_expanded_nodes(self) -> int:
        return self.num_expanded_nodes