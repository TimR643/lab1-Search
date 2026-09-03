from typing import List
from vacuum_world.search.search_node import SearchNode
from vacuum_world.search.problem import SearchProblem
from vacuum_world.world.grid_pos import GridPos
from .base_search import BaseSearch


class AStarNode(SearchNode):    
    # TODO: Implement this class
    
    def __lt__(self, other):
        return True


class AStarSearch(BaseSearch):

    def __init__(self):
        super().__init__()
    
    def search(self, problem: SearchProblem) -> List[SearchNode]:
        return []
    
    
    def get_frontier_nodes(self) -> List[SearchNode]:
        return []
    
    def get_explored_nodes(self) -> List[SearchNode]:
        return []
    
    def get_all_expanded_nodes(self) -> List[SearchNode]:
        return []
    