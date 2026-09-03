"""
Main world class that coordinates all world components.
"""
import random
from typing import List, Optional, Set
from enum import Enum
from .grid_pos import GridPos
from .maze import Maze, MazeType
from .dirt import Dirt
from .agent import VacuumAgent


class Action(Enum):
    GO_NORTH = "north"
    GO_SOUTH = "south"
    GO_EAST = "east"
    GO_WEST = "west"
    SUCK_DIRT = "suck"
    NO_OPERATION = "noop"


class World:
    """The main world class containing the representations of the maze, agent, and dirt."""
    
    def __init__(self, 
                 width: int = 20,
                 height: int = 20, 
                 num_dirt: int = 10,
                 maze_type: MazeType = MazeType.MAZE_LABYRINTH,
                 seed: Optional[int] = None):
        """Initialize the world.
        
        Args:
            width: Width of the world
            height: Height of the world
            num_dirt: Number of dirt particles to place
            maze_type: Type of maze to generate
            seed: Seed for the random number generator
        """
        # Handle random seed
        if seed is None:
            seed = random.randint(0, 999999)
        random.seed(seed)
        self.seed = seed
            
        self.width = width
        self.height = height
        self.maze = Maze(width, height, maze_type)
        self.dirt_particles: Set[Dirt] = set()
        self.agent: Optional[VacuumAgent] = None
        
        self._place_agent()
        self._place_dirt(num_dirt)
        
        self.current_path: List[GridPos] = []
        self.expanded_nodes: Set[GridPos] = set()
        
        self.observers = []
    
    def _place_agent(self):
        """Place the agent at a random free position."""
        free_positions = self.maze.get_all_free_positions()
        if free_positions:
            pos = random.choice(free_positions)
            self.agent = VacuumAgent(pos.x, pos.y)
    
    def _place_dirt(self, num_dirt: int):
        """Place dirt particles at random free positions."""
        free_positions = self.maze.get_all_free_positions()
        
        if self.agent:
            agent_pos = GridPos(self.agent.x, self.agent.y)
            free_positions = [pos for pos in free_positions if pos != agent_pos]
        
        num_to_place = min(num_dirt, len(free_positions))
        chosen_positions = random.sample(free_positions, num_to_place)
        
        for pos in chosen_positions:
            self.dirt_particles.add(Dirt(pos.x, pos.y))
    
    def get_dirt_at_position(self, pos: GridPos) -> Optional[Dirt]:
        """Get dirt at a specific position."""
        for dirt in self.dirt_particles:
            if dirt == pos and not dirt.is_cleaned():
                return dirt
        return None
    
    def get_all_uncleaned_dirt(self) -> List[Dirt]:
        """Get all uncleaned dirt particles."""
        return [dirt for dirt in self.dirt_particles if not dirt.is_cleaned()]
    
    def is_terminated(self) -> bool:
        """Check if the world is in a terminal state (all dirt cleaned)."""
        return len(self.get_all_uncleaned_dirt()) == 0
    
    def move_agent(self, action: Action) -> bool:
        """Move the agent according to the specified action.
            
        Returns:
            True if the move was successful, False otherwise
        """
        if not self.agent:
            return False
            
        current_pos = GridPos(self.agent.x, self.agent.y)
        new_pos = None
        
        if action == Action.GO_NORTH:
            new_pos = GridPos(current_pos.x, current_pos.y - 1)
        elif action == Action.GO_SOUTH:
            new_pos = GridPos(current_pos.x, current_pos.y + 1)
        elif action == Action.GO_EAST:
            new_pos = GridPos(current_pos.x + 1, current_pos.y)
        elif action == Action.GO_WEST:
            new_pos = GridPos(current_pos.x - 1, current_pos.y)
        
        if new_pos and self.maze.is_valid_position(new_pos):
            self.agent.move_to(new_pos)
            self.notify_observers()
            return True
        
        return False
    
    def suck_dirt(self) -> bool:
        """Remove the dirt on the position of the agent, if there is some.
        
        Returns:
            True if some dirt was removed, False otherwise
        """
        if not self.agent:
            return False
            
        agent_pos = GridPos(self.agent.x, self.agent.y)
        dirt = self.get_dirt_at_position(agent_pos)
        
        if dirt:
            dirt.clean()
            self.agent.collect_dirt()
            self.notify_observers()
            return True
        
        return False
    
    def mark_current_path(self, path: List[GridPos]):
        """Mark the current path for visualization."""
        self.current_path = path.copy()
        self.notify_observers()
    
    def mark_expanded_nodes(self, nodes: List[GridPos]):
        """Mark the expanded nodes for visualization."""
        self.expanded_nodes = set(nodes)
        self.notify_observers()
    
    def add_observer(self, observer):
        """Add an observer for world changes."""
        self.observers.append(observer)
    
    def notify_observers(self):
        """Notify all observers of world changes."""
        for observer in self.observers:
            if hasattr(observer, 'update'):
                observer.update()
    
    def get_state_info(self) -> dict:
        """Get current state information, for use in the commande-line interface."""
        return {
            'agent_position': (self.agent.x, self.agent.y) if self.agent else None,
            'dirt_collected': self.agent.get_dirt_collected() if self.agent else 0,
            'remaining_dirt': len(self.get_all_uncleaned_dirt()),
            'is_terminated': self.is_terminated()
        }