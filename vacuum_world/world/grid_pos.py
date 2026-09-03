"""
Represents any position, cell and objects alike
"""
import math
from typing import Tuple


class GridPos:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, GridPos):
            return False
        return self.x == other.x and self.y == other.y
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))
    
    def __str__(self) -> str:
        return f"({self.x}, {self.y})"
    
    def __repr__(self) -> str:
        return f"GridPos({self.x}, {self.y})"
    
    def distance_euclidean(self, other: 'GridPos') -> float:
        """
        Calculate the Euclidean distance between this position and another.
        """
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx ** 2 + dy ** 2)
    
    def distance_manhattan(self, other: 'GridPos') -> int:
        """
        Calculate the Manhattan distance between this position and another.
        """
        return abs(self.x - other.x) + abs(self.y - other.y)
    
    def get_neighbors(self) -> list['GridPos']:
        """Get the four neighboring positions (up, down, left, right).
        
        Returns:
            List of neighboring GridPos objects
        """
        return [
            GridPos(self.x, self.y - 1),  # North
            GridPos(self.x, self.y + 1),  # South
            GridPos(self.x + 1, self.y),  # East
            GridPos(self.x - 1, self.y)   # West
        ]
    
    def to_tuple(self) -> Tuple[int, int]:
        """Convert to a tuple (x, y).
        
        Returns:
            Simpler tuple representation of the position
        """
        return (self.x, self.y)