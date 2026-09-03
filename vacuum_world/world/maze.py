"""
Maze generation and representation for the vacuum world.
"""
import random
from enum import Enum
from typing import List, Set
from .grid_pos import GridPos


class MazeType(Enum):
    """Types of mazes that can be generated."""
    MAZE_LABYRINTH = "labyrinth"
    MAZE_ONLY_BORDER = "only_border"
    MAZE_OFFICE = "office"
    MAZE_CAVES = "caves"


class Maze:
    """Represents the maze structure of the world."""
    
    def __init__(self, width: int, height: int, maze_type: MazeType = MazeType.MAZE_LABYRINTH):
        self.width = width
        self.height = height
        self.maze_type = maze_type
        self.walls: Set[GridPos] = set()
        self._generate_maze()
    
    def _generate_maze(self):
        """Generate the maze structure based on the maze type."""
        if self.maze_type == MazeType.MAZE_ONLY_BORDER:
            self._generate_border_only()
        elif self.maze_type == MazeType.MAZE_OFFICE:
            self._generate_office_maze()
        elif self.maze_type == MazeType.MAZE_CAVES:
            self._generate_caves()
        else:
            self._generate_labyrinth()
    
    def _generate_border_only(self):
        """Generate a maze with walls only on the border."""
        for x in range(self.width):
            self.walls.add(GridPos(x, 0))
            self.walls.add(GridPos(x, self.height - 1))
        
        for y in range(self.height):
            self.walls.add(GridPos(0, y))
            self.walls.add(GridPos(self.width - 1, y))
    
    def _generate_office_maze(self):
        """
        Generate an office-like maze with a few rooms and openings between them.
        """
        self._generate_border_only()

        # Higher values of this make the probability that no path exists quite high
        WALL_CHANCE = 0.6
        
        room_size = min(self.width, self.height) // 4
        
        for x in range(room_size, self.width - room_size + 1, room_size):
            for y in range(1, self.height - 1):
                if random.random() < WALL_CHANCE:
                    self.walls.add(GridPos(x, y))
        
        for y in range(room_size, self.height - room_size + 1, room_size):
            for x in range(1, self.width - 1):
                if random.random() < WALL_CHANCE:
                    self.walls.add(GridPos(x, y))
    
    def _generate_labyrinth(self):
        """
        Generate a maze with random walls.
        """
        self._generate_border_only()

        # Higher values of this make the probability that no path exists quite high
        WALL_CHANCE = 0.3
        
        for x in range(2, self.width - 2):
            for y in range(2, self.height - 2):
                if random.random() < WALL_CHANCE:
                    self.walls.add(GridPos(x, y))
    
    def _generate_caves(self):
        """
        Generate cave-like structures using a cellular automaton.
        """
        # TODO: add cave connectivity check

        # Feel free to tweak these values if you find that the cave is too often fragmented into non-connex components.
        INITIAL_WALL_CHANCE = 0.61
        WALL_THRESHOLD = 5
        
        for x in range(self.width):
            for y in range(self.height):
                if random.random() < INITIAL_WALL_CHANCE:
                    self.walls.add(GridPos(x, y))
        
        for _ in range(5):
            self._cellular_automata_step(WALL_THRESHOLD)
        
        self._generate_border_only()
    
    def _cellular_automata_step(self, wall_threshold = 5):
        new_walls = set()
        
        for x in range(1, self.width - 1):
            for y in range(1, self.height - 1):
                wall_neighbors = self._count_wall_neighbors(x, y)
                
                if wall_neighbors >= wall_threshold:
                    new_walls.add(GridPos(x, y))
        
        self.walls = new_walls
    
    def _count_wall_neighbors(self, x: int, y: int) -> int:
        count = 0
        
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                
                neighbor_x = x + dx
                neighbor_y = y + dy
                
                if (neighbor_x < 0 or neighbor_x >= self.width or 
                    neighbor_y < 0 or neighbor_y >= self.height):
                    count += 1
                elif GridPos(neighbor_x, neighbor_y) in self.walls:
                    count += 1
        
        return count
    
    def is_wall(self, pos: GridPos) -> bool:
        return pos in self.walls
    
    def is_valid_position(self, pos: GridPos) -> bool:
        """
        Check if a position is valid (within bounds and not a wall).
        """
        return (0 <= pos.x < self.width and 
                0 <= pos.y < self.height and 
                not self.is_wall(pos))
    
    def get_reachable_positions(self, pos: GridPos) -> List[GridPos]:
        """
        Get all reachable positions from a given position.
        """
        reachable = []
        
        for neighbor in pos.get_neighbors():
            if self.is_valid_position(neighbor):
                reachable.append(neighbor)

        return reachable
    
    def get_all_free_positions(self) -> List[GridPos]:
        """
        Get all free (non-wall) positions in the maze.
        """
        free_positions = []

        for x in range(self.width):
            for y in range(self.height):
                pos = GridPos(x, y)
                if self.is_valid_position(pos):
                    free_positions.append(pos)

        return free_positions