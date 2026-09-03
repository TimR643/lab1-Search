"""
Intelligent vacuum agent that uses search algorithms to clean dirt.
"""
import time
from typing import List, Optional
from enum import Enum
from rich import print
from ..world.world import World, Action
from ..world.grid_pos import GridPos
from ..search.search_node import SearchNode
from ..search.problem import SearchProblem
from ..search.breadth_first_search import BreadthFirstSearch
from ..search.depth_first_search import DepthFirstSearch
from ..search.a_star_search import AStarSearch
from ..search.random_search import RandomSearch


def agent_print(message: str):
    print(f"[bold cyan]Agent:[/bold cyan] {message}")


class SearchMethod(Enum):
    BREADTH_FIRST_SEARCH = "bfs"
    DEPTH_FIRST_SEARCH = "dfs"
    A_STAR_SEARCH = "astar"
    RANDOM_SEARCH = "random"


class IntelligentVacuumAgent:
    def __init__(self, world: World):
        self.world = world
        self.search_method = SearchMethod.BREADTH_FIRST_SEARCH
        self.target: Optional[GridPos] = None
        self.current_path: List[SearchNode] = []
        self.current_path_index = 0
        self.max_depth = 1000000
    
    def set_search_method(self, method: SearchMethod):
        self.search_method = method
    
    def step(self, real_world: World):
        if real_world.is_terminated():
            return
        
        action = self.choose_action()
        self.act(action, real_world)
    
    def choose_action(self) -> Action:
        """
        Choose the next action to take (without executing it)
        """

        # Are we at the dirt's location?
        if (self.target is not None and 
            self.world.agent and 
            self.world.agent.at_position(self.target)):
            
            dirt = self.world.get_dirt_at_position(self.target)
            if dirt is None:
                # Dirt was already removed
                self.target = None
                return Action.NO_OPERATION
            else:
                # Suck dirt
                self.target = None
                return Action.SUCK_DIRT
        
        # Do we need to select a new target dirt?
        target = self.select_target(self.target)
        if target is None:
            agent_print("No more dirt, the maze is shining clean!")
            return Action.NO_OPERATION
        elif target != self.target:
                self.target = target
                self.reset_plan()
        
        # Do we need to plan a path?
        if not self.current_path:
            path = self.plan_to_target(self.target, self.world)
            self.current_path = path
            self.current_path_index = 0
        
        # If we still have no path, then path planning failed (check if the target was unreachable?)
        if not self.current_path:
            agent_print("No path found!")
            return Action.NO_OPERATION
        else:
            # Follow the plan
            action = self.step_to_target(self.current_path, self.world)
            return action
    
    def act(self, action: Action, world: World):
        """Execute an action in the world.
        
        Args:
            action: The action to execute
            world: The world to act in
        """
        if action == Action.SUCK_DIRT:
            agent_print("Vacuuming Dirt")
            world.suck_dirt()
        elif action == Action.GO_NORTH:
            world.move_agent(Action.GO_NORTH)
        elif action == Action.GO_SOUTH:
            world.move_agent(Action.GO_SOUTH)
        elif action == Action.GO_EAST:
            world.move_agent(Action.GO_EAST)
        elif action == Action.GO_WEST:
            world.move_agent(Action.GO_WEST)
        elif action == Action.NO_OPERATION:
            agent_print("NO-OP Action")
        else:
            agent_print(f"Unknown Action: {action}")
    
    def select_target(self, last_target: Optional[GridPos]) -> Optional[GridPos]:
        """Select the closest dirt particle as target.
        
        Args:
            last_target: The previous target (None to select new)
            
        Returns:
            Selected target or None if no dirt available
        """
        uncleaned_dirt = self.world.get_all_uncleaned_dirt()
        
        if len(uncleaned_dirt) == 0:
            return None
        
        if last_target is None:
            if not self.world.agent:
                return uncleaned_dirt[0]
            
            agent_pos = GridPos(self.world.agent.x, self.world.agent.y)
            best_dist = float('inf')
            target = None
            
            for dirt in uncleaned_dirt:
                dist = agent_pos.distance_euclidean(dirt)
                if dist < best_dist:
                    best_dist = dist
                    target = dirt
            
            return target
        else:
            return last_target
    
    def step_to_target(self, path: List[SearchNode], world: World) -> Action:
        """Make one step towards the target following the path.
        
        Args:
            path: The path to follow
            world: The world to move in
            
        Returns:
            The action to take
        """
        if not path:
            agent_print("NO PATH FOUND!")
            return Action.NO_OPERATION
        
        if self.current_path_index >= len(path):
            return Action.NO_OPERATION
        
        node = path[self.current_path_index]
        self.current_path_index += 1
        
        next_pos = node.get_state()
        
        if not world.agent:
            return Action.NO_OPERATION
        
        dx = next_pos.x - world.agent.x
        dy = next_pos.y - world.agent.y
        
        # Determine action based on direction
        if dx > 0:
            return Action.GO_EAST
        elif dx < 0:
            return Action.GO_WEST
        elif dy < 0:
            return Action.GO_NORTH
        elif dy > 0:
            return Action.GO_SOUTH
        else:
            return Action.NO_OPERATION
    
    def plan_to_target(self, dest: GridPos, world: World) -> List[SearchNode]:
        """Plan a path to the target using the selected search method.
        
        Args:
            dest: The destination position
            world: The world to plan in
            
        Returns:
            List of SearchNode objects representing the path
        """
        if not world.agent:
            return []
        
        start = GridPos(world.agent.x, world.agent.y)
        goal = dest
        
        if start is None or goal is None:
            return []
        
        agent_print(f"planning from {start} to {goal}")
        
        search_result = self.search_plan(world, start, goal, self.search_method, True)
        
        if search_result:
            path = search_result.get_path()
            
            # Update path graphics in world
            if path:
                path_positions = [node.get_state() for node in path]
                world.mark_current_path(path_positions)
            
            # Update explored state graphics in world
            expanded_positions = [node.get_state() for node in search_result.get_all_expanded_nodes()]
            world.mark_expanded_nodes(expanded_positions)
            
            return path
        
        return []
    
    def reset_plan(self):
        self.current_path = []
        self.current_path_index = 0
    
    def search_plan(self, 
                   world: World, 
                   start: GridPos, 
                   goal: GridPos, 
                   method: SearchMethod, 
                   print_result: bool = True):
        """Search for a plan using the specified method.
        
        Args:
            world: The world to search in
            start: The start position
            goal: The goal position
            method: The search method to use
            print_result: Whether to print timing results
            
        Returns:
            The search object with results, or None if failed
        """
        start_time = time.time()
        problem = SearchProblem(world, start, goal)
        
        
        if method == SearchMethod.RANDOM_SEARCH:
            if print_result:
                agent_print("starting Random Search")
            search_run = RandomSearch()
        elif method == SearchMethod.BREADTH_FIRST_SEARCH:
            if print_result:
                agent_print("starting Breadth First Search Method (BFS)")
            search_run = BreadthFirstSearch()
        elif method == SearchMethod.DEPTH_FIRST_SEARCH:
            if print_result:
                agent_print("starting Depth First Search Method (DFS)")
            search_run = DepthFirstSearch()
        elif method == SearchMethod.A_STAR_SEARCH:
            if print_result:
                agent_print("starting A*")
            search_run = AStarSearch()
        else:
            agent_print(f"Unknown search method: {method}")
            return None
        
        problem.reset_expanded_count()
        path = search_run.search(problem)
        
        end_time = time.time()
        elapsed_time = (end_time - start_time) * 1000
        
        if print_result:
            print(f"\tNeeded {elapsed_time:.1f} msec, PathLength: {len(path)}, "
                  f"NumExpNodes: {problem.get_num_expanded_nodes()}")
        
        return search_run
