"""
Search node representation for search algorithms.
"""
from typing import Optional, List
from ..world.grid_pos import GridPos


class SearchNode:
    """Represents a node in the search tree."""
    
    def __init__(self, state: GridPos, parent: Optional['SearchNode'] = None, action: Optional[str] = None, cost: float = 0.0):
        """Initialize a search node.
        
        Args:
            state: The state (grid position) this node represents
            parent: The parent node (None for root)
            action: The action taken to reach this state (unused, kept for compatibility)
            cost: The path cost to reach this state
        """
        self.state = state
        self.parent = parent
        self.cost = cost
    
    def get_path_from_root(self) -> List['SearchNode']:
        """Get the path from the root to this node.
        
        Returns:
            List of SearchNode objects from root to current node
        """
        path = []
        current = self
        
        while current is not None:
            path.append(current)
            current = current.parent
        
        # Reverse to get path from root to current
        return list(reversed(path))
    
    def get_state(self) -> GridPos:
        """Get the state (GridPos) of this node.
        
        Returns:
            The grid position state
        """
        return self.state
    
    def get_cost(self) -> float:
        """Get the path cost to this node.
        
        Returns:
            The path cost
        """
        return self.cost
    
    def __eq__(self, other) -> bool:
        """Check equality based on state."""
        if not isinstance(other, SearchNode):
            return False
        return self.state == other.state
    
    def __hash__(self) -> int:
        """Hash function based on state for use in sets."""
        return hash(self.state)
    
    def __str__(self) -> str:
        """String representation."""
        return f"SearchNode(state={self.state}, cost={self.cost})"
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"SearchNode(state={self.state}, parent={self.parent.state if self.parent else None}, cost={self.cost})"